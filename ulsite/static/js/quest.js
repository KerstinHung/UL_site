document.addEventListener("DOMContentLoaded", () => {
  const rows = Array.from(document.querySelectorAll("table.searchtime tbody tr"));

  // checkbox elements (確保 template 有 id)
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
    // 目前被選取的 region（li.checked）
    const selectedRegions = lis.filter(li => li.classList.contains("checked"))
                              .map(li => li.dataset.region);

    rows.forEach(row => {
      const region = row.dataset.region;
      // 如果沒有選任何 region，視為不顯示（如你之前想要的行為）
      const regionMatch = selectedRegions.length > 0 && selectedRegions.includes(region);
      if (!regionMatch) {
        row.style.display = "none";
        return;
      }

      let show = true;

      // m1 條件：m1 checkbox 被勾選時，至少要有 m1 或 iron 或 memory > 0
      if (cb.m1 && cb.m1.checked) {
        const ok = toNum(row.dataset.m1) > 0 || toNum(row.dataset.iron) > 0 || toNum(row.dataset.memory) > 0;
        if (!ok) show = false;
      }

      // m2 條件：m2 或 bronze 或 time
      if (cb.m2 && cb.m2.checked) {
        const ok = toNum(row.dataset.m2) > 0 || toNum(row.dataset.bronze) > 0 || toNum(row.dataset.time) > 0;
        if (!ok) show = false;
      }

      // m3 條件：m3 或 silver 或 soul
      if (cb.m3 && cb.m3.checked) {
        const ok = toNum(row.dataset.m3) > 0 || toNum(row.dataset.silver) > 0 || toNum(row.dataset.soul) > 0;
        if (!ok) show = false;
      }

      // gold 條件：gold 或 light
      if(cb.gold && cb.gold.checked) {
        const ok = toNum(row.dataset.gold) > 0 || toNum(row.dataset.light) > 0
        if (!ok) show = false;
      }

      // platinum 條件：platinum 或 unlight
      if(cb.platinum && cb.platinum.checked) {
        const ok = toNum(row.dataset.platinum) > 0 || toNum(row.dataset.unlight) > 0
        if (!ok) show = false;
      }

      // boss: checkbox 勾選時，要求 row.dataset.boss 為 true (1)
      if (cb.boss && cb.boss.checked) {
        if (!isTrueStr(row.dataset.boss)) show = false;
      }

      // treasure 同理
      if (cb.treasure && cb.treasure.checked) {
        if (!isTrueStr(row.dataset.treasure)) show = false;
      }

      row.style.display = show ? "" : "none";
    });
  }

  // 綁定 li click（你原本 toggle checked 的地方）
  lis.forEach(li => {
    li.addEventListener("click", (e) => {
      li.classList.toggle("checked");
      applyFilters();
    });
  });

  // h2 點整個區塊全選 / 取消全選（如你原本的行為）
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

  // checkbox 改變時也套用
  Object.values(cb).forEach(ch => {
    if (ch) ch.addEventListener("change", applyFilters);
  });

  // initial
  applyFilters();
});