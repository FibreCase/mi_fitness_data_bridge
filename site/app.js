"use strict";
let language = new URLSearchParams(location.search).get("lang") === "en" ? "en" : "zh";
let dataset = "daily_activity";
const fields = {
  daily_activity: ["date", "steps", "distance_m", "active_kcal", "active_minutes"],
  sleep: ["start_at", "end_at", "duration_minutes", "time_asleep_minutes", "sleep_score"],
  workouts: ["activity_type", "start_at", "duration_minutes", "distance_m", "calories_kcal"],
  body_measurements: ["timestamp", "weight_kg", "bmi", "body_fat_pct"]
};
function render() {
  document.documentElement.lang = language === "zh" ? "zh-CN" : "en";
  document.querySelectorAll("[data-zh]").forEach(el => { el.innerHTML = el.dataset[language]; });
  document.getElementById("language").textContent = language === "zh" ? "English" : "中文";
  document.getElementById("install").href = "https://github.com/shkyyy18/mi_fitness_data_bridge" + (language === "zh" ? "#安装" : "/blob/main/README.en.md#install");
  document.querySelectorAll("[data-dataset]").forEach(el => el.setAttribute("aria-pressed", String(el.dataset.dataset === dataset)));
  const table = document.createElement("table");
  const caption = table.createCaption();
  caption.textContent = language === "zh" ? "合成记录预览 · 仅展示部分字段，下载包含完整列" : "Synthetic preview · selected columns; downloads include all columns";
  const heading = table.createTHead().insertRow();
  fields[dataset].forEach(field => { const th = document.createElement("th"); th.scope = "col"; th.textContent = field; heading.append(th); });
  const body = table.createTBody();
  SAMPLE.json.records[dataset].forEach(record => {
    const row = body.insertRow();
    fields[dataset].forEach(field => { row.insertCell().textContent = record[field] == null ? "—" : String(record[field]); });
  });
  document.getElementById("preview").replaceChildren(table);
  document.getElementById("row-note").textContent = language === "zh" ? "样例不是你的个人数据" : "Not your personal data";
  document.getElementById("json-preview").textContent = JSON.stringify(SAMPLE.json, null, 2);
}
function download(text, filename, type) {
  const url = URL.createObjectURL(new Blob([text], {type}));
  const a = document.createElement("a"); a.href = url; a.download = filename; document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}
document.getElementById("language").addEventListener("click", () => { language = language === "zh" ? "en" : "zh"; render(); });
document.querySelectorAll("[data-dataset]").forEach(el => el.addEventListener("click", () => { dataset = el.dataset.dataset; render(); }));
document.getElementById("csv").addEventListener("click", () => download(SAMPLE.csv[dataset + ".csv"], "synthetic-" + dataset + ".csv", "text/csv;charset=utf-8"));
document.getElementById("json").addEventListener("click", () => download(JSON.stringify(SAMPLE.json, null, 2) + "\n", "synthetic-mi-fitness.json", "application/json"));
render();
