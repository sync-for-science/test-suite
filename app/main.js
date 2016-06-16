var $ = require('jquery');
var _ = require('underscore');
var features_tmpl = require('./templates/features.hbs');
var loading_tmpl = require('./templates/loading.hbs');
var error_tmpl = require('./templates/error.hbs');
var socketio = require('socket.io-client');
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
  });
  socket.on('tests_complete', function () {
    $('#run-tests').prop('disabled', false);
  });
  socket.on('disconnect', function () {
    $('#run-tests').prop('disabled', false);
    $('#canvas').html(error_tmpl({
      'responseText': '<h1>Disconnected from server.</h1>'
    }));
  });

  $('#run-tests').on('click', function (event) {
    var vendor = $('#vendor').val();

    $(event.currentTarget).prop('disabled', true);
    socket.emit('begin_tests', {vendor: vendor})

    $('#canvas').html(loading_tmpl({}));
  });
});
