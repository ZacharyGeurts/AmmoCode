/**
 * GitHub Pages — static AmmoCode editor (no loopback API · no Python).
 * Best version: AmmoCode 6.1 editor UI + optional Grok16 local compile.
 */
(function () {
  "use strict";
  var host = String(location.hostname || "");
  var pages =
    /github\.io$/i.test(host) ||
    /[?&]pages=1/.test(location.search) ||
    /[?&]static=1/.test(location.search);
  if (!pages) return;

  window.AmmoCodeG16Config = {
    apiBase: "",
    pagesStatic: true,
    beltProfile: "belt_2_0",
    pkgVersion: "Grok16-16.1.0-hard-pages",
    g16Version: "16.1.0-hard",
    suite: true,
    repo: "https://github.com/ZacharyGeurts/AmmoCode",
    grok16: "https://github.com/ZacharyGeurts/Grok16",
    wiki: "https://github.com/ZacharyGeurts/AmmoCode/wiki",
  };

  document.documentElement.setAttribute("data-ammocode-pages", "1");
  document.documentElement.setAttribute("data-ammocode-version", "6.2.0");
  document.documentElement.setAttribute("data-ammocode-suite", "1");
  document.documentElement.setAttribute("data-ammocode-run-sandbox", "1");
  // Identical to local: suite + sandboxed Run tab (JS/HTML/BASIC)
  window.AmmoCodeG16Config.runSandbox = true;
  window.AmmoCodeG16Config.pagesRunIdentical = true;
})();