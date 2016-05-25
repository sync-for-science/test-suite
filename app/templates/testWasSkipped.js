module.exports = function (options) {
  var passed = this.status === 'skipped';

  if (passed) {
    return options.fn(this);
  } else {
    return options.inverse(this);
  }
};
