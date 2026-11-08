#!/usr/bin/env python3
"""Build the Information System revision PDF.

    python3 build.py

guide.html may contain {{fig:name}} (a diagram from diagrams.py, drawn as SVG)
and {{img:path}} (an image embedded in the PDF; path relative to this folder).
"""
import base64, mimetypes, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import diagrams  # noqa: E402


def fig(m):
    return diagrams.ALL[m.group(1)]()


def img(m):
    path = os.path.normpath(os.path.join(HERE, m.group(1)))
    mime = mimetypes.guess_type(path)[0]
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def main():
    page = open(os.path.join(HERE, "guide.html")).read()
    page = re.sub(r"\{\{fig:(\w+)\}\}", fig, page)
    page = re.sub(r"\{\{img:([^}]+)\}\}", img, page)
    page = page.replace("/*STYLE*/", open(os.path.join(HERE, "style.css")).read())
    tmp = os.path.join(tempfile.gettempdir(), "is_guide.html")
    open(tmp, "w").write(page)
    pdf = os.path.join(OUT, "IS_Revision_Guide.pdf")
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://{tmp}');
  await p.pdf({{ path: {pdf!r}, format: 'A4', printBackground: true,
    margin: {{ top: '14mm', bottom: '16mm', left: '13mm', right: '13mm' }},
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#888">IS Revision Guide · page <span class="pageNumber"></span>/<span class="totalPages"></span></div>' }});
  await b.close();
}})();
"""
    subprocess.run(["node", "-e", js], check=True)
    print("✓ wrote", pdf)


if __name__ == "__main__":
    main()
