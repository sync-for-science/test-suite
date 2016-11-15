var URLSearchParams = require('url-search-params');

module.exports = {
  getReport: function (callback) {
    var params = new URLSearchParams(window.location.search);
    if (params.get('report_id')) {
      callback(params.get('report_id'));
    }
  },

  setReport: function (reportId) {
    var url = '?report_id=' + reportId + window.location.hash;
    window.history.pushState(null, '', url);
  },

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
