/**
 * AmmoCode language suite — popular-first + A–Z sort · Grok16 compiler map
 * Full suite for 2026+: BASIC, QBasic, modern systems languages, Field.
 */
(function (global) {
  "use strict";

  const state = {
    suite: null,
    sort: "popular", // popular | az
    languages: [],
  };

  function loadLocalSort() {
    try {
      const s = localStorage.getItem("ammocode-lang-sort");
      if (s === "az" || s === "popular") state.sort = s;
    } catch (_) {}
  }

  function saveSort() {
    try {
      localStorage.setItem("ammocode-lang-sort", state.sort);
    } catch (_) {}
  }

  async function loadSuite() {
    loadLocalSort();
    try {
      const r = await fetch("data/ammocode-language-suite.json", { cache: "no-store" });
      if (r.ok) {
        state.suite = await r.json();
        state.languages = Array.isArray(state.suite.languages)
          ? state.suite.languages.slice()
          : [];
        if (state.suite.default_sort === "az" || state.suite.default_sort === "popular") {
          if (!localStorage.getItem("ammocode-lang-sort")) {
            state.sort = state.suite.default_sort;
          }
        }
        return state.suite;
      }
    } catch (_) {}
    state.languages = [
      { id: "python", label: "Python", popularity: 100 },
      { id: "javascript", label: "JavaScript", popularity: 99 },
      { id: "cxx", label: "C++", popularity: 97 },
      { id: "c", label: "C", popularity: 96 },
      { id: "basic", label: "BASIC", popularity: 48 },
      { id: "qbasic", label: "QBasic", popularity: 47 },
      { id: "plaintext", label: "Plain text", popularity: 1 },
    ];
    return { languages: state.languages };
  }

  function sorted() {
    const list = state.languages.slice();
    if (state.sort === "az") {
      list.sort((a, b) =>
        String(a.label || a.id).localeCompare(String(b.label || b.id), undefined, {
          sensitivity: "base",
        })
      );
    } else {
      list.sort(
        (a, b) =>
          (b.popularity || 0) - (a.popularity || 0) ||
          String(a.label || a.id).localeCompare(String(b.label || b.id))
      );
    }
    return list;
  }

  function setSort(mode) {
    if (mode !== "az" && mode !== "popular") return state.sort;
    state.sort = mode;
    saveSort();
    return state.sort;
  }

  function toggleSort() {
    return setSort(state.sort === "popular" ? "az" : "popular");
  }

  function findLang(id) {
    const key = String(id || "").toLowerCase();
    return state.languages.find((l) => l.id === key) || null;
  }

  function labelFor(id) {
    const L = findLang(id);
    return L ? L.label : id || "plaintext";
  }

  function profileFor(id) {
    const L = findLang(id);
    const def =
      (state.suite && state.suite.g16 && state.suite.g16.default_profile) || "belt_2_0";
    return (L && L.profile) || def;
  }

  function fillSelect(sel, currentId) {
    if (!sel) return;
    const list = sorted();
    const cur = String(currentId || "plaintext").toLowerCase();
    sel.innerHTML = "";
    let group = "";
    for (const L of list) {
      // optgroup by sort mode: popular = no groups (flat ranked), az = letter groups optional
      if (state.sort === "az") {
        const letter = String(L.label || L.id)
          .charAt(0)
          .toUpperCase();
        if (letter !== group) {
          group = letter;
          const og = document.createElement("optgroup");
          og.label = letter;
          sel.appendChild(og);
        }
        const parent = sel.lastElementChild;
        const o = document.createElement("option");
        o.value = L.id;
        o.textContent = L.label || L.id;
        if (L.id === cur) o.selected = true;
        (parent && parent.tagName === "OPTGROUP" ? parent : sel).appendChild(o);
      } else {
        const o = document.createElement("option");
        o.value = L.id;
        o.textContent = `${L.label || L.id}`;
        if (L.id === cur) o.selected = true;
        sel.appendChild(o);
      }
    }
    if (cur && !list.some((l) => l.id === cur)) {
      const o = document.createElement("option");
      o.value = cur;
      o.textContent = cur;
      o.selected = true;
      sel.appendChild(o);
    }
  }

  function updateSortButtons() {
    const az = document.getElementById("ac-lang-sort-az");
    const pop = document.getElementById("ac-lang-sort-popular");
    if (az) {
      az.setAttribute("aria-pressed", state.sort === "az" ? "true" : "false");
      az.classList.toggle("active", state.sort === "az");
    }
    if (pop) {
      pop.setAttribute("aria-pressed", state.sort === "popular" ? "true" : "false");
      pop.classList.toggle("active", state.sort === "popular");
    }
  }

  function wire(opts) {
    const sel = document.getElementById("ac-lang-select");
    const az = document.getElementById("ac-lang-sort-az");
    const pop = document.getElementById("ac-lang-sort-popular");
    const onChange = opts && opts.onChange;

    function refresh() {
      fillSelect(sel, opts && opts.getCurrent ? opts.getCurrent() : sel?.value);
      updateSortButtons();
    }

    if (sel) {
      sel.addEventListener("change", () => {
        if (typeof onChange === "function") onChange(sel.value);
      });
    }
    if (az) {
      az.addEventListener("click", () => {
        setSort("az");
        refresh();
      });
    }
    if (pop) {
      pop.addEventListener("click", () => {
        setSort("popular");
        refresh();
      });
    }
    refresh();
    return { refresh, setSort, sorted, labelFor, profileFor, findLang };
  }

  global.AmmoCodeLanguageSuite = {
    loadSuite,
    sorted,
    setSort,
    toggleSort,
    findLang,
    labelFor,
    profileFor,
    fillSelect,
    wire,
    get sort() {
      return state.sort;
    },
    get languages() {
      return state.languages;
    },
    get suite() {
      return state.suite;
    },
  };
})(typeof window !== "undefined" ? window : globalThis);
