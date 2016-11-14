module.exports = function (options) {
  var failed = this.status == 'failed';

  if (failed) {
    return options.fn(this);
  } else {
    return options.inverse(this);
  }
};
