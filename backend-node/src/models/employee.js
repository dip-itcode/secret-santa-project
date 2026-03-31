class Employee {
  constructor({ name, email }) {
    this.name = name?.trim() || '';
    this.email = email?.trim().toLowerCase() || '';
  }

  static fromDict(data) {
    return new Employee({
      name: data.Employee_Name,
      email: data.Employee_EmailID
    });
  }

  toDict() {
    return { Employee_Name: this.name, Employee_EmailID: this.email };
  }

  toXMLDict() {
    return this.toDict();
  }

  equals(other) {
    return other instanceof Employee && this.email === other.email;
  }

  hash() {
    return this.email;
  }
}

class Assignment {
  constructor({ giver, receiver }) {
    this.giver = giver;
    this.receiver = receiver;
  }

  static fromDict(data) {
    return new Assignment({
      giver: new Employee({
        name: data.Employee_Name,
        email: data.Employee_EmailID
      }),
      receiver: new Employee({
        name: data.Secret_Child_Name,
        email: data.Secret_Child_EmailID
      })
    });
  }

  toDict() {
    return {
      Employee_Name: this.giver.name,
      Employee_EmailID: this.giver.email,
      Secret_Child_Name: this.receiver.name,
      Secret_Child_EmailID: this.receiver.email
    };
  }

  toXMLDict() {
    return this.toDict();
  }
}

module.exports = { Employee, Assignment };
