module.exports = function (target) {
  return target.replace(/[^a-zA-Z0-9]+/g, '-').replace(/(^-|-$)/g, '');
};
