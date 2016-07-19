module.exports = {
  save: function(state){
    window.location.hash = JSON.stringify(state);
  },
  load: function(){
    try {
      return JSON.parse(window.location.hash.slice(1));
    } catch (e) {
      return null;
    }
  }
}
