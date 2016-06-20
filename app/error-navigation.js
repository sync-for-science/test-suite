var dashify = require('./templates/dashify.js');
var $ = require('jquery');

var errorNavigation;

function resetErrorNavigation(){
  errorNavigation = {
    index: 0,
    errors: []
  }
};
resetErrorNavigation();

function registerErrors(elist){
  errorNavigation.errors = elist;
}

function scrollToError(){
    $("#"+dashify(errorNavigation.errors[errorNavigation.index].location))[0]
    .scrollIntoView();
}

function moveError(by){
  var i = errorNavigation.index;
  var len = errorNavigation.errors.length;
  var next = (((i + by) % len) + len) % len; // ensure positive, bounded

  errorNavigation.index = next;
  scrollToError();
}

document.addEventListener("keydown", function(e){
  if (e.keyCode === 78) {
    moveError(1);
  }
  if (e.keyCode === 80) {
    moveError(-1);
  }


}, false);


module.exports = {
  move: moveError,
  reset: resetErrorNavigation,
  register: registerErrors
}
