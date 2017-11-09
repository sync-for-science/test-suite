module.exports = function (options) {
  // If the first step of the scenario doesn't have a result, it means the scenario was skipped.
  var skipped = (typeof this.steps[0].result == 'undefined');

  if (skipped) {
    return options.fn(this);
  } else {
    return options.inverse(this);
  }
};
