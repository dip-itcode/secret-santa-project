const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

class EmployeeParser {
  constructor() {
    this.REQUIRED_COLS = new Set(['Employee_Name', 'Employee_EmailID']);
  }

  parseFile(filepath) {
    if (!fs.existsSync(filepath)) {
      throw new Error(`File not found: ${filepath}`);
    }

    const ext = path.extname(filepath).toLowerCase();
    if (ext === '.xlsx' || ext === '.xlsm' || ext === '.xls') {
      return this._parseExcel(filepath);
    }
    if (ext === '.csv' || ext === '.tsv') {
      return this._parseCsv(filepath);
    }
    throw new Error(`Unsupported file format: ${ext}`);
  }

  _parseCsv(filepath) {
    const workbook = XLSX.readFile(filepath);
    const sheetName = workbook.SheetNames[0];
    const df = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
    return this._toEmployees(df);
  }

  _parseExcel(filepath) {
    const workbook = XLSX.readFile(filepath);
    const sheetName = workbook.SheetNames[0];
    const df = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
    return this._toEmployees(df);
  }

  _toEmployees(df) {
    const columns = new Set(Object.keys(df[0] || {}));
    const missing = [...this.REQUIRED_COLS].filter(c => !columns.has(c));
    if (missing.length > 0) {
      throw new Error(`Missing required columns: ${missing.join(', ')}`);
    }

    const { Employee } = require('../models/employee');
    return df
      .filter(row => row.Employee_Name && row.Employee_EmailID)
      .map(row => new Employee({
        name: String(row.Employee_Name),
        email: String(row.Employee_EmailID)
      }));
  }
}

class AssignmentParser {
  constructor() {
    this.REQUIRED_COLS = new Set([
      'Employee_Name', 'Employee_EmailID',
      'Secret_Child_Name', 'Secret_Child_EmailID'
    ]);
  }

  parseFile(filepath) {
    if (!fs.existsSync(filepath)) {
      throw new Error(`File not found: ${filepath}`);
    }

    const ext = path.extname(filepath).toLowerCase();
    let df;
    if (ext === '.xlsx' || ext === '.xlsm' || ext === '.xls') {
      const workbook = XLSX.readFile(filepath);
      const sheetName = workbook.SheetNames[0];
      df = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
    } else {
      const workbook = XLSX.readFile(filepath);
      const sheetName = workbook.SheetNames[0];
      df = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
    }

    const columns = new Set(Object.keys(df[0] || {}));
    const missing = [...this.REQUIRED_COLS].filter(c => !columns.has(c));
    if (missing.length > 0) {
      throw new Error(`Missing required columns: ${missing.join(', ')}`);
    }

    const { Assignment, Employee } = require('../models/employee');
    return df
      .filter(row => row.Employee_Name && row.Employee_EmailID &&
                     row.Secret_Child_Name && row.Secret_Child_EmailID)
      .map(row => new Assignment({
        giver: new Employee({
          name: String(row.Employee_Name),
          email: String(row.Employee_EmailID)
        }),
        receiver: new Employee({
          name: String(row.Secret_Child_Name),
          email: String(row.Secret_Child_EmailID)
        })
      }));
  }
}

module.exports = { EmployeeParser, AssignmentParser };
