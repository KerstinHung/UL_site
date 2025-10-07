document.addEventListener("DOMContentLoaded", () => {
  const rows = Array.from(document.querySelectorAll("table.searchtime tbody tr"));

  // checkbox elements (Ensure template has id)
  const cb = {
    m1: document.getElementById("filter-m1"),
    m2: document.getElementById("filter-m2"),
    m3: document.getElementById("filter-m3"),
    gold: document.getElementById("filter-gold"),
    platinum: document.getElementById("filter-platinum"),
    boss: document.getElementById("filter-boss"),
    treasure: document.getElementById("filter-treasure"),
  };

  const lis = Array.from(document.querySelectorAll("ul li"));

  function toNum(v){ return Number(v || 0); }
  function isTrueStr(v){ return v === "1" || v === "True" || v === "true"; }

  function applyFilters(){
    // Currently selected regions（li.checked）
    const selectedRegions = lis.filter(li => li.classList.contains("checked"))
                              .map(li => li.dataset.region);

    rows.forEach(row => {
      const region = row.dataset.region;
      // If not select any region, redard as invisible
      const regionMatch = selectedRegions.length > 0 && selectedRegions.includes(region);
      if (!regionMatch) {
        row.style.display = "none";
        return;
      }

      let show = true;

      // m1: When m1 checkbox is checked, at least m1 or iron or memory > 0
      if (cb.m1 && cb.m1.checked) {
        const ok = toNum(row.dataset.m1) > 0 || toNum(row.dataset.iron) > 0 || toNum(row.dataset.memory) > 0;
        if (!ok) show = false;
      }

      // m2: at least m2 or bronze or time
      if (cb.m2 && cb.m2.checked) {
        const ok = toNum(row.dataset.m2) > 0 || toNum(row.dataset.bronze) > 0 || toNum(row.dataset.time) > 0;
        if (!ok) show = false;
      }

      // m3 at least m3 or silver or soul
      if (cb.m3 && cb.m3.checked) {
        const ok = toNum(row.dataset.m3) > 0 || toNum(row.dataset.silver) > 0 || toNum(row.dataset.soul) > 0;
        if (!ok) show = false;
      }

      // gold: gold or light
      if(cb.gold && cb.gold.checked) {
        const ok = toNum(row.dataset.gold) > 0 || toNum(row.dataset.light) > 0
        if (!ok) show = false;
      }

      // platinum: platinum or unlight
      if(cb.platinum && cb.platinum.checked) {
        const ok = toNum(row.dataset.platinum) > 0 || toNum(row.dataset.unlight) > 0
        if (!ok) show = false;
      }

      // boss: When checked, require row.dataset.boss is true (1)
      if (cb.boss && cb.boss.checked) {
        if (!isTrueStr(row.dataset.boss)) show = false;
      }

      // treasure: same as boss
      if (cb.treasure && cb.treasure.checked) {
        if (!isTrueStr(row.dataset.treasure)) show = false;
      }

      row.style.display = show ? "" : "none";
    });
  }

  // Bind li click
  lis.forEach(li => {
    li.addEventListener("click", (e) => {
      li.classList.toggle("checked");
      applyFilters();
    });
  });

  // h2 for select/unselect all regions
  document.querySelectorAll("h2").forEach(h2 => {
    h2.addEventListener("click", e => {
      const container = h2.closest("div");
      if (!container) return;
      const groupLis = Array.from(container.querySelectorAll("ul li"));
      const allChecked = groupLis.every(x => x.classList.contains("checked"));
      groupLis.forEach(x => x.classList.toggle("checked", !allChecked));
      applyFilters();
    });
  });

  // When checkbox changed, apply
  Object.values(cb).forEach(ch => {
    if (ch) ch.addEventListener("change", applyFilters);
  });

  // initial
  applyFilters();
});