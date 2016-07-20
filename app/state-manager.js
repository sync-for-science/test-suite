module.exports = {
  save: function(state){
    window.location.hash = JSON.stringify(state);
  },
  load: function(){
    try {
      var h = window.location.hash.slice(1);
      if (h === ""){
        return null;
      }
      if (h.startsWith("%7B")){
        h = decodeURIComponent(h);
      }
      return JSON.parse(h);
    } catch (e) {
      return null;
    }
  }
}
