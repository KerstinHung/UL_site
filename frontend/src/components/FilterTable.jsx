import { useState } from "react";

export default function FilterTable({ rowsData, regions }) {
  const [selectedRegions, setSelectedRegions] = useState([]);
  const [checkboxes, setCheckboxes] = useState({
    m1: false, m2: false, m3: false,
    gold: false, platinum: false,
    boss: false, treasure: false
  });

  const toggleRegion = (region) => {
    setSelectedRegions(prev =>
      prev.includes(region)
        ? prev.filter(r => r !== region)
        : [...prev, region]
    );
  };

  const toggleCheckbox = (name) => {
    setCheckboxes(prev => ({ ...prev, [name]: !prev[name] }));
  };

  const toNum = v => Number(v || 0);
  const isTrueStr = v => v === "1" || v === "True" || v === "true";

  const filteredRows = rowsData.filter(row => {
    // region filter
    if (selectedRegions.length > 0 && !selectedRegions.includes(row.region)) return false;

    if (checkboxes.m1 && !(toNum(row.m1) > 0 || toNum(row.iron) > 0 || toNum(row.memory) > 0)) return false;
    if (checkboxes.m2 && !(toNum(row.m2) > 0 || toNum(row.bronze) > 0 || toNum(row.time) > 0)) return false;
    if (checkboxes.m3 && !(toNum(row.m3) > 0 || toNum(row.silver) > 0 || toNum(row.soul) > 0)) return false;
    if (checkboxes.gold && !(toNum(row.gold) > 0 || toNum(row.light) > 0)) return false;
    if (checkboxes.platinum && !(toNum(row.platinum) > 0 || toNum(row.unlight) > 0)) return false;
    if (checkboxes.boss && !isTrueStr(row.boss)) return false;
    if (checkboxes.treasure && !isTrueStr(row.treasure)) return false;

    return true;
  });

  return (
    <div>
      <div>
        {Object.keys(checkboxes).map(name => (
          <label key={name}>
            <input
              type="checkbox"
              checked={checkboxes[name]}
              onChange={() => toggleCheckbox(name)}
            /> {name}
          </label>
        ))}
      </div>

      <ul>
        {regions.map(region => (
          <li
            key={region}
            className={selectedRegions.includes(region) ? "checked" : ""}
            onClick={() => toggleRegion(region)}
          >{region}</li>
        ))}
      </ul>

      <table>
        <tbody>
          {filteredRows.map((row, idx) => (
            <tr key={idx}>
              <td>{row.name}</td>
              <td>{row.region}</td>
              {/* 其他欄位 */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
