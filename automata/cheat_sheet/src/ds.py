import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fa import FA
from diagrams import D as SD

OUT = "/home/user/study/automata/ds_prep/automata_DS_prep.html"
G = {}

# ---------- statement diagrams (series ex 6, redrawn) ----------
f = FA(400, 110); f.state("1", 50, 70, init="left"); f.state("2", 190, 70); f.state("3", 330, 70, final=True)
f.loop("1", "a"); f.loop("2", "b"); f.loop("3", "a,b"); f.edge("1", "2", "b"); f.edge("2", "3", "a")
G["s6a"] = f.svg("6a")

f = FA(460, 230); f.state("1", 40, 150, init="left"); f.state("2", 170, 150); f.state("3", 300, 50); f.state("4", 420, 150, final=True)
f.edge("1", "2", "a"); f.loop("2", "a", "down"); f.edge("2", "3", "b", bend=14); f.edge("3", "2", "a", bend=14)
f.loop("3", "b", "up"); f.edge("3", "4", "c", bend=14); f.edge("4", "3", "b", bend=14); f.edge("4", "2", "a, c", lo=-10)
G["s6b"] = f.svg("6b")


def chain(fin):
    f = FA(520, 110)
    for i in range(4):
        f.state(str(i + 1), 50 + i * 140, 70, init="left" if i == 0 else None, final=(i + 1) in fin)
    for i in range(3):
        f.loop(str(i + 1), "a"); f.edge(str(i + 1), str(i + 2), "b")
    f.loop("4", "a,b")
    return f.svg("chain")


G["s6c"] = chain({1, 2, 4})
G["s6d"] = chain({3})

f = FA(470, 110); f.state("q0", 50, 70, init="left"); f.state("q1", 170, 70); f.state("q2", 290, 70); f.state("q3", 410, 70, final=True)
f.loop("q0", "a,b"); f.edge("q0", "q1", "a"); f.edge("q1", "q2", "b"); f.edge("q2", "q3", "a")
G["s9"] = f.svg("E9 NFA")

f = FA(400, 110); f.state("q0", 50, 70, init="left"); f.state("q1", 190, 70); f.state("q2", 330, 70, final=True)
f.loop("q0", "a"); f.loop("q1", "b"); f.loop("q2", "a"); f.edge("q0", "q1", "ε"); f.edge("q1", "q2", "ε")
G["s9e"] = f.svg("E9 eps NFA")

# ---------- solution diagrams ----------
f = FA(260, 100); f.state("q0", 50, 60, init="left"); f.state("q1", 200, 60, final=True)
f.loop("q0", "b"); f.edge("q0", "q1", "a"); f.loop("q1", "a,b")
G["e3a"] = f.svg("at least one a")
f = FA(400, 100); f.state("q0", 50, 60, init="left", final=True); f.state("q1", 190, 60, final=True); f.state("q2", 330, 60, dead=True)
f.loop("q0", "b"); f.edge("q0", "q1", "a"); f.loop("q1", "b"); f.edge("q1", "q2", "a"); f.loop("q2", "a,b")
G["e3b"] = f.svg("at most one a")
f = FA(260, 110); f.state("q0", 50, 60, init="left", final=True); f.state("q1", 200, 60)
f.loop("q0", "b"); f.loop("q1", "b"); f.edge("q0", "q1", "a", bend=16); f.edge("q1", "q0", "a", bend=16)
G["e3c"] = f.svg("even a")

f = FA(390, 200); f.state("0", 40, 100, init="left")
for i, (s, y) in enumerate([("1", 40), ("2", 40), ("3", 40)]):
    f.state(s, 140 + i * 110, y, final=(s == "3"))
for i, s in enumerate(["4", "5", "6"]):
    f.state(s, 140 + i * 110, 165, final=(s == "6"))
f.edge("0", "1", "a"); f.edge("1", "2", "b"); f.edge("2", "3", "a"); f.edge("0", "4", "b", lo=-10); f.edge("4", "5", "a"); f.edge("5", "6", "b")
G["e4a"] = f.svg("aba|bab")

f = FA(390, 240); f.state("0", 40, 120, init="left", final=True)
for i, s in enumerate(["1", "2", "3"]):
    f.state(s, 140 + i * 110, 60, final=(s == "3"))
for i, s in enumerate(["4", "5", "6"]):
    f.state(s, 140 + i * 110, 180, final=(s == "6"))
f.edge("0", "1", "a"); f.edge("1", "2", "b"); f.edge("2", "3", "a"); f.edge("3", "1", "a", bend=-50, lo=-10)
f.edge("0", "4", "b", lo=-10); f.edge("4", "5", "a"); f.edge("5", "6", "b"); f.edge("6", "4", "b", bend=50)
G["e4b"] = f.svg("(aba)*|(bab)*")


def bbb(flip):
    f = FA(520, 170)
    for i, s in enumerate("ABCD"):
        fin = (s != "D") if flip else (s == "D")
        f.state(s, 50 + i * 140, 70, init="left" if s == "A" else None, final=fin, dead=(flip and s == "D"))
    f.loop("A", "a"); f.edge("A", "B", "b", bend=-12); f.edge("B", "A", "a", bend=-12)
    f.edge("B", "C", "b"); f.edge("C", "A", "a", bend=-60, lo=-10); f.edge("C", "D", "b"); f.loop("D", "a,b")
    return f.svg("bbb")


G["e4c"] = bbb(False)
G["e4d"] = bbb(True)

f = FA(520, 230); f.state("0", 40, 115, init="left"); f.state("1", 150, 45); f.state("2", 150, 185)
f.state("3", 280, 115); f.state("4", 380, 115); f.state("5", 480, 115, final=True)
f.edge("0", "1", "a"); f.edge("0", "2", "b", lo=-10); f.edge("0", "3", "a", bend=0, t=0.78)
f.loop("1", "a", "up"); f.loop("2", "b", "down"); f.edge("1", "2", "b", bend=34, t=0.3); f.edge("2", "1", "a", bend=34, t=0.3)
f.edge("1", "3", "a"); f.edge("2", "3", "a", lo=-10); f.edge("3", "4", "b"); f.edge("4", "5", "b")
G["e5g"] = f.svg("Glushkov (a|b)*abb")
G["e5d"] = SD["p_abb"]

f = FA(380, 220); f.state("0", 50, 110, init="left"); f.state("1", 190, 40); f.state("3", 190, 185); f.state("2", 330, 110, final=True)
f.loop("0", "b", "down"); f.edge("0", "1", "a", bend=-14); f.edge("1", "0", "a", bend=-14)
f.edge("1", "2", "b"); f.edge("2", "3", "a", bend=14); f.edge("3", "2", "b", bend=14)
f.edge("3", "1", "a", bend=0, lo=-10, t=0.72); f.edge("2", "0", "b", lo=-12, t=0.62)
G["e6"] = f.svg("table automaton")

f = FA(440, 150); f.state("15", 60, 90, init="left", rx=24, label="1,5"); f.state("26", 220, 90, rx=24, label="2,6")
f.state("37", 380, 90, final=True, rx=24, label="3,7")
f.loop("15", "b"); f.loop("26", "a"); f.edge("15", "26", "a"); f.edge("26", "37", "b", bend=14); f.edge("37", "26", "a", bend=14)
f.edge("37", "15", "b", bend=-60, lo=-10)
G["e8"] = f.svg("minimised ends ab")

f = FA(520, 190)
for i, (s, lab) in enumerate([("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]):
    f.state(s, 50 + i * 140, 90, init="left" if s == "A" else None, final=(s == "D"))
f.loop("A", "b"); f.edge("A", "B", "a"); f.loop("B", "a"); f.edge("B", "C", "b", bend=-12); f.edge("C", "D", "a", bend=-12)
f.edge("D", "C", "b", bend=-12); f.edge("C", "A", "b", bend=50); f.edge("D", "B", "a", bend=-55, lo=-10)
G["e9"] = f.svg("DFA ends aba")

f = FA(500, 110)
f.state("A", 50, 70, init="left", final=True); f.state("B", 180, 70, final=True); f.state("C", 310, 70, final=True); f.state("X", 440, 70, dead=True, label="ϕ")
f.loop("A", "a"); f.edge("A", "B", "b"); f.loop("B", "b"); f.edge("B", "C", "a"); f.loop("C", "a"); f.edge("C", "X", "b"); f.loop("X", "a,b")
G["e9e"] = f.svg("DFA a*b*a*")

# --- big exercise diagrams ---
f = FA(500, 360)
f.state("0", 50, 180, init="left"); f.state("10", 50, 45, final=True); f.state("7", 50, 320, final=True)
f.state("1", 190, 45); f.state("2", 190, 130); f.state("4", 190, 225); f.state("8", 190, 310)
f.state("3", 330, 130); f.state("5", 330, 225); f.state("9", 330, 310, final=True); f.state("6", 460, 225)
f.edge("0", "10", "ε"); f.edge("0", "7", "b", lo=-10); f.edge("0", "1", "a"); f.edge("0", "2", "b", t=0.7)
f.edge("0", "4", "b", t=0.7, lo=-10); f.edge("0", "8", "b", lo=-10, t=0.7)
f.loop("1", "a", "up"); f.edge("2", "3", "a"); f.edge("3", "1", "a"); f.edge("4", "5", "b"); f.edge("5", "6", "a")
f.edge("6", "1", "a", bend=80); f.edge("8", "9", "b")
f.note(230, 355, "1, 3, 6: same exits as 0 (see table)")
G["b_nfa"] = f.svg("Glushkov NFA")
f = FA(580, 460)
f.state("A", 50, 190, init="left", final=True); f.state("B", 210, 60, final=True); f.state("C", 210, 300, final=True)
f.state("D", 380, 190, final=True); f.state("E", 380, 390, final=True); f.state("F", 540, 300, final=True); f.state("X", 540, 400, dead=True, label="∅")
f.edge("A", "B", "a"); f.edge("A", "C", "b", lo=-10); f.loop("B", "a", "up"); f.edge("B", "C", "b")
f.edge("C", "D", "a", bend=14); f.edge("D", "C", "b", bend=14); f.edge("D", "B", "a"); f.edge("C", "E", "b", lo=-10)
f.edge("E", "F", "a"); f.edge("E", "X", "b"); f.edge("F", "B", "a", bend=90); f.edge("F", "C", "b", lo=-10, t=0.3); f.loop("X", "a,b", "down")
G["b_dfa"] = f.svg("big DFA")
f = FA(560, 160)
f.state("P", 70, 90, init="left", final=True, rx=34, label="A,B,D,F"); f.state("C", 230, 90, final=True); f.state("E", 370, 90, final=True); f.state("X", 510, 90, dead=True, label="∅")
f.loop("P", "a"); f.edge("P", "C", "b", bend=-12); f.edge("C", "P", "a", bend=-12); f.edge("C", "E", "b"); f.edge("E", "P", "a", bend=-60, lo=-10)
f.edge("E", "X", "b"); f.loop("X", "a,b")
G["b_min"] = f.svg("big minimal")
f = FA(650, 340)
f.state("A", 50, 170, init="left"); f.state("B", 175, 70); f.state("C", 175, 270)
for s, x, y in [("D", 320, 70), ("E", 320, 270), ("F", 460, 70), ("G", 460, 270), ("H", 600, 120), ("I", 600, 230)]:
    f.state(s, x, y, final=True)
f.edge("A", "B", "a"); f.edge("A", "C", "b", lo=-10); f.edge("B", "C", "b", bend=14); f.edge("C", "B", "a", bend=14)
f.edge("B", "D", "a"); f.edge("C", "E", "b", lo=-10); f.loop("D", "a", "up"); f.loop("E", "b", "down")
f.edge("D", "F", "b", bend=-12); f.edge("F", "D", "a", bend=-12); f.edge("E", "G", "a", bend=12); f.edge("G", "E", "b", bend=12)
f.edge("F", "H", "b"); f.edge("G", "I", "a", lo=-10); f.loop("H", "b", "up"); f.loop("I", "a", "down")
f.edge("H", "I", "a", bend=14); f.edge("I", "H", "b", bend=14)
G["s79_dfa"] = f.svg("slide 79 DFA")
G["enfa"] = SD["enfa"]; G["edfa"] = SD["edfa"]

CSS = r"""
:root{--ink:#1f2a6b;--pink:#c2185b;--teal:#1a8fa3}
*{box-sizing:border-box}
body{margin:0;background:#f6f7fb;color:#1d2233;font:14px/1.5 "Segoe UI",system-ui,Roboto,Arial,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:18px 16px 50px}
header{background:var(--ink);color:#fff;border-radius:12px;padding:16px 20px}
header h1{margin:0;font-size:22px} header p{margin:4px 0 0;opacity:.85}
h2{color:var(--ink);font-size:19px;margin:26px 0 10px;padding-left:10px;border-left:6px solid var(--teal)}
.ex{background:#fff;border:1px solid #dfe3ee;border-radius:12px;padding:12px 16px;margin:12px 0;break-inside:avoid}
.ex h3{margin:0 0 6px;color:var(--pink);font-size:16px}
.meta{font-size:12px;color:#5b6275;margin-bottom:6px}
.badge{display:inline-block;border-radius:99px;padding:0 8px;font-size:11.5px;font-weight:700;color:#fff;background:var(--teal);margin-right:4px}
.badge.must{background:var(--pink)} .badge.src{background:#5b6275}
ol,ul{margin:4px 0 4px 20px;padding:0} li{margin:3px 0}
code,.m{font-family:Consolas,"DejaVu Sans Mono",monospace;font-size:12.5px;background:#eef1f8;padding:0 4px;border-radius:4px}
table{border-collapse:collapse;margin:6px 0;font-size:13px}
th,td{border:1px solid #cfd5e6;padding:3px 9px;text-align:center}
th{background:#fde8ef;color:var(--ink)} td.s{background:#fde8ef;font-weight:600}
.box td.s{outline:2px solid var(--ink);outline-offset:-2px}
.steps{font-family:Consolas,"DejaVu Sans Mono",monospace;font-size:12.5px;background:#f3f6fd;border-radius:8px;padding:6px 10px;white-space:pre-wrap;margin:6px 0}
.fig{text-align:center;margin:6px 0}
.sl{font:600 12px Arial,sans-serif;fill:#1f2a6b}.el{font:600 12.5px Arial,sans-serif;fill:#c2185b}.nt{font:italic 11px Arial,sans-serif;fill:#5b6275}
.ans{color:#0b7a3e;font-weight:600}
.tip{background:#fff8e6;border-left:4px solid #e0a100;padding:5px 10px;border-radius:6px;font-size:13px;margin:6px 0}
.plan td,.plan th{text-align:left}
.sol{background:#fbfffc;border-color:#bfe3cc}
.sol h3{color:#0b7a3e}
.row{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-start}.row>div{flex:1 1 260px;min-width:0}
@media print{@page{size:A4;margin:10mm} body{background:#fff;font-size:12px} .wrap{padding:0} .pb{break-before:page} h2{break-after:avoid}}
"""

BODY = r"""
<header>
<h1>Automata — DS preparation</h1>
<p>Dr-Ing Ines Baccouche · 7 exercises covering every chapter · built from her Tutorial 1 (series.pdf), her slides and the class board · solutions at the end</p>
</header>

<h2>How to use this in the time you have</h2>
<table class="plan">
<tr><th>Order</th><th>Exercise</th><th>Covers</th><th>Time</th></tr>
<tr><td>1–3</td><td>E1, E2, E3</td><td>RegEx notation, true/false, language → RegEx + DFA</td><td>done ✔</td></tr>
<tr><td>4 ★</td><td>E4 — aba / bab / bbb</td><td>explain a language, Glushkov, DFA, complement</td><td>20 min</td></tr>
<tr><td>5 ★</td><td>E5 — read 4 automata</td><td>automaton → language, deterministic / complete</td><td>15 min</td></tr>
<tr><td>6 ★★</td><td>E6 — (a|ba|bba)*(b|bb|ε)</td><td>the big one: Glushkov → NFA with ε column → DFA → minimisation → drawings, traces</td><td>35 min</td></tr>
<tr><td>7 ★★</td><td>E7 — slide 79 (ε-NFA)</td><td>NFA table with ε column → DFA table → drawing → minimal DFA</td><td>25 min</td></tr>
</table>
<div class="tip">★ = do these first: they are the long DS-style questions. Work on paper, in her format (tables, Step0…, δ'([q0],a) = …). When stuck, open the cheat sheet section given in each exercise, then continue. Check the solution only after you finish the exercise.</div>

<h2>Exercises</h2>

<div class="ex"><h3>E1 — Numbers (Ch1, RegEx notation)</h3>
<div class="meta"><span class="badge src">Tutorial 1 · Ex 1</span> Cheat sheet: Ch1 §3 notation</div>
Alphabet {0,…,9}, d = [0-9]. Give the RegEx of:
<ol><li>numbers of exactly three digits;</li><li>numbers that can be divided by 5;</li><li>numbers that start with 4 and end with 7;</li><li>numbers of three digits that do not start with 0.</li></ol>
</div>

<div class="ex"><h3>E2 — True or false? (Ch1)</h3>
<div class="meta"><span class="badge src">slides 27–29 style</span> Cheat sheet: Ch1 §6 and §7</div>
<ol><li>True or false? Justify with a rule (true) or a counter-example word (false):
<br><code>(a*b)* = (a|b)*b</code> · <code>(ab)*a = a(ba)*</code> · <code>(a|b)* = (a*b*)*</code> · <code>(ab)* = a*b*</code></li>
<li>R = <code>(a|b)*bb</code> and S = <code>b(a|b)*</code>. Give a word: in R not in S · in S not in R · in both · in neither.</li></ol>
</div>

<div class="ex"><h3>E3 — RegEx and automaton of a language (Ch1 + Ch2)</h3>
<div class="meta"><span class="badge src">Tutorial 1 · Ex 4</span> Cheat sheet: Ch1 §4, Ch3 §3</div>
Over {a,b}, give the RegEx <b>and</b> a deterministic automaton of the words containing:
<ol><li>at least one a;</li><li>at most one a;</li><li>an even number of a.</li></ol>
</div>

<div class="ex"><h3>E4 — Explain and build (Ch1 + Ch2 + Ch3)</h3>
<div class="meta"><span class="badge must">★ DS</span><span class="badge src">Tutorial 1 · Ex 2</span> Cheat sheet: Glushkov, Ch3 §4 (flip)</div>
For each language, explain it in words and draw an automaton that recognises it using a construction method:
<ol><li>L denoted by <code>(aba)|(bab)</code>;</li><li>L denoted by <code>(aba)*|(bab)*</code>;</li>
<li>L = { u ∈ {a,b}* | u contains the factor bbb };</li><li>L = { u ∈ {a,b}* | u does not contain the factor bbb }. Also give its RegEx.</li></ol>
</div>

<div class="ex"><h3>E5 — Give the language of each automaton (Ch2 + Ch3)</h3>
<div class="meta"><span class="badge must">★ DS</span><span class="badge src">Tutorial 1 · Ex 6</span> Cheat sheet: Ch3 §1, Extra A (Arden)</div>
For each automaton: describe the language in words, give a RegEx, and say if it is deterministic and complete.
<p style="margin:6px 0 0"><b>a)</b></p><div class="fig">{{s6a}}</div>
<p style="margin:6px 0 0"><b>b)</b> alphabet {a,b,c}</p><div class="fig">{{s6b}}</div>
<p style="margin:6px 0 0"><b>c)</b></p><div class="fig">{{s6c}}</div>
<p style="margin:6px 0 0"><b>d)</b></p><div class="fig">{{s6d}}</div>
<p style="margin:6px 0 0"><b>e)</b> What is the link between c) and d)?</p>
</div>

<div class="ex"><h3>E6 — The big one: (a | ba | bba)* (b | bb | ε)</h3>
<div class="meta"><span class="badge must">★★ DS</span><span class="badge src">slide 61 + class board</span> Cheat sheet: Glushkov, NFA→DFA, Minimisation</div>
<ol>
<li><b>Glushkov:</b> number the letters (ε gets its own number, like on the board), give start letters, end letters and the successors table.</li>
<li><b>NFA:</b> write the transition table with columns <b>a | b | ε</b>. Is it deterministic? Why?</li>
<li><b>NFA → DFA:</b> convert it (start = 0 + its ε cell). Give the DFA table and draw it.</li>
<li><b>Minimise</b> the DFA (Step0, Step1…) and draw the minimal automaton.</li>
<li>Trace <b>abbab</b> and <b>abbba</b> on the minimal DFA. What is the language, in one sentence?</li>
</ol>
</div>

<div class="ex"><h3>E7 — Slide 79: create the corresponding DFA (NFA → DFA)</h3>
<div class="meta"><span class="badge must">★★ DS</span><span class="badge src">slide 79 (class photo)</span> Cheat sheet: NFA→DFA</div>
<div class="fig">{{enfa}}</div>
<ol>
<li>Write the NFA table with columns <b>a | b | ε</b>. First row: <span class="m">→0 | – | – | {1,4}</span></li>
<li>Convert it to a DFA (start = 0 + its ε cell). Give the DFA table, mark the new states and the finals.</li>
<li>Draw the DFA.</li>
<li>Bonus: minimise it. What is the language?</li>
</ol>
</div>

<h2 class="pb">Solutions</h2>

<div class="ex sol"><h3>E1</h3>
<ol><li><code>\d{3}</code> = <code>ddd</code></li><li><code>\d*(0|5)</code> — her slide: (0-9)*(0|5). Any number ending with 0 or 5.</li>
<li><code>4\d*7</code> (her slide: <code>4.*7</code>) — 47 ✔, 4 ✘, 417 ✔</li><li><code>[1-9]\d{2}</code></li></ol>
</div>

<div class="ex sol"><h3>E2</h3>
<ol><li><code>(a*b)* = (a|b)*b</code> → <span class="ans">False</span>: ε ∈ (a*b)* but ε ∉ (a|b)*b (must end with b).<br>
<code>(ab)*a = a(ba)*</code> → <span class="ans">True</span>: sliding rule (rs)*r = r(sr)*. Both = {a, aba, ababa, …}.<br>
<code>(a|b)* = (a*b*)*</code> → <span class="ans">True</span>: every word is a sequence of a's and b's, each letter is one a*b* block.<br>
<code>(ab)* = a*b*</code> → <span class="ans">False</span>: a ∈ a*b* but a ∉ (ab)* (also aab).</li>
<li>R = ends with bb, S = starts with b.<br>In R not S: <span class="ans">abb</span> · in S not R: <span class="ans">b</span> · in both: <span class="ans">bb</span> · in neither: <span class="ans">a</span></li></ol>
</div>

<div class="ex sol"><h3>E3</h3>
<div class="row">
<div><b>1. At least one a:</b> <code>b*a(a|b)*</code><div class="fig">{{e3a}}</div></div>
<div><b>2. At most one a:</b> <code>b* | b*ab*</code> = <code>b*(a|ε)b*</code><div class="fig">{{e3b}}</div><p style="font-size:12px;margin:0">q2 = dead state (a second a).</p></div>
<div><b>3. Even number of a:</b> <code>b*(ab*ab*)*</code> = <code>(b|ab*a)*</code><div class="fig">{{e3c}}</div><p style="font-size:12px;margin:0">q0 = even, q1 = odd. ε is accepted (0 a's).</p></div>
</div>
</div>

<div class="ex sol"><h3>E4</h3>
<p><b>1.</b> L = {aba, bab}: exactly two words. Glushkov: <span class="m">a1 b2 a3 | b4 a5 b6</span>; First = {a1, b4}, Last = {a3, b6} ⇒ F = {3, 6}; successors a1→b2, b2→a3, b4→a5, a5→b6.</p>
<div class="fig">{{e4a}}</div>
<p><b>2.</b> L = repetitions of aba only, or repetitions of bab only: {ε, aba, abaaba, …, bab, babbab, …}. No mixing: ababab (= aba·bab) ✘ — same idea as a*|b*.<br>
Glushkov: <span class="m">(a1 b2 a3)* | (b4 a5 b6)*</span>. Nullable ⇒ <b>0 ∈ F</b>. F = {0, 3, 6}. Successors: a1→b2, b2→a3, <b>a3→a1</b> (star), b4→a5, a5→b6, <b>b6→b4</b> (star).</p>
<div class="fig">{{e4b}}</div>
<p><b>3.</b> Contains bbb: <code>(a|b)*bbb(a|b)*</code>. State = number of b's read in a row (A: 0, B: 1, C: 2, D: bbb found). An a sends back to A.</p>
<div class="fig">{{e4c}}</div>
<p><b>4.</b> Complement of 3: the DFA is complete ⇒ <b>flip the states</b> (A, B, C final, D non-final = dead).</p>
<div class="fig">{{e4d}}</div>
<p>RegEx: <code>(a|ba|bba)*(ε|b|bb)</code> — exactly the class exercise of slide 61! Blocks a, ba, bba never make 3 b's; the end adds at most bb.</p>
</div>

<div class="ex sol"><h3>E5</h3>
<p><b>a)</b> Words over {a,b} that contain <b>ba</b>: <code>(a|b)*ba(a|b)*</code> = <code>a*bb*a(a|b)*</code>. Deterministic and complete.</p>
<p><b>b)</b> What each state remembers: 2 = last letter a (or "bcc"), 3 = last letter b, 4 = ends with "bc". A c is only possible from 3 or 4, so <b>every c comes right after b or after "bc"</b>, never after a, and at most 2 c in a row.<br>
Language: words over {a,b,c} that <b>start with a</b>, <b>end with bc</b>, where every block of c's follows a b and has length 1 or 2:
<code>a(a|b|bc|bcc)*bc</code> = <code>a(a|b(ε|c|cc))*bc</code>. Words: abc, aabc, abbc, abcbc, abccbc · ✘ acbc (c after a), abccc.<br>
Unambiguous, but <b>not complete</b> (1 has no b, c; 2 has no c) ⇒ by her definition it is <b>not a DFA</b> until you add a dead state for the missing arrows.</p>
<p><b>c)</b> Number of b <b>different from 2</b> (0, 1, or at least 3): <code>a* | a*ba* | a*ba*ba*b(a|b)*</code>. Deterministic and complete.</p>
<p><b>d)</b> <b>Exactly two b</b>: <code>a*ba*ba*</code>. State 4 is a dead state. Deterministic and complete.</p>
<p><b>e)</b> Same automaton, final and non-final states flipped ⇒ d) is the <b>complement</b> of c).</p>
<div class="tip">Method for any automaton: find what each state "remembers" (number of b's, last letter…), then follow start → final paths: loop = *, choice = |.</div>
</div>


<div class="ex sol"><h3>E6</h3>
<p><b>1. Glushkov</b> — <span class="m">(a1 | b2 a3 | b4 b5 a6)* (b7 | b8 b9 | ε10)</span> · states 0 … 10</p>
<div class="row"><div>
<table><tr><th></th><th>successors</th></tr>
<tr><td class="s">ɸ</td><td>a1 b2 b4 b7 b8 ε10</td></tr>
<tr><td class="s">a1</td><td>a1 b2 b4 b7 b8 ε10</td></tr>
<tr><td class="s">b2</td><td>a3</td></tr>
<tr><td class="s">a3</td><td>a1 b2 b4 b7 b8 ε10</td></tr>
<tr><td class="s">b4</td><td>b5</td></tr>
<tr><td class="s">b5</td><td>a6</td></tr>
<tr><td class="s">a6</td><td>a1 b2 b4 b7 b8 ε10</td></tr>
<tr class="box"><td class="s">b7</td><td>ɸ</td></tr>
<tr><td class="s">b8</td><td>b9</td></tr>
<tr class="box"><td class="s">b9</td><td>ɸ</td></tr>
<tr class="box"><td class="s">ε10</td><td>ɸ</td></tr>
</table></div>
<div>
<ul>
<li><b>Start letters</b> = a1, b2, b4 (start of a block) and b7, b8, ε10 (the star can be empty).</li>
<li><b>End letters</b> = b7, b9, ε10 ⇒ <b>F = {7, 9, 10}</b>.</li>
<li>a1, a3, a6 end a block of the star ⇒ they loop back to a1, b2, b4 <b>or</b> leave the star to b7, b8, ε10.</li>
</ul>
<p><b>2. NFA table</b> (rows 0, 1, 3, 6 are identical):</p>
<table><tr><th>δ</th><th>a</th><th>b</th><th>ε</th></tr>
<tr><td class="s">→0</td><td>1</td><td>{2,4,7,8}</td><td>10</td></tr>
<tr><td class="s">1</td><td>1</td><td>{2,4,7,8}</td><td>10</td></tr>
<tr><td class="s">2</td><td>3</td><td>–</td><td>–</td></tr>
<tr><td class="s">3</td><td>1</td><td>{2,4,7,8}</td><td>10</td></tr>
<tr><td class="s">4</td><td>–</td><td>5</td><td>–</td></tr>
<tr><td class="s">5</td><td>6</td><td>–</td><td>–</td></tr>
<tr><td class="s">6</td><td>1</td><td>{2,4,7,8}</td><td>10</td></tr>
<tr><td class="s">*7</td><td>–</td><td>–</td><td>–</td></tr>
<tr><td class="s">8</td><td>–</td><td>9</td><td>–</td></tr>
<tr><td class="s">*9</td><td>–</td><td>–</td><td>–</td></tr>
<tr><td class="s">*10</td><td>–</td><td>–</td><td>–</td></tr>
</table>
<p>Not deterministic: b goes to 4 states at once, there are ε-arrows, and many cells are empty.</p>
</div></div>
<div class="fig">{{b_nfa}}</div>
<p class="cap" style="text-align:center;font-size:12px;color:#5b6275">Drawing: all exits of 0 are drawn; 1, 3 and 6 have <b>the same exits as 0</b> (a→1, b→2,4,7,8, ε→10) — see the table.</p>

<p><b>3. NFA → DFA.</b> Start = 0 + its ε cell = <b>[0,10]</b>. After each move, add the ε cell of the states you land on (1, 3, 6 → add 10).</p>
<div class="steps">δ'([0,10],a)    = {1}       + ε of 1 → [1,10]      ← new
δ'([0,10],b)    = {2,4,7,8}             → [2,4,7,8]   ← new
δ'([1,10],a)    = {1}       + 10        → [1,10]
δ'([1,10],b)    = {2,4,7,8}             → [2,4,7,8]
δ'([2,4,7,8],a) = 2→3       + ε of 3 → [3,10]      ← new
δ'([2,4,7,8],b) = 4→5, 8→9              → [5,9]       ← new
δ'([3,10],a)    = {1} + 10  → [1,10]    δ'([3,10],b) = [2,4,7,8]
δ'([5,9],a)     = 5→6       + ε of 6 → [6,10]      ← new
δ'([5,9],b)     = nothing               → ∅ (dead)
δ'([6,10],a)    = [1,10]                δ'([6,10],b) = [2,4,7,8]</div>
<div class="row"><div>
<table><tr><th>δ'</th><th>a</th><th>b</th></tr>
<tr><td class="s">→*A = [0,10]</td><td>B</td><td>C</td></tr>
<tr><td class="s">*B = [1,10]</td><td>B</td><td>C</td></tr>
<tr><td class="s">*C = [2,4,7,8]</td><td>D</td><td>E</td></tr>
<tr><td class="s">*D = [3,10]</td><td>B</td><td>C</td></tr>
<tr><td class="s">*E = [5,9]</td><td>F</td><td>∅</td></tr>
<tr><td class="s">*F = [6,10]</td><td>B</td><td>C</td></tr>
<tr><td class="s">∅</td><td>∅</td><td>∅</td></tr>
</table>
<p style="font-size:12.5px">Final = contains 7, 9 or 10 ⇒ every state except ∅.</p></div></div>
<div class="fig">{{b_dfa}}</div>

<p><b>4. Minimisation</b></p>
<div class="steps">Step0: (A,B,C,D,E,F) (∅)                      finals / non-finals
Step1: E –b→ ∅, the others –b→ a final  ⇒ (A,B,C,D,F) (E) (∅)
Step2: C –b→ E, A,B,D,F –b→ C            ⇒ (A,B,D,F) (C) (E) (∅)
Step3: A,B,D,F: a → (A,B,D,F), b → (C)   ⇒ same ⇒ stable
fusion: {A,B,D,F} = "A,B,D,F"   C   E   ∅</div>
<div class="row"><div>
<table><tr><th>δ</th><th>a</th><th>b</th></tr>
<tr><td class="s">→*(A,B,D,F)</td><td>(A,B,D,F)</td><td>C</td></tr>
<tr><td class="s">*C</td><td>(A,B,D,F)</td><td>E</td></tr>
<tr><td class="s">*E</td><td>(A,B,D,F)</td><td>∅</td></tr>
<tr><td class="s">∅</td><td>∅</td><td>∅</td></tr>
</table></div></div>
<div class="fig">{{b_min}}</div>
<p>Meaning of each state: "A,B,D,F" = 0 b's in a row · C = 1 b · E = 2 b's in a row · ∅ = bbb was read.</p>
<p><b>5.</b> abbab: (A,B,D,F) –a→ (A,B,D,F) –b→ C –b→ E –a→ (A,B,D,F) –b→ C ✔ · abbba: … –b→ C –b→ E –b→ ∅ ✘</p>
<p><b>Language:</b> all words over {a,b} that <b>never contain bbb</b> — the same answer as E4.4!</p>
<div class="tip">On the board she minimised the Glushkov table directly (groups {7,9,10} {0,1,3,6} {8} {2} {4} {5}). If the question says "minimise" right after Glushkov, write her version (in the cheat sheet). If it says "DFA, then minimise", write this one.</div>
</div>

<div class="ex sol"><h3>E7</h3>
<div class="row"><div>
<p><b>1. NFA table</b></p>
<table><tr><th>δ</th><th>a</th><th>b</th><th>ε</th></tr>
<tr><td class="s">→0</td><td>–</td><td>–</td><td>{1,4}</td></tr>
<tr><td class="s">1</td><td>{1,2}</td><td>1</td><td>–</td></tr>
<tr><td class="s">2</td><td>3</td><td>–</td><td>–</td></tr>
<tr><td class="s">*3</td><td>3</td><td>3</td><td>–</td></tr>
<tr><td class="s">4</td><td>4</td><td>{4,5}</td><td>–</td></tr>
<tr><td class="s">5</td><td>–</td><td>6</td><td>–</td></tr>
<tr><td class="s">*6</td><td>6</td><td>6</td><td>–</td></tr>
</table></div>
<div><p><b>2. DFA table</b> — start = 0 + its ε cell = <b>[0,1,4]</b></p>
<table><tr><th>δ'</th><th>a</th><th>b</th></tr>
<tr><td class="s">→A = [0,1,4]</td><td>[1,2,4] = B ← new</td><td>[1,4,5] = C ← new</td></tr>
<tr><td class="s">B = [1,2,4]</td><td>[1,2,3,4] = D ← new</td><td>C</td></tr>
<tr><td class="s">C = [1,4,5]</td><td>B</td><td>[1,4,5,6] = E ← new</td></tr>
<tr><td class="s">*D = [1,2,3,4]</td><td>D</td><td>[1,3,4,5] = F ← new</td></tr>
<tr><td class="s">*E = [1,4,5,6]</td><td>[1,2,4,6] = G ← new</td><td>E</td></tr>
<tr><td class="s">*F = [1,3,4,5]</td><td>D</td><td>[1,3,4,5,6] = H ← new</td></tr>
<tr><td class="s">*G = [1,2,4,6]</td><td>[1,2,3,4,6] = I ← new</td><td>E</td></tr>
<tr><td class="s">*H = [1,3,4,5,6]</td><td>I</td><td>H</td></tr>
<tr><td class="s">*I = [1,2,3,4,6]</td><td>I</td><td>H</td></tr>
</table>
<p style="font-size:12.5px">Example cell: B with a → 1→{1,2}, 2→3, 4→4 ⇒ [1,2,3,4]. Final = contains 3 or 6.</p></div></div>
<p><b>3. Drawing</b></p>
<div class="fig">{{s79_dfa}}</div>
<p><b>4. Minimal DFA</b>: Step0: (D,E,F,G,H,I) (A,B,C) · Step1: B –a→ final, C –b→ final, A never ⇒ (D…I) (A) (B) (C) · D…I only go to D…I ⇒ fusion into one final state, drawn as "F" below (= D, E, F, G, H, I together).</p>
<div class="fig">{{edfa}}</div>
<p>A = start · B = last letter a · C = last letter b · F = found aa or bb. <b>Language: words that contain aa or bb</b> = <code>(a|b)*(aa|bb)(a|b)*</code>.</p>
</div>
"""

html = BODY
for k, v in G.items():
    html = html.replace("{{" + k + "}}", v)
assert "{{" not in html, html[html.index("{{"):][:30]
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Automata DS Prep</title><style>{CSS}</style></head><body><div class="wrap">{html}</div></body></html>"""
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write(page)
print("wrote", OUT)
