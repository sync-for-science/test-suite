require('expose?$!expose?jQuery!jquery');

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

  socket.on('global_error', function (error) {
    // If this happened before any tests were shown, get rid of the loading animation
    $('#canvas .loading').remove();
    // Alert the user to the global error
    $('#canvas').prepend(error_tmpl({
      'responseText': error.replace(/\n/g, '<br>\n')
    }));
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
  socket.on('reconnect', function () {
    $('#status .alert').alert('close');
  });

  $('#run-tests').on('click', function (event) {
    var vendor = $('#vendor').val();
    var tags = $('input[name="tags"]:checked').map(function () {
      return $(this).val();
    }).get();
    var override = $('#config-override').val();

    errorNavigation.reset();

    $(event.currentTarget).prop('disabled', true);
    socket.emit('begin_tests', {
      vendor: vendor,
      tags: tags,
      override: override
    });

    $('#summary').html("");
    $('#canvas').html(loading_tmpl({}));
  });

  /**
   * Summary links may refer to elements that are collapsed.
   * Make sure they are open before following them.
   *
   * Note: do not preventDefault because we do want to follow the link.
   */
  $('#summary').on('click', 'a[data-target]', function (event) {
    var $el = $(event.currentTarget);

    $($el.data('target')).collapse('show');
  });

  /**
   * Add toggle behavior to tags.
   */
  $('#tags').on('change', ':checkbox', function (event) {
    var $el = $(event.currentTarget);
    var checked = $el.is(':checked');

    if (checked) {
      $el.parent().addClass('label-info').removeClass('label-empty');
    } else {
      $el.parent().addClass('label-empty').removeClass('label-info');
    }
  });
  $('#toggle-all-tags').on('click', function (event) {
    $('#tags').find('.label-empty').click();
  });
  $('#toggle-none-tags').on('click', function (event) {
    $('#tags').find('.label-info').click();
  });
});
