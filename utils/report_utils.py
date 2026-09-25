import os
import base64
import datetime

from config import config

execution_log = []


def log_step(step: str, status: str = "PASS", message: str = ""):
    execution_log.append({
        "step": step,
        "status": status.upper(),
        "message": message,
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
    })


def reset():
    execution_log.clear()


def _status_color(status):
    return {
        "PASS": "#2d8a4e",
        "FAIL": "#cc2222",
        "INFO": "#1565c0",
    }.get(status, "#666666")


def _embed_image(path):
    # convert screenshot to base64 so it embeds directly in the html
    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    except Exception:
        return ""


def generate_html_report(screenshots, report_name="execution_report.html", suite_name="E-Commerce Automation Suite"):
    # builds the html report from execution_log and the captured screenshots list
    os.makedirs(config.HTML_REPORT_DIR, exist_ok=True)
    report_path = os.path.join(config.HTML_REPORT_DIR, report_name)

    total = len(execution_log)
    passed = sum(1 for e in execution_log if e["status"] == "PASS")
    failed = sum(1 for e in execution_log if e["status"] == "FAIL")
    info = total - passed - failed

    rows_html = ""
    for entry in execution_log:
        color = _status_color(entry["status"])
        rows_html += f"""
        <tr>
            <td>{entry['time']}</td>
            <td>{entry['step']}</td>
            <td style="color:{color}; font-weight:bold;">{entry['status']}</td>
            <td>{entry['message']}</td>
        </tr>"""

    shots_html = ""
    for step_name, path in screenshots:
        data_uri = _embed_image(path)
        if not data_uri:
            continue
        shots_html += f"""
        <div class="shot-card">
            <p class="shot-title">{step_name}</p>
            <img src="{data_uri}" alt="{step_name}" />
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{suite_name} - Execution Report</title>
<style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background:#f4f6f8; margin:0; padding:24px; color:#202124; }}
    h1 {{ margin-bottom:4px; }}
    .subtitle {{ color:#5f6368; margin-top:0; }}
    .summary {{ display:flex; gap:16px; margin:20px 0; }}
    .card {{ background:#fff; border-radius:8px; padding:16px 24px; box-shadow:0 1px 3px rgba(0,0,0,0.15); flex:1; text-align:center; }}
    .card h2 {{ margin:0; font-size:28px; }}
    .card p {{ margin:4px 0 0; color:#5f6368; }}
    table {{ width:100%; border-collapse:collapse; background:#fff; border-radius:8px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.15); }}
    th, td {{ text-align:left; padding:10px 14px; border-bottom:1px solid #eee; font-size:14px; }}
    th {{ background:#202124; color:#fff; }}
    .screenshots {{ display:flex; flex-wrap:wrap; gap:16px; margin-top:24px; }}
    .shot-card {{ background:#fff; border-radius:8px; padding:10px; box-shadow:0 1px 3px rgba(0,0,0,0.15); width:280px; }}
    .shot-card img {{ width:100%; border-radius:4px; border:1px solid #ddd; }}
    .shot-title {{ font-size:13px; font-weight:600; margin:4px 0; }}
    section {{ margin-top:32px; }}
</style>
</head>
<body>
    <h1>{suite_name}</h1>
    <p class="subtitle">Execution Report generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

    <div class="summary">
        <div class="card"><h2>{total}</h2><p>Total Steps</p></div>
        <div class="card"><h2 style="color:#2d8a4e;">{passed}</h2><p>Passed</p></div>
        <div class="card"><h2 style="color:#cc2222;">{failed}</h2><p>Failed</p></div>
        <div class="card"><h2 style="color:#1565c0;">{info}</h2><p>Info</p></div>
    </div>

    <section>
        <h2>Step Log</h2>
        <table>
            <tr><th>Time</th><th>Step</th><th>Status</th><th>Message</th></tr>
            {rows_html}
        </table>
    </section>

    <section>
        <h2>Screenshots</h2>
        <div class="screenshots">
            {shots_html if shots_html else "<p>No screenshots captured.</p>"}
        </div>
    </section>
</body>
</html>"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    return report_path
