(function () {
  function update() {
    document.querySelectorAll(".table-wrapper").forEach(function (w) {
      w.classList.remove("wide");
      if (w.scrollWidth > w.clientWidth) {
        w.classList.add("wide");
      }
    });
  }
  update();
  window.addEventListener("resize", update);
})();
