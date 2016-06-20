var $ = require('jquery');
var _ = require('underscore');
var summary_tmpl = require('./templates/summary.hbs');
var features_tmpl = require('./templates/features.hbs');
var loading_tmpl = require('./templates/loading.hbs');
var error_tmpl = require('./templates/error.hbs');
var socketio = require('socket.io-client');
var errorNavigation = require('./error-navigation.js');
require('./styles.less');
require('bootstrap/dist/js/npm');


$(function () {
  var socket = socketio.connect(document.location.origin);
  socket.on('connect', function () {
    console.log('connected');
  });
  socket.on('message', function (message) {
    console.log('message', message);
  });

  socket.on('snapshot', function (event) {

    var tmpl_data = {
      features: event.snapshot,
      length: event.plan.length
    }

    $('#canvas')
      .html(features_tmpl(tmpl_data))
      .find('[data-toggle="tooltip"]').tooltip();

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
    })
  errorNavigation.register(errors);

  $('#summary').html(summary_tmpl({summary: summary}))
      .find('[data-toggle="tooltip"]').tooltip();
  });

  socket.on('tests_complete', function () {
    $('#run-tests').prop('disabled', false);
  });
  socket.on('disconnect', function () {
    $('#run-tests').prop('disabled', false);
    $('#status').html(error_tmpl({
      'responseText': 'Disconnected from server.'
    }));
  });

  $('#run-tests').on('click', function (event) {
    var vendor = $('#vendor').val();
    errorNavigation.reset();

    $(event.currentTarget).prop('disabled', true);
    socket.emit('begin_tests', {vendor: vendor})

    $('#summary').html("");
    $('#canvas').html(loading_tmpl({}));
  });
});
