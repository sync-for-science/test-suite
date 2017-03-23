var Handlebars = require('handlebars');

module.exports = function (message) {
  return btoa(message);
};
