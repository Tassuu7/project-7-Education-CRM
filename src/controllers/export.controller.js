'use strict';

const exportService = require('../services/export.service');

class ExportController {
  async exportCSV(req, res) {
    try {
      const tableName = req.params.table;
      const csv = exportService.exportTableToCSV(tableName);
      
      res.setHeader('Content-Type', 'text/csv');
      res.setHeader('Content-Disposition', `attachment; filename="edupulse_${tableName}_${Date.now()}.csv"`);
      return res.status(200).send(csv);
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }

  async exportJSON(req, res) {
    try {
      const tableName = req.params.table;
      const data = exportService.exportTableToJSON(tableName);
      return res.status(200).json({ success: true, table: tableName, data });
    } catch (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
  }
}

module.exports = new ExportController();
