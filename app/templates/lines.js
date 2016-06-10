var Handlebars = require('handlebars');

module.exports = function (message) {
  if (typeof message === 'string') {
    return [message];
  } else {
    return message;
  }
};
