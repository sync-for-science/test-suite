var _ = require('underscore');

module.exports = function (options) {
  var passed = _.every(this.steps, function (step) {
    return step.result.status === 'passed';
  });

  if (passed) {
    return options.fn(this);
  } else {
    return options.inverse(this);
  }
};
