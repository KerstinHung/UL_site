import { test, expect } from "@playwright/test";

test('點擊「死者圖書館」後應顯示死人圖書館1', async ({ page }) => {
  // 1. Open Django webpage
  await page.goto('http://127.0.0.1:8000/quests/');
  // 2. click region
  await page.getByText('死者圖書館', { exact: true }).click();
  // 3. Check table.searchtime displays「死人圖書館1」
  const cell = page.locator('table.searchtime >> text=死人圖書館1');
  // 4. expect element appear
  await expect(cell).toBeVisible();
});

test('點擊 area "HexRealm" 應顯示每個 region 的 quests', async ({ page }) => {
  // 1. Open Django webpage
  await page.goto('http://127.0.0.1:8000/quests/');
  // 2. click region
  await page.getByText('HexRealm', { exact: true }).click();
  // 3. Check table.searchtime displays quests
  const cell1 = page.locator('table.searchtime >> text=無底泥潭');
  const cell2 = page.locator('table.searchtime >> text=山丘矮人');
  const cell3 = page.locator('table.searchtime >> text=落日大蝙蝠');
  // 4. expect element appear
  await expect(cell1).toBeVisible();
  await expect(cell2).toBeVisible();
  await expect(cell3).toBeVisible();
});

test('點擊 area "HexRealm" 再點擊 region 魔女山谷，不應該出現 quest 落日大蝙蝠', async ({ page }) => {
  // 1. Open Django webpage
  await page.goto('http://127.0.0.1:8000/quests/');
  // 2. click region
  await page.getByText('HexRealm', { exact: true }).click();
  await page.getByText('魔女山谷', { exact: true }).click();
  // 3. Check table.searchtime displays quests
  const cell = page.locator('table.searchtime >> text=落日大蝙蝠');
  // 4. expect element appear
  await expect(cell).not.toBeVisible();
});

test('點擊 area "HexRealm" 再點擊 "HexRealm"，會取消全選', async ({ page }) => {
  // 1. Open Django webpage
  await page.goto('http://127.0.0.1:8000/quests/');
  // 2. click region
  await page.getByText('HexRealm', { exact: true }).click();
  await page.getByText('HexRealm', { exact: true }).click();
  // 3. Check table.searchtime displays quests
  const cell = page.locator('table.searchtime >> text=落日大蝙蝠');
  // 4. expect element appear
  await expect(cell).not.toBeVisible();
});

test('點擊 area "HexRealm" 再點擊 region 魔女山谷，再點擊 "HexRealm"，會恢復全選', async ({ page }) => {
  // 1. Open Django webpage
  await page.goto('http://127.0.0.1:8000/quests/');
  // 2. click region
  await page.getByText('HexRealm', { exact: true }).click();
  await page.getByText('魔女山谷', { exact: true }).click();
  await page.getByText('HexRealm', { exact: true }).click();
  // 3. Check table.searchtime displays quests
  const cell = page.locator('table.searchtime >> text=落日大蝙蝠');
  // 4. expect element appear
  await expect(cell).toBeVisible();
});

test('點擊 region 死都黑爾頓，再勾 checkbox M3，應該出現 quest 死都的寶藏3 而非 死都的寶藏2', async ({ page }) => {
  // 1. Open Django webpage
  await page.goto('http://127.0.0.1:8000/quests/');
  // 2. click region and checkbox
  await page.getByText('死都黑爾頓', { exact: true }).click();
  await page.getByLabel('M3').check();
  // 3. Check table.searchtime displays quests
  const cell1 = page.locator('table.searchtime >> text=死都的寶藏2');
  const cell2 = page.locator('table.searchtime >> text=死都的寶藏3');
  // 4. expect element appear
  await expect(cell1).not.toBeVisible();
  await expect(cell2).toBeVisible();
});

test('點擊 region 死都黑爾頓，再勾 checkbox M2 和 M3，只會出現 quest 失音的廣場1', async ({ page }) => {
  // 1. Open Django webpage
  await page.goto('http://127.0.0.1:8000/quests/');
  // 2. click region
  await page.getByText('死都黑爾頓', { exact: true }).click();
  await page.getByLabel('M2').check();
  await page.getByLabel('M3').check();
  // 3. Check table.searchtime displays quests
  const cell1 = page.locator('table.searchtime >> text=失音的廣場1');
  const cell2 = page.locator('table.searchtime >> text=死都的寶藏3');
  // 4. expect element appear
  await expect(cell1).toBeVisible();
  await expect(cell2).not.toBeVisible();
});

test('點擊 region 死都黑爾頓，勾 checkbox M2 和 M3，再勾 M2，會出現 quest 失音的廣場1 和 死都的寶藏3', async ({ page }) => {
  // 1. Open Django webpage
  await page.goto('http://127.0.0.1:8000/quests/');
  // 2. click region
  await page.getByText('死都黑爾頓', { exact: true }).click();
  const m2 = page.getByLabel('M2');
  await m2.check();
  await page.getByLabel('M3').check();
  const isChecked = await m2.isChecked();
  if (isChecked) {
    await m2.uncheck();   // 取消勾選
  }
  // 3. Check table.searchtime displays quests
  const cell1 = page.locator('table.searchtime >> text=失音的廣場1');
  const cell2 = page.locator('table.searchtime >> text=死都的寶藏3');
  // 4. expect element appear
  await expect(cell1).toBeVisible();
  await expect(cell2).toBeVisible();
});

test('點擊 region 死都黑爾頓，再勾 checkbox M1 和寶圖，只會出現 quest 死都的寶藏1', async ({ page }) => {
  // 1. Open Django webpage
  await page.goto('http://127.0.0.1:8000/quests/');
  // 2. click region
  await page.getByText('死都黑爾頓', { exact: true }).click();
  await page.getByLabel('M1').check();
  await page.getByLabel('寶圖').check();
  // 3. Check table.searchtime displays quests
  const cell1 = page.locator('table.searchtime >> text=死都的寶藏1');
  const cell2 = page.locator('table.searchtime >> text=死都的寶藏3');
  const cell3 = page.locator('table.searchtime >> text=死都的入口3');
  // 4. expect element appear
  await expect(cell1).toBeVisible();
  await expect(cell2).not.toBeVisible();
  await expect(cell3).not.toBeVisible();
});

test('點擊 region 死都黑爾頓，再勾 checkbox M2 和 BOSS，只會出現 quest 飛龍的守護者2(BOSS)', async ({ page }) => {
  // 1. Open Django webpage
  await page.goto('http://127.0.0.1:8000/quests/');
  // 2. click region
  await page.getByText('死都黑爾頓', { exact: true }).click();
  await page.getByLabel('M2').check();
  await page.getByLabel('BOSS').check();
  // 3. Check table.searchtime displays quests
  const cell1 = page.locator('table.searchtime >> text=飛龍的守護者2(BOSS)');
  const cell2 = page.locator('table.searchtime >> text=飛龍的守護者1(BOSS)');
  // 4. expect element appear
  await expect(cell1).toBeVisible();
  await expect(cell2).not.toBeVisible();
});