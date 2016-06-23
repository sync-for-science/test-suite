var $ = require('jquery');
var _ = require('underscore');
var uuid = require('uuid');
var socketio = require('socket.io-client');

var summary_tmpl = require('./templates/summary.hbs');
var features_tmpl = require('./templates/features.hbs');
var loading_tmpl = require('./templates/loading.hbs');
var error_tmpl = require('./templates/error.hbs');
var errorNavigation = require('./error-navigation.js');
var summarize = require('./summarize.js');

require('./styles.less');
require('bootstrap/dist/js/npm');


$(function () {
  var socket = socketio.connect(document.location.origin);
  var room = uuid.v4();

  socket.on('connect', function () {
    console.log('connected');
    socket.emit('join', room);
  });
  socket.on('message', function (message) {
    console.log('message', message);
  });

  socket.on('snapshot', function (event) {

    var tmpl_data = {
      features: event.snapshot,
      length: event.plan.length
    }
    var summaryResult = summarize(event);

    errorNavigation.register(summaryResult.errors);

    // Remove any lingering tooltips when redrawing the page
    $('.tooltip').tooltip('destroy');

    $('#canvas')
      .html(features_tmpl(tmpl_data))
      .find('[data-toggle="tooltip"]').tooltip();

    $('#summary')
      .html(summary_tmpl({summary: summaryResult.summary}))
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
    socket.emit('begin_tests', {vendor: vendor});

    $('#summary').html("");
    $('#canvas').html(loading_tmpl({}));
  });
});
