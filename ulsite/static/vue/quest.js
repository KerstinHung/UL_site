const vueApp = Vue.createApp({
  data() {
    return {
      // 所有選中的地區
      regions: {},

      // checkbox 狀態
      filters: {
        m1: false,
        m2: false,
        m3: false,
        gold: false,
        platinum: false,
        boss: false,
        treasure: false,
      }
    };
  },

  mounted() {
    // 初始化將所有 region 設定為 false
    document.querySelectorAll(".region_container li").forEach(li => {
      this.regions[li.dataset.region] = false;
    });
  },

  methods: {

    toggleRegion(name) {
      this.regions[name] = !this.regions[name];
    },

    toggleGroup(event) {
      const container = event.target.closest("div");
      const items = container.querySelectorAll("li");

      const allChecked = Array.from(items).every(li => this.regions[li.dataset.region]);

      items.forEach(li => {
        this.regions[li.dataset.region] = !allChecked;
      });
    },

    toNum(v) { return Number(v || 0); },
    isTrue(v) { return v === "1" || v === "True" || v === "true"; },

    shouldShow(row) {
      const selected = Object.keys(this.regions).filter(r => this.regions[r]);

      // 若沒選地區 → 全部隱藏
      if (selected.length === 0 || !selected.includes(row.region))
        return false;

      // --- M 類 ---
      if (this.filters.m1 &&
          !(this.toNum(row.m1) > 0 ||
            this.toNum(row.iron) > 0 ||
            this.toNum(row.memory) > 0))
        return false;

      if (this.filters.m2 &&
          !(this.toNum(row.m2) > 0 ||
            this.toNum(row.bronze) > 0 ||
            this.toNum(row.time) > 0))
        return false;

      if (this.filters.m3 &&
          !(this.toNum(row.m3) > 0 ||
            this.toNum(row.silver) > 0 ||
            this.toNum(row.soul) > 0))
        return false;

      // 金幣
      if (this.filters.gold &&
          !(this.toNum(row.gold) > 0 ||
            this.toNum(row.light) > 0))
        return false;

      // 白金幣
      if (this.filters.platinum &&
          !(this.toNum(row.platinum) > 0 ||
            this.toNum(row.unlight) > 0))
        return false;

      // boss/treasure
      if (this.filters.boss && !this.isTrue(row.boss))
        return false;

      if (this.filters.treasure && !this.isTrue(row.treasure))
        return false;

      return true;
    }
  }
});

vueApp.mount("#vueApp");
