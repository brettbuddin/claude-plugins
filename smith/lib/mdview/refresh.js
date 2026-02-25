(function() {
  var file = FILE_PLACEHOLDER;
  var last = null;
  setInterval(async function() {
    try {
      var r = await fetch('/mtime/' + encodeURIComponent(file));
      var t = await r.text();
      if (last !== null && t !== last) {
        var r2 = await fetch(location.href);
        var h = await r2.text();
        var d = new DOMParser().parseFromString(h, 'text/html');
        document.body.innerHTML = d.body.innerHTML;
        if (document.querySelector('.mermaid')) {
          import('https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs')
            .then(m => m.default.run());
        }
      }
      last = t;
    } catch(e) {}
  }, 1000);
})();
