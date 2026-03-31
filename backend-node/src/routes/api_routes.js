const express = require('express');
const multer = require('multer');
const os = require('os');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');

const { EmployeeParser, AssignmentParser } = require('../parsers/file_parser');
const { SecretSantaService, AssignmentError } = require('../services/secret_santa_service');
const { ExportService } = require('../services/export_service');
const { AssignmentInputValidator } = require('../validators/input_validator');
const { MongoService } = require('../services/mongo_service');
const { Assignment, Employee } = require('../models/employee');

const router = express.Router();

const upload = multer({ dest: os.tmpdir() });

const employeeParser = new EmployeeParser();
const assignmentParser = new AssignmentParser();
const santaService = new SecretSantaService();
const exportService = new ExportService();
const validator = new AssignmentInputValidator();

let mongoService = null;

function setMongoService(service) {
  mongoService = service;
}

function getYear() {
  return new Date().getFullYear();
}

router.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

router.post('/assignments/generate', upload.fields([
  { name: 'employees_file', maxCount: 1 },
  { name: 'previous_file', maxCount: 1 }
]), async (req, res) => {
  try {
    if (!req.files || !req.files.employees_file) {
      return res.status(400).json({ error: 'employees_file is required' });
    }

    const empFile = req.files.employees_file[0];
    const year = req.body.year ? parseInt(req.body.year) : getYear();
    const fmt = (req.body.format || 'json').toLowerCase();

    const tmpPath = path.join(os.tmpdir(), `employees_${year}${path.extname(empFile.originalname)}`);
    fs.renameSync(empFile.path, tmpPath);

    let employees;
    try {
      employees = employeeParser.parseFile(tmpPath);
    } catch (e) {
      return res.status(422).json({ error: e.message });
    }

    let previousAssignments = null;
    if (req.files && req.files.previous_file) {
      const prevFile = req.files.previous_file[0];
      const prevPath = path.join(os.tmpdir(), `previous_${year}.csv`);
      fs.renameSync(prevFile.path, prevPath);
      try {
        previousAssignments = assignmentParser.parseFile(prevPath);
      } catch (e) {
        return res.status(422).json({ error: `Previous file error: ${e.message}` });
      }
    }

    const errors = validator.validate(employees, previousAssignments);
    if (errors.length > 0) {
      return res.status(422).json({ errors });
    }

    let assignments;
    try {
      assignments = santaService.generate(employees, previousAssignments);
    } catch (e) {
      if (e instanceof AssignmentError) {
        return res.status(500).json({ error: e.message });
      }
      throw e;
    }

    let docId = null;
    if (mongoService && mongoService.isConnected()) {
      try {
        docId = await mongoService.saveAssignments(assignments, year);
      } catch (e) {
        console.warn('MongoDB save failed:', e.message);
      }
    }

    if (fmt === 'csv') {
      const csvStr = exportService.toCsvSync(assignments);
      res.setHeader('Content-Type', 'text/csv');
      res.setHeader('Content-Disposition', `attachment; filename=secret_santa_${year}.csv`);
      return res.send(csvStr);
    }

    if (fmt === 'xml') {
      const xmlStr = exportService.toXml(assignments);
      res.setHeader('Content-Type', 'application/xml');
      return res.send(xmlStr);
    }

    res.json({
      year,
      total: assignments.length,
      mongo_id: docId,
      assignments: assignments.map(a => a.toDict())
    });
  } catch (e) {
    console.error('Generate error:', e);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/assignments/years', async (req, res) => {
  if (!mongoService || !mongoService.isConnected()) {
    return res.status(503).json({ error: 'MongoDB not configured' });
  }

  try {
    const years = await mongoService.listYears();
    res.json({ years });
  } catch (e) {
    console.error('List years error:', e);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/assignments/:year', async (req, res) => {
  try {
    const year = parseInt(req.params.year);

    if (!mongoService || !mongoService.isConnected()) {
      return res.status(503).json({ error: 'MongoDB not configured' });
    }

    const assignments = await mongoService.getAssignmentsByYear(year);
    if (!assignments) {
      return res.status(404).json({ error: `No assignments found for year ${year}` });
    }

    const fmt = (req.query.format || 'json').toLowerCase();
    if (fmt === 'csv') {
      const csvStr = exportService.toCsvSync(assignments);
      res.setHeader('Content-Type', 'text/csv');
      return res.send(csvStr);
    }
    if (fmt === 'xml') {
      const xmlStr = exportService.toXml(assignments);
      res.setHeader('Content-Type', 'application/xml');
      return res.send(xmlStr);
    }

    res.json({
      year,
      total: assignments.length,
      assignments: assignments.map(a => a.toDict())
    });
  } catch (e) {
    console.error('Get assignments error:', e);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
module.exports.setMongoService = setMongoService;
