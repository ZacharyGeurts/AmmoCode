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
    pkgVersion: "AmmoCode-6.1.0-pages",
    g16Version: "16.2.0-pages-static",
    repo: "https://github.com/ZacharyGeurts/AmmoCode",
    wiki: "https://github.com/ZacharyGeurts/AmmoCode/wiki",
  };

  document.documentElement.setAttribute("data-ammocode-pages", "1");
  document.documentElement.setAttribute("data-ammocode-version", "6.1.0");
})();