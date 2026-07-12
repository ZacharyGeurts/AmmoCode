/**
 * AmmoCode run sandbox host — opens/switches Run tab, posts programs into sandbox.
 * GitHub Pages + local identical: JS/HTML/BASIC run in-browser; systems langs need g16.
 */
(function (global) {
  "use strict";

  const state = {
    frame: null,
    ready: false,
    queue: null,
    view: "editor", // editor | run
  };

  function $(id) {
    return document.getElementById(id);
  }

  function ensureUi() {
    let dock = $("ac-run-dock");
    if (dock) return dock;
    // Inject view switcher into titlebar meta if missing
    const meta = document.querySelector(".ac-titlebar-meta");
    if (meta && !$("ac-view-editor")) {
      const wrap = document.createElement("div");
      wrap.className = "ac-view-switch";
      wrap.setAttribute("role", "tablist");
      wrap.innerHTML =
        '<button type="button" class="ac-view-btn active" id="ac-view-editor" role="tab" aria-selected="true">Editor</button>' +
        '<button type="button" class="ac-view-btn" id="ac-view-run" role="tab" aria-selected="false">Run</button>';
      meta.insertBefore(wrap, meta.firstChild);
      $("ac-view-editor")?.addEventListener("click", () => showView("editor"));
      $("ac-view-run")?.addEventListener("click", () => showView("run"));
    }
    dock = document.createElement("div");
    dock.id = "ac-run-dock";
    dock.className = "ac-run-dock hidden";
    dock.innerHTML =
      '<div class="ac-run-toolbar">' +
      '<span class="ac-run-title">Program run · sandbox</span>' +
      '<button type="button" id="ac-run-stop" class="ac-run-tool">Stop</button>' +
      '<button type="button" id="ac-run-reload" class="ac-run-tool">Reload sandbox</button>' +
      '<button type="button" id="ac-run-back" class="ac-run-tool">← Editor</button>' +
      "</div>" +
      '<iframe id="ac-run-frame" class="ac-run-frame" title="AmmoCode sandboxed run" ' +
      'sandbox="allow-scripts" referrerpolicy="no-referrer"></iframe>';
    const shell = document.querySelector(".ac-shell") || document.body;
    shell.appendChild(dock);
    $("ac-run-stop")?.addEventListener("click", stop);
    $("ac-run-reload")?.addEventListener("click", () => {
      state.ready = false;
      loadFrame();
    });
    $("ac-run-back")?.addEventListener("click", () => showView("editor"));
    loadFrame();
    return dock;
  }

  function loadFrame() {
    const frame = $("ac-run-frame");
    if (!frame) return;
    state.frame = frame;
    state.ready = false;
    frame.onload = function () {
      state.ready = true;
      if (state.queue) {
        const q = state.queue;
        state.queue = null;
        post(q);
      }
    };
    // same-directory run.html — works on Pages and local
    frame.src = "run.html?sandbox=1&t=" + Date.now();
  }

  function showView(which) {
    state.view = which === "run" ? "run" : "editor";
    ensureUi();
    const dock = $("ac-run-dock");
    const main = document.querySelector(".ac-main");
    const langbar = document.querySelector(".ac-langbar");
    const toolbar = document.querySelector(".ac-toolbar-wrap");
    const ed = which === "editor";
    if (dock) dock.classList.toggle("hidden", ed);
    if (main) main.classList.toggle("hidden", !ed);
    if (langbar) langbar.classList.toggle("ac-dim", !ed);
    if (toolbar) toolbar.classList.toggle("ac-dim", !ed);
    $("ac-view-editor")?.classList.toggle("active", ed);
    $("ac-view-run")?.classList.toggle("active", !ed);
    $("ac-view-editor")?.setAttribute("aria-selected", ed ? "true" : "false");
    $("ac-view-run")?.setAttribute("aria-selected", ed ? "false" : "true");
  }

  function post(msg) {
    const frame = state.frame || $("ac-run-frame");
    if (!frame || !frame.contentWindow) return false;
    try {
      frame.contentWindow.postMessage(
        Object.assign({ source: "ammocode-editor" }, msg),
        "*"
      );
      return true;
    } catch (_) {
      return false;
    }
  }

  function canSandbox(lang) {
    const L = String(lang || "").toLowerCase();
    return (
      L === "javascript" ||
      L === "js" ||
      L === "typescript" ||
      L === "html" ||
      L === "htm" ||
      L === "basic" ||
      L === "qbasic" ||
      L === "quickbasic" ||
      L === "freebasic" ||
      L === "vba" ||
      L === "visual_basic" ||
      L === "plaintext"
    );
  }

  function run({ code, language, name, path }) {
    ensureUi();
    showView("run");
    const payload = {
      type: "run",
      code: code || "",
      language: language || "javascript",
      name: name || (path ? String(path).split("/").pop() : "program"),
      path: path || "",
    };
    if (!state.ready) {
      state.queue = payload;
      if (!state.frame || !state.frame.src) loadFrame();
      return { ok: true, queued: true, sandbox: true };
    }
    post(payload);
    return { ok: true, sandbox: true, language: payload.language };
  }

  function stop() {
    post({ type: "stop" });
  }

  window.addEventListener("message", function (ev) {
    const d = ev.data;
    if (!d || d.source !== "ammocode-run-sandbox") return;
    if (d.type === "ready") {
      state.ready = true;
      if (state.queue) {
        const q = state.queue;
        state.queue = null;
        post(q);
      }
    }
    // surface status into editor output if present
    try {
      const out = document.getElementById("ac-output");
      if (out && d.type === "run_done") {
        out.textContent =
          (out.textContent ? out.textContent + "\n" : "") +
          "[sandbox done] " +
          (d.language || "");
      }
      if (out && d.type === "run_needs_g16") {
        out.textContent =
          "[sandbox] " +
          (d.language || "") +
          " needs Grok16 hard for full compile/run · JS/HTML/BASIC run on Pages";
      }
      if (out && d.type === "run_error") {
        out.textContent = "[sandbox error] " + (d.message || "");
        out.className = "ac-output err";
      }
    } catch (_) {}
  });

  global.AmmoCodeRunSandbox = {
    ensureUi,
    showView,
    run,
    stop,
    canSandbox,
    get view() {
      return state.view;
    },
  };
})(typeof window !== "undefined" ? window : globalThis);
