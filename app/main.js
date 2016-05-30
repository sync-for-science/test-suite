var $ = require('jquery');
var features_tmpl = require('./templates/features.hbs');
var loading_tmpl = require('./templates/loading.hbs');
var error_tmpl = require('./templates/error.hbs');
require('./styles.less');
require('bootstrap/dist/js/npm');

$(function () {
  $('#vendor').on('change', function (event) {
    var $el = $(event.currentTarget);
    var $option = $el.find(':selected');

    if ($option.data('authorize')) {
      $('#authorize').prop('disabled', false);
    } else {
      $('#authorize').prop('disabled', true);
    }
  }).trigger('change');

  $('#run-tests').on('click', function (event) {
    var vendor = $('#vendor').val();

    $(event.currentTarget).prop('disabled', true);

    $.post('/tests.json', {vendor: vendor})
    .done(function (data) {
      $('#canvas')
        .html(features_tmpl({features: data}))
        .find('[data-toggle="tooltip"]').tooltip();
    })
    .fail(function (error) {
      $('#canvas').html(error_tmpl(error));
    })
    .always(function () {
      $(event.currentTarget).prop('disabled', false);
    });

    $('#canvas').html(loading_tmpl({}));
  });
});
