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
f.edge("1", "2", "a"); f.loop("2", "a,c", "down"); f.edge("2", "3", "b", bend=14); f.edge("3", "2", "a", bend=14)
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
<p>Dr-Ing Ines Baccouche · 9 exercises covering every chapter · built from her Tutorial 1 (series.pdf), her slides and the class board · solutions at the end</p>
</header>

<h2>How to use this in the time you have</h2>
<table class="plan">
<tr><th>Order</th><th>Exercise</th><th>Covers</th><th>Time</th></tr>
<tr><td>1 ★</td><td>E5 — (a|b)*abb</td><td>Glushkov → NFA → DFA → minimal (3 chapters in 1)</td><td>20 min</td></tr>
<tr><td>2 ★</td><td>E4 — aba / bab / bbb</td><td>explain a language, Glushkov, DFA, complement</td><td>20 min</td></tr>
<tr><td>3 ★</td><td>E7 — read 4 automata</td><td>automaton → language, deterministic / complete</td><td>15 min</td></tr>
<tr><td>4 ★</td><td>E8 — minimise</td><td>unreachable state, Step0/Step1…, fusion</td><td>15 min</td></tr>
<tr><td>5 ★</td><td>E9 — NFA → DFA (+ ε)</td><td>subset construction, ε-closure, complement</td><td>15 min</td></tr>
<tr><td>6</td><td>E3 — at least / at most / even</td><td>language → RegEx + DFA</td><td>10 min</td></tr>
<tr><td>7</td><td>E2 — true or false</td><td>RegEx equalities, counter-examples</td><td>10 min</td></tr>
<tr><td>8</td><td>E6 — table → automaton</td><td>drawing, traces, properties</td><td>10 min</td></tr>
<tr><td>9</td><td>E1 — numbers</td><td>RegEx notation \d, {n}</td><td>5 min</td></tr>
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

<div class="ex"><h3>E5 — The complete chain: (a|b)*abb (Ch2 + Ch3)</h3>
<div class="meta"><span class="badge must">★ DS</span><span class="badge src">Tutorial 1 · Ex 3</span> Cheat sheet: Glushkov, NFA→DFA, Minimisation</div>
<ol><li>Build the Glushkov automaton of <code>(a|b)*abb</code> (numbering, successors table, F, drawing).</li>
<li>Is it deterministic? Justify.</li>
<li>Convert it to a DFA (subset construction).</li>
<li>Is your DFA minimal? Prove it with the Step method.</li>
<li>Trace <b>aabb</b> and <b>abab</b> on the DFA.</li></ol>
</div>

<div class="ex"><h3>E6 — From a table to an automaton (Ch2)</h3>
<div class="meta"><span class="badge src">Tutorial 1 · Ex 5</span> Cheat sheet: Ch2 §1, §5</div>
<div class="row"><div>
<table><tr><th></th><th>a</th><th>b</th></tr>
<tr><td class="s">0</td><td>1</td><td>0</td></tr><tr><td class="s">1</td><td>0</td><td>2</td></tr>
<tr><td class="s">2</td><td>3</td><td>0</td></tr><tr><td class="s">3</td><td>1</td><td>2</td></tr></table></div>
<div><ol><li>Draw the automaton (0 initial, 2 final).</li><li>Is it complete? Unambiguous? Deterministic?</li>
<li>Are <b>ab</b>, <b>aab</b>, <b>abab</b>, <b>abb</b> accepted? Write the traces.</li><li>Is it minimal? (Step method)</li></ol></div></div>
</div>

<div class="ex"><h3>E7 — Give the language of each automaton (Ch2 + Ch3)</h3>
<div class="meta"><span class="badge must">★ DS</span><span class="badge src">Tutorial 1 · Ex 6</span> Cheat sheet: Ch3 §1, Extra A (Arden)</div>
For each automaton: describe the language in words, give a RegEx, and say if it is deterministic and complete.
<p style="margin:6px 0 0"><b>a)</b></p><div class="fig">{{s6a}}</div>
<p style="margin:6px 0 0"><b>b)</b> alphabet {a,b,c}</p><div class="fig">{{s6b}}</div>
<p style="font-size:12px;color:#5b6275;margin:0">The loop label on state 2 is unreadable on the scan; a,c is the reading that makes the automaton consistent.</p>
<p style="margin:6px 0 0"><b>c)</b></p><div class="fig">{{s6c}}</div>
<p style="margin:6px 0 0"><b>d)</b></p><div class="fig">{{s6d}}</div>
<p style="margin:6px 0 0"><b>e)</b> What is the link between c) and d)?</p>
</div>

<div class="ex"><h3>E8 — Minimise (Ch2)</h3>
<div class="meta"><span class="badge must">★ DS</span><span class="badge src">slides 60–61 style</span> Cheat sheet: Minimisation</div>
<div class="row"><div>
<table><tr><th></th><th>a</th><th>b</th></tr>
<tr><td class="s">→1</td><td>2</td><td>5</td></tr><tr><td class="s">2</td><td>6</td><td>3</td></tr>
<tr><td class="s">*3</td><td>6</td><td>5</td></tr><tr><td class="s">4</td><td>2</td><td>7</td></tr>
<tr><td class="s">5</td><td>6</td><td>1</td></tr><tr><td class="s">6</td><td>2</td><td>7</td></tr>
<tr><td class="s">*7</td><td>2</td><td>1</td></tr></table></div>
<div><ol><li>Remove the unreachable states.</li><li>Minimise (write every Step).</li><li>Draw the minimal automaton.</li><li>Give the language (words + RegEx).</li></ol></div></div>
</div>

<div class="ex"><h3>E9 — NFA → DFA, ε, complement (Ch3)</h3>
<div class="meta"><span class="badge must">★ DS</span><span class="badge src">slides 75–79 style</span> Cheat sheet: NFA→DFA, ε-closure</div>
<div class="fig">{{s9}}</div>
<ol><li>Why is this automaton an NFA? Give its transition table.</li>
<li>Convert it to a DFA. What is the language?</li>
<li>Give an automaton for the words that do <b>not</b> end with aba.</li></ol>
<p style="margin:6px 0 0"><b>4.</b> Same question 2 for this ε-NFA (compute the ε-closures first):</p>
<div class="fig">{{s9e}}</div>
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
<p><b>1.</b> <span class="m">(a1 | b2)* a3 b4 b5</span> · First = {a1, b2, a3} · Last = {b5} · not nullable ⇒ <b>F = {5}</b></p>
<div class="row"><div>
<table><tr><th></th><th>successors</th></tr>
<tr><td class="s">ɸ</td><td>a1, b2, a3</td></tr><tr><td class="s">a1</td><td>a1, b2, a3</td></tr>
<tr><td class="s">b2</td><td>a1, b2, a3</td></tr><tr><td class="s">a3</td><td>b4</td></tr>
<tr><td class="s">b4</td><td>b5</td></tr><tr class="box"><td class="s">b5</td><td>ɸ</td></tr></table></div>
<div><div class="fig">{{e5g}}</div></div></div>
<p><b>2.</b> Not deterministic: from 0 (and 1, 2), reading a goes to <b>1 and 3</b> ⇒ ambiguity ⇒ NFA. Also 3, 4 have no a-transition.</p>
<p><b>3.</b> Rows 0, 1, 2 are identical ⇒ call them S. Subset construction:</p>
<div class="steps">δ'([S],a)   = [S,3]  ← new        δ'([S],b)   = [S]
δ'([S,3],a) = [S,3]               δ'([S,3],b) = [S,4]  ← new
δ'([S,4],a) = [S,3]               δ'([S,4],b) = [S,5]  ← new
δ'([S,5],a) = [S,3]               δ'([S,5],b) = [S]
A = [S]   B = [S,3]   C = [S,4]   *D = [S,5]  (contains 5)</div>
<div class="fig">{{e5d}}</div>
<p><b>4.</b> Step0: (D) (A,B,C) · Step1: C –b→ D final, A and B –b→ non-final ⇒ (D) (C) (A,B) · Step2: B –b→ C, A –b→ A ⇒ (D) (C) (B) (A). All separated ⇒ <span class="ans">minimal (4 states)</span>.</p>
<p><b>5.</b> aabb: A –a→ B –a→ B –b→ C –b→ D ✔ accepted · abab: A –a→ B –b→ C –a→ B –b→ C ✘ (C not final).</p>
</div>

<div class="ex sol"><h3>E6</h3>
<div class="fig">{{e6}}</div>
<ol><li>See drawing (0 loops on b).</li>
<li>Every state has exactly one a and one b ⇒ <b>complete</b> and <b>unambiguous</b> ⇒ <b>deterministic</b>.</li>
<li>ab: 0→1→2 ✔ · aab: 0→1→0→0 ✘ · abab: 0→1→2→3→2 ✔ · abb: 0→1→2→0 ✘</li>
<li>Step0: (2) (0,1,3) · Step1: 1 –b→ 2 and 3 –b→ 2 (final), 0 –b→ 0 ⇒ (2) (0) (1,3) · Step2: 1 –a→ 0, 3 –a→ 1: different groups ⇒ (2) (0) (1) (3) ⇒ <span class="ans">already minimal</span>.</li></ol>
</div>

<div class="ex sol"><h3>E7</h3>
<p><b>a)</b> Words over {a,b} that contain <b>ba</b>: <code>(a|b)*ba(a|b)*</code> = <code>a*bb*a(a|b)*</code>. Deterministic and complete.</p>
<p><b>b)</b> Words over {a,b,c} that <b>start with a and end with bc</b>: <code>a(a|b|c)*bc</code>. State 3 = last letter b, 4 = ends with bc. Deterministic, <b>not complete</b> (state 1 has no b, c ⇒ add a dead state).</p>
<p><b>c)</b> Number of b <b>different from 2</b> (0, 1, or at least 3): <code>a* | a*ba* | a*ba*ba*b(a|b)*</code>. Deterministic and complete.</p>
<p><b>d)</b> <b>Exactly two b</b>: <code>a*ba*ba*</code>. State 4 is a dead state. Deterministic and complete.</p>
<p><b>e)</b> Same automaton, final and non-final states flipped ⇒ d) is the <b>complement</b> of c).</p>
<div class="tip">Method for any automaton: find what each state "remembers" (number of b's, last letter…), then follow start → final paths: loop = *, choice = |.</div>
</div>

<div class="ex sol"><h3>E8</h3>
<p><b>1.</b> Nothing goes to 4 ⇒ 4 is unreachable ⇒ delete it.</p>
<div class="steps">Step0: (3,7) (1,2,5,6)
Step1: 2 –b→ 3 and 6 –b→ 7 (final); 1 –b→ 5, 5 –b→ 1 (non-final)
       ⇒ (3,7) (2,6) (1,5)
Step2: 1: a→2, b→5   5: a→6, b→1   ⇒ same groups
       2: a→6, b→3   6: a→2, b→7   ⇒ same groups
       3: a→6, b→5   7: a→2, b→1   ⇒ same groups
       stable ⇒ fusion: {1,5} {2,6} {3,7}</div>
<div class="fig">{{e8}}</div>
<p><b>4.</b> "1,5" = nothing useful, "2,6" = last letter a, "3,7" = ends with ab. Language: words ending with <b>ab</b>: <code>(a|b)*ab</code>.</p>
</div>

<div class="ex sol"><h3>E9</h3>
<div class="row"><div>
<p><b>1.</b> From q0, reading a goes to q0 <b>and</b> q1 ⇒ ambiguous ⇒ NFA.</p>
<table><tr><th></th><th>a</th><th>b</th></tr>
<tr><td class="s">→q0</td><td>{q0,q1}</td><td>q0</td></tr><tr><td class="s">q1</td><td>-</td><td>q2</td></tr>
<tr><td class="s">q2</td><td>q3</td><td>-</td></tr><tr><td class="s">*q3</td><td>-</td><td>-</td></tr></table></div>
<div><p><b>2.</b></p><div class="steps">δ'([q0],a) = [q0,q1] ← new
δ'([q0],b) = [q0]
δ'([q0,q1],a) = [q0,q1]
δ'([q0,q1],b) = [q0,q2] ← new
δ'([q0,q2],a) = [q0,q1,q3] ← new
δ'([q0,q2],b) = [q0]
δ'([q0,q1,q3],a) = [q0,q1]
δ'([q0,q1,q3],b) = [q0,q2]
A=[q0] B=[q0,q1] C=[q0,q2] *D=[q0,q1,q3]</div></div></div>
<div class="fig">{{e9}}</div>
<p>Language: words ending with <b>aba</b>: <code>(a|b)*aba</code>.</p>
<p><b>3.</b> The DFA is complete ⇒ flip: A, B, C final, D non-final. (Never flip the NFA directly!)</p>
<p><b>4.</b> ε-closure(q0) = {q0,q1,q2} · ε-closure(q1) = {q1,q2} · ε-closure(q2) = {q2}</p>
<div class="steps">A = {q0,q1,q2}* : a → {q0,q2} → closure {q0,q1,q2} = A
                b → {q1}    → closure {q1,q2} = B*
B = {q1,q2}*    : a → {q2} = C*      b → {q1} → {q1,q2} = B
C = {q2}*       : a → C              b → ϕ (dead)</div>
<div class="fig">{{e9e}}</div>
<p>All of A, B, C contain q2 ⇒ final. Language: <code>a*b*a*</code>.</p>
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
