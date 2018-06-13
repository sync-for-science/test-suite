var $ = require('jquery');
var _ = require('underscore');
var uuid = require('uuid');
var socketio = require('socket.io-client');
var yaml = require('js-yaml');

var stateManager = require('./state-manager.js');
var summary_tmpl = require('./templates/summary.hbs');
var features_tmpl = require('./templates/features.hbs');
var loading_tmpl = require('./templates/loading.hbs');
var report_tmpl = require('./templates/report.hbs');
var error_tmpl = require('./templates/error.hbs');
var info_tmpl = require('./templates/info.hbs');
var errorNavigation = require('./error-navigation.js');
var summarize = require('./summarize.js');
var report = require('./report.js');

require('./styles.less');
require('bootstrap/dist/js/npm');


$(function () {
  var socket = socketio.connect(document.location.origin);
  var room = uuid.v4();
  var payloads = {};

  socket.on('connect', function () {
    console.log('connected', room);
    socket.emit('join', room);

    // If we're retrieving an old report, start that process
    stateManager.getReport(function (report_id) {
      errorNavigation.reset();
      $.post('/load-report/' + report_id, {room: room});
    });
  });
  socket.on('message', function (message) {
    console.log('message', message);
  });

  socket.on('snapshot', function (event) {

    var tmpl_data = {
      features: event.snapshot,
      length: event.plan.length,
    }
    var summaryResult = summarize(event);

    _.each(tmpl_data.features, function (feature) {
      feature.payloads = payloads[feature.name] || [];
    });

    stateManager.setReport(event.report_id);

    errorNavigation.register(summaryResult.errors);

    // Remove any lingering tooltips when redrawing the page
    $('.tooltip').tooltip('destroy');

    $('#canvas')
      .html(features_tmpl(tmpl_data))
      .find('[data-toggle="tooltip"]').tooltip();

    $('#summary')
      .html(summary_tmpl({summary: summaryResult.summary}))
      .find('[data-toggle="tooltip"]').tooltip();

    var reportResult = {
      report: report(event.snapshot),
      systems: summaryResult.systems,
      url: window.location.href,
    };

    $('#report').html(report_tmpl(reportResult));
  });

  socket.on('payload', function (payload) {
    if (typeof payloads[payload.feature] === 'undefined') {
      payloads[payload.feature] = [];
    }

    payloads[payload.feature].push(payload);
  });

  socket.on('global_error', function (error) {
    // If this happened before any tests were shown, get rid of the loading animation
    $('#canvas .loading').remove();
    // Alert the user to the global error
    $('#canvas').prepend(error_tmpl({
      'responseText': _.escape(error).replace(/\n/g, '<br>\n')
    }));
    $('#report-modal').remove();
  });

  socket.on('tests_complete', function () {
    $('#run-tests').prop('disabled', false);
    $('#report').show();
    $('#report-modal').modal({'show': true});
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

    stateManager.clear();
    stateManager.save({
      vendor: vendor,
      tags: tags,
      override: override
    });

    errorNavigation.reset();

    payloads = {};

    $(event.currentTarget).prop('disabled', true);
    socket.emit('begin_tests', {
      vendor: vendor,
      tags: tags,
      override: override
    });

    $('#summary').html("");
    $('#canvas').html(loading_tmpl({}));
    $('#report').hide();
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

  /**
   * Add YAML validation.
   */
  $('#config-override').on('change keypress keyup', function (event) {
    var $el = $(event.currentTarget);
    var $runBtn = $('#run-tests');
    var $alert = $el.siblings('.alert-danger');
    var config;

    try {
      config = yaml.safeLoad($el.val());
      $alert.addClass('hide');
      $runBtn.prop('disabled', false);
    } catch (err) {
      $alert.removeClass('hide').text(err);
      $runBtn.prop('disabled', true);

      // This can be triggered on page-load with options still hidden
      $el.closest('#more-options').collapse('show');
    }
  });

  $('#toggle-all-tags').on('click', function (event) {
    $('#tags').find('.label-empty').click();
  });
  $('#toggle-none-tags').on('click', function (event) {
    $('#tags').find('.label-info').click();
  });

  $('.container').on('click', '.info-window', function (event) {
    console.log('running');
    var data = $(event.currentTarget).data('info');
    window.open().document.write(info_tmpl({message: atob(data)}));
  });

  var state = stateManager.load();
  if (state) {
    $('#vendor').val(state.vendor)
    $('#config-override').text(state.override).trigger('change');
    $('#tags').find('.label-info').click();
    state.tags.forEach(function(tag){
      $('#tags').find('.label-empty input[value="'+tag+'"]').click();
    })
  }
});
