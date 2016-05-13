var $ = require('jquery');
var features_tmpl = require('./templates/features.hbs');
var loading_tmpl = require('./templates/loading.hbs');
var error_tmpl = require('./templates/error.hbs');
var io = require('socket.io-client');
require('./styles.less');
require('bootstrap/dist/js/npm');


$(function () {
  var socket = io.connect('http://' + document.domain + ':' + location.port);

  socket.on('result', function(status) {
    console.log("Got result snapshot");
    var summary = summarizeStatus(status)
    $('#output').text(JSON.stringify(summary, null, 2))
  });


  $('#run-tests').on('click', function (event) {
    var config = $('#behave-ini').val();
    socket.emit('testme', {
      room: ""+Math.random(),
      ini: config
    });
  });

  function summarizeStatus(status){
    return status.map(function(feature){
      return feature.elements.map(function(scenario){
        return scenario.name + ": " + scenario.steps.map(function(step){
          return step.result && step.result.status === 'passed'  ? 1 : 0
        }).reduce(function(total, step){
          return total+step
        }, 0) + "/" + scenario.steps.length
      })
    })
  }

});
