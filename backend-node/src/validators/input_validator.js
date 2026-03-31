const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

class EmployeeValidator {
  validate(employees) {
    const errors = [];

    if (!employees || employees.length === 0) {
      errors.push('Employee list is empty.');
      return errors;
    }

    if (employees.length < 2) {
      errors.push('At least 2 employees are required for Secret Santa.');
    }

    const emailsSeen = new Set();
    for (const emp of employees) {
      if (!emp.name) {
        errors.push(`Employee has an empty name (email: ${emp.email}).`);
      }
      if (!emp.email) {
        errors.push(`Employee '${emp.name}' has an empty email.`);
      } else if (!EMAIL_RE.test(emp.email)) {
        errors.push(`Invalid email format: '${emp.email}' for employee '${emp.name}'.`);
      } else if (emailsSeen.has(emp.email)) {
        errors.push(`Duplicate email detected: '${emp.email}'.`);
      } else {
        emailsSeen.add(emp.email);
      }
    }

    return errors;
  }
}

class AssignmentInputValidator {
  validate(employees, previousAssignments = null) {
    const errors = new EmployeeValidator().validate(employees);
    if (errors.length > 0) {
      return errors;
    }

    return [];
  }
}

module.exports = { EmployeeValidator, AssignmentInputValidator };
