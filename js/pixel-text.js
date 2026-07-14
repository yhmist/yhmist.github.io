(function () {
  "use strict";

  function renderGlyph(ch, rows) {
    var charEl = document.createElement("span");
    charEl.className = "px-char";
    charEl.setAttribute("aria-hidden", "true");

    var cols = 0;
    for (var r = 0; r < rows.length; r++) {
      cols = Math.max(cols, rows[r].length);
    }
    charEl.style.setProperty("--cols", String(cols || 1));
    charEl.style.setProperty("--rows", String(rows.length || 1));

    for (var y = 0; y < rows.length; y++) {
      var row = rows[y];
      for (var x = 0; x < row.length; x++) {
        if (row.charAt(x) !== "1") continue;
        var dot = document.createElement("i");
        dot.className = "px-dot";
        dot.style.gridColumn = String(x + 1);
        dot.style.gridRow = String(y + 1);
        charEl.appendChild(dot);
      }
    }

    // Keep layout width even if a glyph is empty.
    if (!charEl.childElementCount) {
      charEl.style.width = "calc(var(--dot) * " + (cols || 1) + ")";
      charEl.style.height = "calc(var(--dot) * " + (rows.length || 1) + ")";
    }

    return charEl;
  }

  function renderText(el) {
    var font = window.PX_FONT;
    if (!font || !font.glyphs) return;

    var text = el.getAttribute("data-px") || "";
    if (!el.getAttribute("aria-label")) {
      el.setAttribute("aria-label", text);
    }

    var frag = document.createDocumentFragment();
    for (var i = 0; i < text.length; i++) {
      var ch = text.charAt(i);
      var rows = font.glyphs[ch];
      if (!rows) {
        // Unknown glyph: reserve a gap so layout does not collapse.
        rows = ["0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000"];
      }
      frag.appendChild(renderGlyph(ch, rows));
    }

    el.textContent = "";
    el.appendChild(frag);
    el.classList.add("px-ready");
  }

  function boot() {
    var nodes = document.querySelectorAll("[data-px]");
    for (var i = 0; i < nodes.length; i++) {
      renderText(nodes[i]);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
