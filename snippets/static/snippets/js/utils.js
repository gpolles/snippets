
function getFormData(selector){
  var paramObj = {};
  $.each($( selector ).serializeArray(), function(_, kv) {
    if (paramObj.hasOwnProperty(kv.name)) {
      paramObj[kv.name] = $.makeArray(paramObj[kv.name]);
      paramObj[kv.name].push(kv.value);
    }
    else {
      paramObj[kv.name] = kv.value;
    }
  });  
  return paramObj;
}

function formatDate( date ) {
  options = {
    year: 'numeric', 
    month: 'long', 
    day: 'numeric', 
    hour: 'numeric', 
    minute: 'numeric' 
  };
  return date.toLocaleString('en-US', options)
             .replace('AM', 'a.m.')
             .replace('PM', 'p.m.');
}

function stripScripts(s) {
  var div = document.createElement('div');
  div.innerHTML = s;
  var scripts = div.getElementsByTagName('script');
  var i = scripts.length;
  while (i--) {
    scripts[i].parentNode.removeChild(scripts[i]);
  }
  return div.innerHTML;
}