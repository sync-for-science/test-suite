var _ = require('underscore');

module.exports = function(event) {
  var errors = [];
  // Deep-clone the event plan
  var summary = JSON.parse(JSON.stringify(event.plan));

  summary.forEach(function(f, i){
    // Plan and snapshot offsets may not match, get the correct key
    var fkey = _.findKey(event.snapshot, function (feature) {
      return feature.location === f.location;
    });

    f.scenarios.forEach(function(s, j) {
      s.status = 'pending';
      if (fkey && fkey < event.snapshot.length) {
        if (event.snapshot[fkey].status === 'skipped') {
          s.status = 'skipped';
          return;
        }
        if (j < event.snapshot[fkey].elements.length) {
          s.status = 'passed';
          event.snapshot[fkey].elements[j].steps.forEach(function(r) {
            if (r.result && r.result.status === 'failed') {
              s.status = 'failed';
              errors.push(s);
            }
            // This happens if a step does not have a definition
            if (r.result && r.result.status === 'undefined') {
              s.status = 'skipped';
            }
            // Skipped steps should mark scenarios as skipped
            if (r.result && r.result.status === 'skipped') {
              s.status = 'skipped';
            }
          });
        }
      }
    })
  });

  return {
    summary: summary,
    errors: errors
  };
};

