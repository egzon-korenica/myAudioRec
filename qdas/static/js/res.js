var tables = document.getElementsByTagName('td');

colors = { "sadness": 'blue', "anger": 'red', "fear": 'green', "joy": 'purple', 'disgust': 'yellow'}

for(var i = 0; i < tables.length; i++)
{
  for (var key of Object.keys(keywords)) {
    var s = tables[i].innerHTML;
    while (s.includes(key)) {
      s = s.replace(key, '<span style="color:' + colors[keywords[key]] + '; font-weight:bold">KEY_PLACEHOLDER</span>');
    }
    while (s.includes("KEY_PLACEHOLDER")) {
      s = s.replace("KEY_PLACEHOLDER", key);
    }
    tables[i].innerHTML = s;
  }
}
