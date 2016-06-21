var dashify = require('./templates/dashify.js');
var $ = require('jquery');

var errorNavigation;

function reset(){
  document.removeEventListener("keydown", onKey, false);
  errorNavigation = {
    index: 0,
    errors: []
  }
  init();
};

function register(elist){
  errorNavigation.errors = elist;
}

function scroll(){
    $("#"+dashify(errorNavigation.errors[errorNavigation.index].location))[0]
    .scrollIntoView();
}

function moveBy(by){
  var i = errorNavigation.index;
  var len = errorNavigation.errors.length;
  var next = (((i + by) % len) + len) % len; // ensure positive, bounded

  errorNavigation.index = next;
  scroll();
}

function onKey(e) {
    if (e.keyCode === 78) {
      moveBy(1);
    }
    if (e.keyCode === 80) {
      moveBy(-1);
    }
  }

function init(){
  document.addEventListener("keydown", onKey, false);
}


module.exports = {
  reset: reset,
  register: register
}
