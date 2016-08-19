var _ = require('underscore');

function scenarioGroup(scenario) {
  if (scenario.skip_reason) {
    return 'skipped';
  }

  return _.reduce(scenario.steps, function (memo, step) {
    if (['failed', 'warning'].indexOf(memo) !== -1) {
      return memo;
    }
    if (step.result && step.result.status === 'failed') {
      if (scenario.tags.indexOf('warning') !== -1) {
        return 'warning';
      } else {
        return 'failed';
      }
    }
    if (typeof step.result === 'undefined') {
      return 'skipped';
    }
    return memo;
  }, 'passed');
}

function stepGroup(step) {
  return (step.result && step.result.status) || 'skipped';
}

module.exports = function (features) {
  var defaults = {passed: [], failed: [], skipped: []};
  var scenarios = _.flatten(_.pluck(features, 'elements'));
  var steps = _.flatten(_.pluck(scenarios, 'steps'));

  return {
    features: _.defaults(_.groupBy(features, 'status'), defaults),
    scenarios: _.defaults(_.groupBy(scenarios, scenarioGroup), defaults, {warning: []}),
    steps: _.defaults(_.groupBy(steps, stepGroup), defaults)
  };
};
