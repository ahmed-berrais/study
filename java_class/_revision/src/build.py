#!/usr/bin/env python3
"""Build the Java revision PDFs.

    python3 build.py            # check all code + build both PDFs
    python3 build.py --no-pdf   # only compile/run the code blocks

Source files are HTML with fenced code blocks:

    ```java class      full compilation unit (one or more classes) -> compiled
    ```java frag       statements -> wrapped in a main() and compiled + run
    ```java members    fields/methods -> wrapped in a class and compiled
    ```java nocheck    intentionally wrong or partial code -> not compiled
    ```text            program output / plain text

Every checked block is compiled with javac before the PDF is made, so the
PDFs never contain Java that does not compile.
"""
import html
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)  # java_class/_revision

KEYWORDS = set("""abstract boolean break byte case catch char class continue default do
double else extends final finally float for if implements import int interface long new
package private protected public return short static super switch this throw throws try
void while null true false var""".split())

FENCE = re.compile(r"```(\w+)(?:[ \t]+(\w+))?[ \t]*\n(.*?)\n```", re.S)


def highlight(code: str) -> str:
    token = re.compile(
        r'(?P<com>//[^\n]*|/\*.*?\*/)|(?P<str>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])\')'
        r'|(?P<num>\b\d+(?:\.\d+)?[fFdDlL]?\b)|(?P<word>\b[A-Za-z_]\w*\b)',
        re.S,
    )
    out, pos = [], 0
    for m in token.finditer(code):
        out.append(html.escape(code[pos:m.start()]))
        t = m.group(0)
        e = html.escape(t)
        if m.group("com"):
            out.append(f'<span class="c">{e}</span>')
        elif m.group("str"):
            out.append(f'<span class="s">{e}</span>')
        elif m.group("num"):
            out.append(f'<span class="n">{e}</span>')
        elif t in KEYWORDS:
            out.append(f'<span class="k">{e}</span>')
        elif t[0].isupper():
            out.append(f'<span class="t">{e}</span>')
        else:
            out.append(e)
        pos = m.end()
    out.append(html.escape(code[pos:]))
    return "".join(out)


def java_env():
    env = dict(os.environ)
    env.pop("JAVA_TOOL_OPTIONS", None)
    return env


def check_block(kind: str, code: str, label: str) -> None:
    if kind == "frag":
        imports = "".join(l + "\n" for l in code.splitlines() if l.startswith("import "))
        body = "\n".join(l for l in code.splitlines() if not l.startswith("import "))
        src = imports + "public class Main {\npublic static void main(String[] args) throws Exception {\n" + body + "\n}\n}\n"
        name = "Main"
    elif kind == "members":
        src = "public class Main {\n" + code + "\n}\n"
        name = "Main"
    else:
        src = code
        m = re.search(r"public\s+(?:final\s+|abstract\s+)?class\s+(\w+)", code)
        name = m.group(1) if m else "Main"
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, name + ".java")
        with open(path, "w") as f:
            f.write(src)
        r = subprocess.run(["javac", "-nowarn", "-d", d, path], capture_output=True, text=True, env=java_env())
        if r.returncode != 0:
            print(f"\n✗ {label}: does not compile\n{src}\n{r.stderr}")
            sys.exit(1)
        if kind == "frag" and "Scanner" not in code:
            r = subprocess.run(["java", "-cp", d, "Main"], capture_output=True, text=True, env=java_env(), timeout=10)
            if r.returncode != 0:
                print(f"\n✗ {label}: crashes\n{src}\n{r.stderr}")
                sys.exit(1)


def render(src_name: str, check_only: bool) -> str:
    with open(os.path.join(HERE, src_name)) as f:
        text = f.read()
    count = {"checked": 0}

    def repl(m):
        lang, kind, code = m.group(1), (m.group(2) or ""), m.group(3)
        if lang == "java" and kind in ("class", "frag", "members"):
            line = text[: m.start()].count("\n") + 1
            check_block(kind, code, f"{src_name}:{line}")
            count["checked"] += 1
        cls = "code" if lang == "java" else "out"
        body = highlight(code) if lang == "java" else html.escape(code)
        return f'<pre class="{cls}">{body}</pre>'

    page = FENCE.sub(repl, text)
    print(f"✓ {src_name}: {count['checked']} code blocks compiled OK")
    with open(os.path.join(HERE, "style.css")) as f:
        css = f.read()
    return page.replace("/*STYLE*/", css)


def to_pdf(html_text: str, pdf_name: str) -> None:
    tmp = os.path.join(tempfile.gettempdir(), pdf_name + ".html")
    with open(tmp, "w") as f:
        f.write(html_text)
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://{tmp}');
  await p.pdf({{ path: '{os.path.join(OUT, pdf_name)}', format: 'A4', printBackground: true,
    margin: {{ top: '14mm', bottom: '16mm', left: '13mm', right: '13mm' }},
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#888">' +
      '{pdf_name.replace(".pdf", "").replace("_", " ")} · page <span class="pageNumber"></span>/<span class="totalPages"></span></div>' }});
  await b.close();
}})();
"""
    subprocess.run(["node", "-e", js], check=True)
    print(f"✓ wrote {os.path.join(OUT, pdf_name)}")


if __name__ == "__main__":
    no_pdf = "--no-pdf" in sys.argv
    for src, pdf in [("cheatsheet.html", "Java_CheatSheet.pdf"), ("ds.html", "Java_DS_Blanc_Mock_Exam.pdf")]:
        if not os.path.exists(os.path.join(HERE, src)):
            continue
        page = render(src, no_pdf)
        if not no_pdf:
            to_pdf(page, pdf)
