/* Hide/show and drag-to-resize for the left Table of Contents sidebar.
   Both settings are remembered across pages (localStorage). The saved state is
   applied before first paint by the inline script in _templates/layout.html. */
document.addEventListener("DOMContentLoaded", function () {
  var root = document.documentElement;
  var sidebar = document.querySelector(".bd-sidebar-primary");
  var header = document.querySelector(".sidebar-toc-header");
  if (!sidebar || !header) return;

  var MIN_WIDTH = 180;
  var MAX_WIDTH = 600;

  function save(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* storage blocked */ }
  }

  function setHidden(hidden) {
    root.classList.toggle("toc-hidden", hidden);
    save("toc-hidden", hidden ? "1" : "0");
  }

  // "Hide" button in the sidebar header.
  var hideBtn = document.createElement("button");
  hideBtn.type = "button";
  hideBtn.className = "toc-hide-button";
  hideBtn.title = "Hide Table of Contents";
  hideBtn.setAttribute("aria-label", "Hide Table of Contents");
  hideBtn.innerHTML = '<i class="fa-solid fa-angles-left"></i>';
  hideBtn.addEventListener("click", function () { setHidden(true); });
  header.appendChild(hideBtn);

  // "Show" button in the sidebar's place, visible only while it is hidden.
  var showBtn = document.createElement("button");
  showBtn.type = "button";
  showBtn.className = "toc-show-button";
  showBtn.title = "Show Table of Contents";
  showBtn.setAttribute("aria-label", "Show Table of Contents");
  showBtn.innerHTML = '<i class="fa-solid fa-angles-right"></i> Contents';
  showBtn.addEventListener("click", function () { setHidden(false); });
  sidebar.before(showBtn);

  // Drag handle on the sidebar's right edge.
  var handle = document.createElement("div");
  handle.className = "toc-resize-handle";
  handle.title = "Drag to resize, double-click to reset";
  handle.setAttribute("role", "separator");
  handle.setAttribute("aria-orientation", "vertical");
  sidebar.after(handle);

  handle.addEventListener("pointerdown", function (e) {
    e.preventDefault();
    handle.setPointerCapture(e.pointerId);
    root.classList.add("toc-resizing");
    var left = sidebar.getBoundingClientRect().left;

    function onMove(ev) {
      var width = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, ev.clientX - left));
      root.style.setProperty("--toc-width", width + "px");
    }
    function onUp() {
      handle.removeEventListener("pointermove", onMove);
      handle.removeEventListener("pointerup", onUp);
      handle.removeEventListener("pointercancel", onUp);
      root.classList.remove("toc-resizing");
      save("toc-width", root.style.getPropertyValue("--toc-width"));
    }
    handle.addEventListener("pointermove", onMove);
    handle.addEventListener("pointerup", onUp);
    handle.addEventListener("pointercancel", onUp);
  });

  handle.addEventListener("dblclick", function () {
    root.style.removeProperty("--toc-width");
    try { localStorage.removeItem("toc-width"); } catch (e) { /* storage blocked */ }
  });
});
