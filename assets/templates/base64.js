var Handlebars = require('handlebars');

module.exports = function (message) {
  try {
    return btoa(message);
  } catch (e) {
    return btoa(unescape(encodeURIComponent(message)));
  }
};
