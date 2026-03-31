const { MongoClient } = require('mongodb');

class MongoService {
  constructor(uri, dbName = 'secret_santa') {
    this.uri = uri;
    this.dbName = dbName;
    this.client = null;
    this.db = null;
    this.assignments = null;
  }

  async connect() {
    try {
      this.client = new MongoClient(this.uri, {
        serverSelectionTimeoutMS: 5000
      });
      await this.client.connect();
      this.db = this.client.db(this.dbName);
      this.assignments = this.db.collection('assignments');
      await this.client.db('admin').command({ ping: 1 });
      return true;
    } catch (err) {
      console.warn(`MongoDB init failed: ${err.message}`);
      return false;
    }
  }

  isConnected() {
    return this.client !== null && this.assignments !== null;
  }

  async saveAssignments(assignments, year) {
    if (!this.isConnected()) {
      throw new Error('MongoDB not connected');
    }

    const doc = {
      year,
      created_at: new Date().toISOString(),
      assignments: assignments.map(a => a.toDict())
    };

    const result = await this.assignments.insertOne(doc);
    return result.insertedId.toString();
  }

  async getAssignmentsByYear(year) {
    if (!this.isConnected()) {
      throw new Error('MongoDB not connected');
    }

    const doc = await this.assignments
      .find({ year })
      .sort({ created_at: -1 })
      .limit(1)
      .toArray();

    if (!doc.length) {
      return null;
    }

    const { Employee, Assignment } = require('../models/employee');
    return doc[0].assignments.map(a => {
      return new Assignment({
        giver: new Employee({ name: a.Employee_Name, email: a.Employee_EmailID }),
        receiver: new Employee({ name: a.Secret_Child_Name, email: a.Secret_Child_EmailID })
      });
    });
  }

  async listYears() {
    if (!this.isConnected()) {
      throw new Error('MongoDB not connected');
    }

    const years = await this.assignments.distinct('year');
    return years.sort((a, b) => a - b);
  }

  async close() {
    if (this.client) {
      await this.client.close();
    }
  }
}

module.exports = { MongoService };
