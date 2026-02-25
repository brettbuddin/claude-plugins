(function() {
  var last = null;
  setInterval(async function() {
    try {
      var r = await fetch('/mtime-dir');
      var t = await r.text();
      if (last !== null && t !== last) {
        var r2 = await fetch('/');
        var h = await r2.text();
        var d = new DOMParser().parseFromString(h, 'text/html');
        document.body.innerHTML = d.body.innerHTML;
      }
      last = t;
    } catch(e) {}
  }, 2000);
})();
