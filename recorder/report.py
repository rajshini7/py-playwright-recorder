from pathlib import Path
from datetime import datetime
import html
import base64

def _img_to_base64(path):
    if not path or not Path(path).exists():
        return ""
    data = Path(path).read_bytes()
    return base64.b64encode(data).decode("utf-8")

def generate_report(results, output_path="reports/replay-report.html"):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    rows = []
    for r in results:
        status_color = "#d4edda" if r["status"] == "PASS" else "#f8d7da"
        screenshot_html = ""

        if r["status"] == "FAIL" and r.get("screenshot"):
            img64 = _img_to_base64(r["screenshot"])
            screenshot_html = f"""
            <div style="margin-top:10px">
                <b>Failure Screenshot:</b><br/>
                <img src="data:image/png;base64,{img64}"
                     style="max-width:100%; border:1px solid #333"/>
            </div>
            """

        rows.append(f"""
        <tr style="background-color:{status_color}">
            <td>{r['step']}</td>
            <td>
              <a href="{html.escape(r['url'])}" target="_blank">
                {html.escape(r['url'])}
              </a>
            </td>
            <td>{html.escape(r['recorded'])}</td>
            <td>
                {html.escape(r['live'])}
                {screenshot_html}
            </td>
            <td><b>{r['status']}</b></td>
        </tr>
        """)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>Replay Verification Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; vertical-align: top; }}
            th {{ background-color: #333; color: white; }}
            td {{ white-space: pre-wrap; }}
        </style>
    </head>
    <body>
        <h1>Replay Verification Report</h1>
        <p><b>Generated:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <table>
            <tr>
                <th>Step</th>
                <th>URL</th>
                <th>Recorded firstP</th>
                <th>Live firstP / Screenshot</th>
                <th>Status</th>
            </tr>
            {''.join(rows)}
        </table>
    </body>
    </html>
    """

    Path(output_path).write_text(html_content, encoding="utf-8")
