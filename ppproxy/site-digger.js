url = 'http://www.site-digger.com/html/articles/20110516/proxieslist.html'

var page = require('webpage').create();
page.open(url, function(status) {
  var title = page.evaluate(function() {
    return document.title;
  });
  if(status != 'success'){
    console.log(status);
  }
  var regex = /\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}:\d+/g;
  console.log(page.plainText);
  // console.log(regex.exec(page.plainText))
  
  /* var matches = [], found;
   * while (found = regex.exec(page.plainText)) {
   *   console.log(found)
   *   matches.push(found[0]);
   *   // regex.lastIndex -= found[0].split(':')[1].length;
   *   console.log(regex.lastIndex);
   *   regex.lastIndex -= found[0].length;
   * }
   * console.log(matches); */

  phantom.exit();
});

