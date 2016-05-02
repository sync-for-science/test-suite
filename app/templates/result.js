var Handlebars = require('handlebars');

module.exports = function (status) {
  var passed = '<span class="glyphicon glyphicon-ok"></span>';
  var failed = '<span class="glyphicon glyphicon-remove"></span>';

  switch (status) {
    case 'passed':
      return new Handlebars.SafeString(passed);
    case 'failed':
      return new Handlebars.SafeString(failed);
  }
};
