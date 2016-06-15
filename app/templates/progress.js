module.exports = function (status) {
  switch (status) {
    case 'passed':
      return '.';
    case 'failed':
      return 'F';
    case 'skipped':
      return 'S';
    default:
      return '?';
  }
}
