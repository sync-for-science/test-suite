var Handlebars = require('handlebars');

module.exports = function (message, count) {
  if (typeof message === 'string') {
    return [message].slice(0, count);
  } else {
    return message.slice(0, count);
  }
};
