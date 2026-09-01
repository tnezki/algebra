\
#!/usr/bin/env python3

from __future__ import annotations

import html
import re
import tempfile
from datetime import date, datetime
from pathlib import Path

import requests
from openpyxl import load_workbook

SPREADSHEET_ID = "1Qga2eTz0Nfgu8wIw5L-ZGC2xRtb4fOUoUXN-TyxuASE"
SHEET_NAME = "Student Calendar"
EXPORT_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx"

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "index.html"

RESOURCE_LINKS = [
    ("Course Website", "https://tnezki.github.io/algebra/"),
    ("Overview", "https://tnezki.github.io/algebra/misc/overview.html"),
    ("Textbook", "https://tnezki.github.io/textbooks/alg/index.html"),
    ("Virtual Tools", "https://technology.cpm.org/general/tiles/"),
    ("Printables", "https://tnezki.github.io/algebra/misc/printables/aaagallery_index.html"),
    ("Desmos", "https://www.desmos.com/calculator"),
    ("GeoGebra", "https://www.geogebra.org/graphing"),
    ("Canvas", "https://mariners.instructure.com/"),
    ("Upload Spot", "https://drive.google.com/drive/folders/1DwDKsvsAHMFefLMderdK8PI3MBcvXAxu?usp=sharing"),
]

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def safe_text(value):
    if value is None or value.__class__.__name__ == "ArrayFormula":
        return ""
    if isinstance(value, (datetime, date)):
        return f"{value.month}/{value.day}"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def looks_like_date(value):
    if isinstance(value, (datetime, date)):
        return True
    if value is None:
        return False
    return bool(re.fullmatch(r"\d{1,2}/\d{1,2}(?:/\d{2,4})?", str(value).strip()))


def date_key(value, school_start_year=2026):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if value is None:
        return None
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", str(value).strip())
    if not m:
        return None
    month, day = int(m.group(1)), int(m.group(2))
    year_text = m.group(3)
    if year_text:
        year = int(year_text)
        if year < 100:
            year += 2000
    else:
        year = school_start_year if month >= 7 else school_start_year + 1
    try:
        return date(year, month, day)
    except ValueError:
        return None


def cell_info(ws_values, ws_links, row, col):
    vc = ws_values.cell(row=row, column=col)
    lc = ws_links.cell(row=row, column=col)

    # Keep evaluated blank formulas blank instead of displaying the formula.
    value = vc.value
    link = None

    for c in (vc, lc):
        if c.hyperlink and c.hyperlink.target:
            link = c.hyperlink.target
            break

    formula = lc.value
    if not link and isinstance(formula, str) and formula.startswith("="):
        m = re.search(r'HYPERLINK\(\s*"([^"]+)"', formula, re.I)
        if m:
            link = m.group(1)

    return safe_text(value), link


def gather_items(ws_values, ws_links, start_row, end_row, col):
    items = []
    for row in range(start_row, end_row + 1):
        label, url = cell_info(ws_values, ws_links, row, col)
        if label:
            items.append((label, url))
    return items


def download_workbook():
    response = requests.get(
        EXPORT_URL,
        timeout=45,
        headers={"User-Agent": "Mozilla/5.0 AgendaBuilder/1.0"},
    )
    response.raise_for_status()
    if len(response.content) < 1000:
        raise RuntimeError("Google returned an unexpectedly small workbook export.")
    f = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    f.write(response.content)
    f.close()
    return Path(f.name)


def read_calendar():
    xlsx = download_workbook()
    try:
        wb_values = load_workbook(xlsx, data_only=True, read_only=False)
        wb_links = load_workbook(xlsx, data_only=False, read_only=False)

        if SHEET_NAME not in wb_values.sheetnames:
            raise RuntimeError(f"Missing sheet: {SHEET_NAME}")

        wsv = wb_values[SHEET_NAME]
        wsl = wb_links[SHEET_NAME]

        current_dates = [cell_info(wsv, wsl, 2, c)[0] for c in range(1, 6)]
        current_items = [gather_items(wsv, wsl, 3, 9, c) for c in range(1, 6)]
        current_start = next((date_key(x) for x in current_dates if date_key(x)), None)

        archive_date_rows = []
        for r in range(11, min(wsv.max_row, 500) + 1):
            values = [wsv.cell(r, c).value for c in range(1, 6)]
            if sum(1 for v in values if looks_like_date(v)) >= 4:
                archive_date_rows.append(r)

        previous = []
        for i, date_row in enumerate(archive_date_rows):
            next_date_row = (
                archive_date_rows[i + 1]
                if i + 1 < len(archive_date_rows)
                else min(date_row + 11, wsv.max_row + 1)
            )

            dates = [cell_info(wsv, wsl, date_row, c)[0] for c in range(1, 6)]
            start = next((date_key(x) for x in dates if date_key(x)), None)

            # Keep every week in the lower calendar.
            # Highlight the one that matches the top current-week block.
            is_current = bool(current_start and start and start == current_start)

            end_row = min(next_date_row - 1, date_row + 10)
            items = [gather_items(wsv, wsl, date_row + 1, end_row, c) for c in range(1, 6)]

            if any(items):
                previous.append({
                    "dates": dates,
                    "items": items,
                    "is_current": is_current,
                })

        return {
            "current": {"dates": current_dates, "items": current_items},
            "previous": previous,
        }
    finally:
        try:
            xlsx.unlink()
        except OSError:
            pass


def render_link(label, url, kind=""):
    classes = "cal-link" + (f" {kind}" if kind else "")
    if url:
        return (
            f'<a class="{classes}" href="{html.escape(url, quote=True)}" '
            f'target="_blank" rel="noopener">{html.escape(label)}</a>'
        )
    return f'<span class="{classes} no-link">{html.escape(label)}</span>'


def render_week(dates, items_by_day, current=False, archive_current=False):
    if current:
        cells = "".join(
            f"<th><div class='dow'>{d}</div><div class='date'>{html.escape(x)}</div></th>"
            for d, x in zip(DAY_NAMES, dates)
        )
        header = f'<tr class="week-head">{cells}</tr>'
        cls = "current-week"
    else:
        cells = "".join(
            f"<th><div class='date'>{html.escape(x)}</div></th>"
            for x in dates
        )
        header = f'<tr class="week-head">{cells}</tr>'
        cls = "calendar-current-week" if archive_current else "previous-week"

    row_count = max([len(x) for x in items_by_day] + [1])
    body_rows = []

    for i in range(row_count):
        tds = []
        for items in items_by_day:
            if i >= len(items):
                tds.append("<td></td>")
                continue

            label, url = items[i]
            kind = ""
            if i == 0:
                low = label.lower()
                kind = "holiday" if any(x in low for x in ("labor day", "pd", "no school", "holiday")) else "lesson"
            tds.append(f"<td>{render_link(label, url, kind)}</td>")
        body_rows.append("<tr>" + "".join(tds) + "</tr>")

    return f'<tbody class="week-block {cls}">{header}{"".join(body_rows)}</tbody>'


def build_html(calendar):
    resources = "\n".join(
        f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">{html.escape(label)}</a>'
        for label, url in RESOURCE_LINKS
    )

    current_html = render_week(
        calendar["current"]["dates"],
        calendar["current"]["items"],
        current=True,
    )

    previous_html = ""
    if calendar["previous"]:
        previous_html = (
            '<tbody class="previous-weeks-divider"><tr>'
            '<td colspan="5">Previous Weeks</td>'
            '</tr></tbody>'
            + "".join(
                render_week(
                    w["dates"],
                    w["items"],
                    current=False,
                    archive_current=w.get("is_current", False),
                )
                for w in calendar["previous"]
            )
        )

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>Algebra 1 Agenda 2026-2027</title>
<style>
:root {{
  --navy:#173f6d;
  --navy-dark:#173f6d;
  --gold:#e0bd4f;
  --gold-light:#fff0b8;
  --gold-pale:#fff8df;
  --ink:#1f2937;
  --muted:#64748b;
  --lesson:#fff0b8;
  --link:#173f6d;
}}
* {{ box-sizing:border-box; }}
body {{
  margin:0;
  font-family:Arial, Helvetica, sans-serif;
  background:#fff;
  color:var(--ink);
}}
.wrapper {{
  width:min(1180px, calc(100% - 24px));
  margin:18px auto 40px;
}}
.titlebar {{
  background:var(--navy);
  color:#fff;
  padding:16px 22px;
  border-radius:10px 10px 0 0;
  text-align:center;
}}
.titlebar h1 {{
  margin:0;
  font-size:clamp(1.55rem, 3vw, 2.25rem);
  font-weight:800;
}}
.titlebar .small {{
  font-size:.64em;
  font-weight:600;
}}
.resources {{
  border:1px solid var(--gold);
  border-top:0;
  padding:12px 14px 13px;
  display:flex;
  flex-wrap:wrap;
  justify-content:center;
  gap:8px;
  background:#fff9e9;
}}
.resources a {{
  text-decoration:none;
  color:var(--navy-dark);
  background:#fff;
  border:1px solid var(--gold);
  border-radius:999px;
  padding:7px 11px;
  font-size:.88rem;
  font-weight:700;
}}
.resources a:hover,
.resources a:focus-visible {{
  background:var(--gold-light);
  border-color:var(--navy);
}}
.calendar-wrap {{
  overflow-x:auto;
  border:1px solid #c8b675;
  border-top:0;
}}
table {{
  border-collapse:collapse;
  width:100%;
  min-width:760px;
  table-layout:fixed;
}}
th, td {{
  border-right:1px solid #cfd4da;
  border-bottom:1px solid #cfd4da;
  text-align:center;
  vertical-align:middle;
}}
tr > *:last-child {{ border-right:0; }}
.week-head th {{ padding:8px 6px; }}
.dow {{ font-size:.9rem; font-weight:800; }}
.date {{ margin-top:2px; font-size:.82rem; font-weight:700; }}
td {{ padding:5px 6px; background:#fff; height:34px; }}
.cal-link {{
  display:block;
  width:100%;
  text-decoration:none;
  color:var(--link);
  font-size:.88rem;
  font-weight:650;
  padding:4px 5px;
  border-radius:5px;
}}
a.cal-link:hover,
a.cal-link:focus-visible {{
  background:#fff4c7;
  text-decoration:underline;
}}
.cal-link.lesson {{
  background:var(--lesson);
  border:1px solid #e1c86d;
  font-weight:800;
  color:var(--navy-dark);
}}
.cal-link.holiday {{
  background:#f6edcf;
  color:#475569;
  font-weight:800;
}}
.no-link {{ cursor:default; }}

.current-week .week-head th {{
  background:var(--navy);
  color:#fff;
  text-align:left;
  padding:9px 10px 10px;
}}
.current-week .dow {{
  font-size:1.02rem;
  font-weight:850;
  line-height:1.1;
}}
.current-week .date {{
  margin-top:4px;
  font-size:1.22rem;
  font-weight:900;
  text-align:left;
}}
.current-week td {{
  padding:0;
  height:48px;
  min-height:48px;
  background:#fff;
}}
.current-week .cal-link {{
  display:flex;
  align-items:center;
  justify-content:center;
  width:100%;
  min-height:48px;
  padding:10px 8px;
  font-size:1.08rem;
  font-weight:750;
  line-height:1.25;
}}
.current-week .cal-link.lesson {{
  background:#fff;
  border:0;
  color:var(--navy);
  font-size:1.12rem;
  font-weight:900;
  text-decoration:underline;
}}
.current-week .cal-link.holiday {{
  font-size:1.08rem;
  font-weight:900;
}}
.current-week tr:nth-child(odd):not(.week-head) td {{
  background:var(--gold-light);
}}

.previous-weeks-divider td {{
  background:var(--gold) !important;
  color:#10243d;
  font-size:1.05rem;
  font-weight:800;
  padding:10px 8px;
}}

.calendar-current-week .week-head th {{
  background:var(--navy);
  color:#fff;
  border-top:5px solid var(--gold);
  padding:8px 9px;
  font-weight:850;
  text-align:left;
}}
.calendar-current-week .week-head th .date {{
  color:#fff;
  font-size:1rem;
  font-weight:900;
  text-align:left;
}}
.calendar-current-week tr td {{
  background:#fff !important;
  border-color:#cfd4da;
}}
.calendar-current-week tr:nth-child(odd):not(.week-head) td {{
  background:var(--gold-light) !important;
}}
.calendar-current-week .cal-link.lesson {{
  background:#fff;
  border:0;
  color:var(--navy);
  font-weight:900;
  text-decoration:underline;
}}
.calendar-current-week .cal-link.holiday {{
  background:#f6edcf;
  color:#475569;
}}

.previous-week .week-head th {{
  background:#3f4650;
  color:#fff;
  border-top:5px solid #20242a;
  text-align:left;
  padding-left:9px;
}}
.previous-week .week-head th .date {{ color:#e5e7eb; }}
.previous-week tr td {{
  background:#fff !important;
  border-color:#cfd4da;
}}
.previous-week tr:nth-child(even) td {{
  background:#f3f4f6 !important;
}}
.previous-week .cal-link.lesson {{
  background:#e5e7eb;
  border:1px solid #c7ccd1;
  color:#2f3740;
}}
.previous-week .cal-link.holiday {{
  background:#eceff2;
  color:#4b5563;
}}
.previous-week a.cal-link:hover,
.previous-week a.cal-link:focus-visible {{
  background:#e2e6ea;
}}
.updated {{
  text-align:center;
  color:var(--muted);
  font-size:.76rem;
  padding-top:8px;
}}

@media (max-width:700px) {{
  .wrapper {{ width:100%; margin:0; }}
  .titlebar {{ border-radius:0; }}
  .resources {{ justify-content:flex-start; padding:10px; }}
  .resources a {{ font-size:.8rem; padding:6px 9px; }}
}}
</style>
</head>
<body>
<div class="wrapper">
  <header class="titlebar">
    <h1>Algebra 1 <span class="small">– Agenda 2026-2027</span></h1>
  </header>

  <nav class="resources" aria-label="Student resources">
    {resources}
  </nav>

  <div class="calendar-wrap">
    <table aria-label="Algebra 1 student agenda">
      {current_html}
      {previous_html}
    </table>
  </div>

  <div class="updated">Agenda generated {html.escape(stamp)}</div>
</div>
</body>
</html>
"""


def main():
    calendar = read_calendar()
    output = build_html(calendar)
    temp = OUTPUT.with_suffix(".html.tmp")
    temp.write_text(output, encoding="utf-8")
    temp.replace(OUTPUT)
    print(f"Updated {OUTPUT}")


if __name__ == "__main__":
    main()
