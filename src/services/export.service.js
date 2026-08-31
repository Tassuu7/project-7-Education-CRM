'use strict';

/**
 * Data Export & Reporting Service (CSV / JSON / PDF simulation)
 */

const db = require('../../database/db');

class ExportService {
  /**
   * Export table data as CSV string
   */
  exportTableToCSV(tableName) {
    const rows = db.find(tableName);
    if (!rows || rows.length === 0) {
      return 'No data available for export.';
    }

    const headers = Object.keys(rows[0]);
    const csvLines = [headers.join(',')];

    for (const row of rows) {
      const line = headers.map(header => {
        let val = row[header];
        if (val === null || val === undefined) val = '';
        val = String(val).replace(/"/g, '""');
        if (val.includes(',') || val.includes('\n') || val.includes('"')) {
          val = `"${val}"`;
        }
        return val;
      });
      csvLines.push(line.join(','));
    }

    return csvLines.join('\n');
  }

  /**
   * Export table as structured JSON
   */
  exportTableToJSON(tableName) {
    return db.find(tableName);
  }
}

module.exports = new ExportService();
