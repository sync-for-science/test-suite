module.exports = function(event) {
  var errors = [];
  var summary = JSON.parse(JSON.stringify(event.plan));
  summary.forEach(function(f, i){
    f.scenarios.forEach(function(s, j){
      s.status = 'pending';
      if (i < event.snapshot.length){
        if (event.snapshot[i].status === 'skipped'){
          s.status = 'skipped';
          return;
        }
        if (j < event.snapshot[i].elements.length){
          s.status = 'passed';
          event.snapshot[i].elements[j].steps.forEach(function(r){
            if (r.result && r.result.status === 'failed'){
              s.status = 'failed';
              errors.push(s);
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

