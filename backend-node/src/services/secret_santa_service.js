const { Assignment } = require('../models/employee');

class AssignmentError extends Error {
  constructor(message) {
    super(message);
    this.name = 'AssignmentError';
  }
}

class SecretSantaService {
  constructor() {
    this.MAX_RETRIES = 1000;
  }

  generate(employees, previousAssignments = null) {
    if (employees.length < 2) {
      throw new AssignmentError('Need at least 2 employees for Secret Santa.');
    }

    const previousMap = {};
    if (previousAssignments) {
      for (const a of previousAssignments) {
        previousMap[a.giver.email] = a.receiver.email;
      }
    }

    for (let attempt = 0; attempt < this.MAX_RETRIES; attempt++) {
      const result = this._tryAssign(employees, previousMap);
      if (result !== null) {
        return result;
      }
    }

    throw new AssignmentError(
      `Could not generate a valid Secret Santa assignment after ${this.MAX_RETRIES} attempts. Check for constraint conflicts.`
    );
  }

  _tryAssign(employees, previousMap) {
    const givers = [...employees];
    const receivers = this._shuffle([...employees]);

    const assignments = [];
    for (let i = 0; i < givers.length; i++) {
      const giver = givers[i];
      const receiver = receivers[i];
      if (!this._isValidPair(giver, receiver, previousMap)) {
        return null;
      }
      assignments.push(new Assignment({ giver, receiver }));
    }

    return assignments;
  }

  _isValidPair(giver, receiver, previousMap) {
    if (giver.email === receiver.email) {
      return false;
    }
    if (previousMap[giver.email] === receiver.email) {
      return false;
    }
    return true;
  }

  _shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }
}

module.exports = { SecretSantaService, AssignmentError };
