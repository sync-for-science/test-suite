var Handlebars = require('handlebars');

var passed = '<span class="glyphicon glyphicon-ok"></span>';
var failed = '<span class="glyphicon glyphicon-remove"></span>';
var skipped = '<small>skipped</small>';

module.exports = function (status) {
  switch (status) {
    case 'passed':
      return new Handlebars.SafeString(passed);
    case 'failed':
      return new Handlebars.SafeString(failed);
    case 'skipped':
      return new Handlebars.SafeString(skipped);
  }
};
