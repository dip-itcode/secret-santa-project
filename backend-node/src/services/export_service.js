const { XMLBuilder } = require('fast-xml-parser');

class ExportService {
  constructor() {
    this.CSV_FIELDS = [
      'Employee_Name',
      'Employee_EmailID',
      'Secret_Child_Name',
      'Secret_Child_EmailID'
    ];
  }

  toCsvSync(assignments) {
    const rows = assignments.map(a => a.toDict());
    const header = this.CSV_FIELDS.join(',') + '\n';
    const body = rows.map(row => 
      this.CSV_FIELDS.map(field => {
        const val = row[field] || '';
        return val.includes(',') || val.includes('"') 
          ? `"${val.replace(/"/g, '""')}"` 
          : val;
      }).join(',')
    ).join('\n');
    return header + body;
  }

  toXml(assignments) {
    const builder = new XMLBuilder({
      format: true,
      ignoreAttributes: false,
      attributeNamePrefix: ''
    });

    const data = {
      SecretSantaAssignments: {
        Assignment: assignments.map(a => a.toXMLDict())
      }
    };

    return builder.build(data);
  }
}

module.exports = { ExportService };
