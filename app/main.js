var $ = require('jquery');
var _ = require('underscore');
var features_tmpl = require('./templates/features.hbs');
var loading_tmpl = require('./templates/loading.hbs');
var error_tmpl = require('./templates/error.hbs');
var socketio = require('socket.io-client');
require('./styles.less');
require('bootstrap/dist/js/npm');

$(function () {
  var socket = socketio.connect('http://' + document.domain + ':' + location.port);
  socket.on('connect', function () {
    console.log('connected');
  });
  socket.on('message', function (message) {
    console.log('message', message);
  });
  socket.on('snapshot', function (snapshot) {
    console.log(snapshot);
    snapshot.reverse();

    $('#canvas')
      .html(features_tmpl({features: snapshot}))
      .find('[data-toggle="tooltip"]').tooltip();
  });
  socket.on('tests_complete', function () {
    $('#run-tests').prop('disabled', false);
  });

  window.socket = socket;

  $('#run-tests').on('click', function (event) {
    var vendor = $('#vendor').val();

    $(event.currentTarget).prop('disabled', true);
    socket.emit('begin_tests', {vendor: vendor})

    $('#canvas').html(loading_tmpl({}));
  });
});
