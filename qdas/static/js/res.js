var tables = document.getElementsByTagName('td');

colors = ['blue', 'red', 'green', 'pink', 'yellow']

for(var i = 0; i < tables.length; i++)
{
  for (var key of Object.keys(keywords)) {
      switch (keywords[key]) {
        case 'anger':
          var s = tables[i].innerHTML;
          s = s.replace(key, '<span style="color:green; font-weight:bold">' + key + '</span>');
          tables[i].innerHTML = s;
          break;
        case 'sadness':
          var s = tables[i].innerHTML;
          s = s.replace(key, '<span style="color:blue; font-weight:bold">' + key + '</span>');
          tables[i].innerHTML = s;
          break;
        case 'fear':
          var s = tables[i].innerHTML;
          s = s.replace(key, '<span style="color:red; font-weight:bold">' + key + '</span>');
          tables[i].innerHTML = s;
          break;
        case 'disgust':
          var s = tables[i].innerHTML;
          s = s.replace(key, '<span style="color:yellow; font-weight:bold">' + key + '</span>');
          tables[i].innerHTML = s;
          break;
        case 'joy':
          var s = tables[i].innerHTML;
          s = s.replace(key, '<span style="color:purple; font-weight:bold">' + key + '</span>');
          tables[i].innerHTML = s;
          break;
      default:
          console.log("Nothing was paassed");
      }
  }

}
