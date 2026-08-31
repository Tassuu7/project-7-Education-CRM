'use strict';

class Validator {
  static isEmail(email) {
    if (!email || typeof email !== 'string') return false;
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email.toLowerCase());
  }

  static isPhone(phone) {
    if (!phone || typeof phone !== 'string') return false;
    return /^[+0-9\s-()]{7,20}$/.test(phone);
  }

  static isPositiveNumber(num) {
    return typeof num === 'number' && !isNaN(num) && num >= 0;
  }

  static sanitizeString(str) {
    if (typeof str !== 'string') return '';
    return str.trim().replace(/[<>]/g, '');
  }
}

module.exports = Validator;
