var _ = require('underscore');

module.exports = function () {
  var passed = _.every(this.steps, function (step) {
    return step.result && step.result.status === 'passed';
  });

  return passed ? '.' : 'E';
};
