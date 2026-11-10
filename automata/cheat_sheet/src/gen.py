import re, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from diagrams import D

OUT = "/home/user/study/automata/cheat_sheet/automata_cheat_sheet.html"

CSS = r"""
:root{--ink:#1f2a6b;--pink:#c2185b;--teal:#1a8fa3;--bg:#f6f7fb;--card:#fff;--line:#dfe3ee;--muted:#5b6275;--hl:#fff4cc}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:#1d2233;font:14px/1.5 "Segoe UI",system-ui,-apple-system,Roboto,Arial,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:20px 16px 60px}
header{background:var(--ink);color:#fff;border-radius:14px;padding:18px 22px;margin-bottom:16px}
header h1{margin:0;font-size:24px;letter-spacing:.2px}
header p{margin:4px 0 0;opacity:.85}
nav{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
nav a{color:#fff;background:rgba(255,255,255,.14);padding:3px 10px;border-radius:99px;text-decoration:none;font-size:12.5px}
h2{color:var(--ink);font-size:20px;margin:28px 0 10px;padding-left:10px;border-left:6px solid var(--teal)}
h2 small{color:var(--pink);font-weight:600;font-size:13px;margin-left:6px}
h3{color:var(--pink);font-size:15px;margin:0 0 6px}
.grid{columns:3 330px;column-gap:12px}
.grid>.card{margin:0 0 12px;display:block;width:100%}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;break-inside:avoid;page-break-inside:avoid;min-width:0}
.card.wide{column-span:all}
.style{background:#fff7fa;border:2px dashed var(--pink)}
.trap{background:#fff8e6;border-left:4px solid #e0a100}
.trap b{color:#a06b00}
ul,ol{margin:4px 0 4px 18px;padding:0}
li{margin:2px 0}
code,.m{font-family:"Cascadia Code",Consolas,"DejaVu Sans Mono",monospace;font-size:12.5px;background:#eef1f8;padding:0 4px;border-radius:4px}
.ans{color:#0b7a3e;font-weight:600}
table{border-collapse:collapse;margin:6px 0;font-size:13px}
.tbl-wrap{overflow-x:auto;max-width:100%}
th,td{border:1px solid #cfd5e6;padding:3px 8px;text-align:center}
th{background:#fde8ef;color:var(--ink)}
td.s{background:#fde8ef;font-weight:600;text-align:left}
tr.box td{outline:2px solid var(--ink);outline-offset:-2px}
table.l td{text-align:left}
table.pat td:first-child{white-space:nowrap;font-size:12px}
.sl{font:600 12px "Segoe UI",Arial,sans-serif;fill:#1f2a6b}
.el{font:600 12.5px "Segoe UI",Arial,sans-serif;fill:#c2185b}
.nt{font:italic 11px "Segoe UI",Arial,sans-serif;fill:#5b6275}
.fig{text-align:center;margin:6px 0}
.cap{font-size:12px;color:var(--muted);text-align:center;margin-top:-2px}
.steps{font-family:"Cascadia Code",Consolas,"DejaVu Sans Mono",monospace;font-size:13px;background:#f3f6fd;border-radius:8px;padding:6px 10px;white-space:pre-wrap;overflow-x:auto}
.k{color:var(--pink);font-weight:700}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px;align-items:start}
@media (max-width:640px){.two{grid-template-columns:1fr}header h1{font-size:20px}}
footer{margin-top:30px;color:var(--muted);font-size:12px;text-align:center}
@media print{
 @page{size:A4;margin:9mm}
 body{background:#fff;font-size:10.5px}
 .wrap{padding:0;max-width:none}
 header{padding:10px 14px} nav{display:none}
 h2{font-size:15px;margin:12px 0 6px;break-after:avoid}
 .grid{column-gap:7px}
 .grid>.card{margin-bottom:7px}
 .card{padding:7px 9px;border-radius:7px}
 table{font-size:10px} th,td{padding:1px 5px}
 code,.m,.steps{font-size:10px}
 .pb{break-before:page}
}
"""

BODY = r"""
<header>
 <h1>Language Theory &amp; Automata — Cheat Sheet</h1>
 <p>Dr-Ing Ines Baccouche · Pristini · 2nd year Applied AI · Chapters 1–3 (RegEx · Finite Automata, Glushkov &amp; Minimisation · DFA / NFA)</p>
 <nav><a href="#style">How she writes it</a><a href="#ch1">Ch1 RegEx</a><a href="#ch2">Ch2 Finite automata</a><a href="#glushkov">Glushkov</a><a href="#min">Minimisation</a><a href="#ch3">Ch3 DFA/NFA</a><a href="#subset">NFA→DFA</a><a href="#exam">Exam checklist</a></nav>
</header>

<div class="grid" id="style">
<div class="card style wide">
<h3>✍️ How she writes things in class — copy this format on the exam</h3>
<div class="two">
<ul>
 <li><b>Automaton</b> = 5-tuple <span class="m">A = (Q, V<sub>T</sub>, δ, q0, F)</span> — always write all 5 parts.</li>
 <li><b>States</b>: <span class="m">q0, q1…</span> or plain numbers <span class="m">0,1,2…</span> (Glushkov). Initial = incoming arrow (in tables <span class="m">→q0</span>). Final = <b>double circle</b> (in tables <span class="m">*q2</span> or a <b>box</b> around it).</li>
 <li><b>Transition table</b>: rows = states, columns = symbols, <span class="m">δ</span> in the corner. Empty cell = <span class="m">-</span> or <span class="m">ϕ</span>. Several targets = a set <span class="m">{q1, q2}</span>.</li>
 <li><b>NFA→DFA</b>: one line per computation: <span class="m">δ'([q1], 0) = [q1, q2] → new state</span>, then <b>rename</b> the new set (<span class="m">{q1,q2} = q3</span>) and redraw.</li>
</ul>
<ul>
 <li><b>Glushkov</b>: number every letter with an index: <span class="m">a1* b2 (a3|c4)* b5</span>. Then a <b>"successors" table</b> whose first row is <span class="m">ɸ</span> (= start letters). Final letters are <b>boxed</b>.</li>
 <li><b>Minimisation</b>: one line per step, groups in brackets:<br><span class="m">Step0: (6,7,8) (1,2,3,4,5)</span><br><span class="m">Step1: (6) (7,8) (1,2,3,4,5)</span> … then "<b>fusion</b> (same behaviour)".</li>
 <li><b>Identical rows</b> in a table → she <b>boxes them</b> → they are merged into one state.</li>
 <li><b>Merged state</b> is named with all its members: <span class="m">"1,2"</span>, <span class="m">"7,8"</span>, <span class="m">"0,1,3,6"</span>.</li>
</ul>
</div>
</div>
</div>

<!-- ================= CHAPTER 1 ================= -->
<h2 id="ch1">Chapter 1 — Language theory &amp; Regular Expressions</h2>
<div class="grid">
<div class="card">
<h3>1. Vocabulary</h3>
<ul>
 <li><b>Symbol</b>: <span class="m">a</span> · <b>Alphabet</b> Σ: finite set of symbols <span class="m">{a, b}</span></li>
 <li><b>String / word</b>: finite sequence of symbols <span class="m">aabb</span></li>
 <li><b>Language</b> L ⊆ Σ*: a set of strings <span class="m">{ε, ab, aabb, aaabbb, …}</span> (finite or infinite)</li>
 <li><b>ε</b> = empty string, <span class="m">|ε| = 0</span>; <span class="m">|01101| = 5</span></li>
 <li><b>Σ<sup>k</sup></b> = strings of length k. <span class="m">Σ<sup>0</sup> = {ε}</span>; Σ={0,1} ⇒ <span class="m">Σ<sup>2</sup> = {00,01,10,11}</span></li>
 <li><b>Σ*</b> = Σ<sup>0</sup> ∪ Σ<sup>1</sup> ∪ Σ<sup>2</sup> ∪ … (Kleene star, all strings)</li>
 <li><b>Σ<sup>+</sup></b> = Σ<sup>1</sup> ∪ Σ<sup>2</sup> ∪ … ⇒ <span class="m">Σ* = Σ<sup>+</sup> ∪ {ε}</span></li>
 <li><b>Concatenation</b>: x=01101, y=110 → xy = 01101110, yx = 11001101. <span class="m">εw = wε = w</span></li>
</ul>
</div>
<div class="card trap">
<h3>⚠ Classic traps</h3>
<ul>
 <li><b>∅ ≠ {ε}</b>: ∅ has <i>no</i> string, {ε} has <i>one</i> (the empty one).</li>
 <li><b>Σ ≠ Σ<sup>1</sup></b>: Σ contains <i>symbols</i>, Σ<sup>1</sup> contains <i>strings</i> of length 1.</li>
 <li>xy ≠ yx in general (concatenation is not commutative).</li>
 <li>L* <b>always</b> contains ε; L<sup>+</sup> contains ε only if ε ∈ L.</li>
 <li>{0,11}* = 0s and 1s where the 1s come <b>in pairs</b>: 011, 11110, ε ✔ — 01011, 101 ✘</li>
</ul>
<h3 style="margin-top:8px">Exercise (slide 14) — A = {a,b}, u = aa, v = bab</h3>
<ul>
 <li>uv = <span class="ans">aabab</span> · (uv)² = <span class="ans">aababaabab</span> · u³v = <span class="ans">aaaaaabab</span></li>
 <li>Words of length 2: <span class="ans">{aa, ab, ba, bb}</span></li>
 <li>E1 = {u.v / u,v ∈ A<sup>+</sup>} = <span class="ans">words with |w| ≥ 2</span>; E2 = <span class="ans">A<sup>+</sup></span>; E3 = <span class="ans">A*</span></li>
</ul>
</div>
<div class="card wide">
<h3>2. Operations on languages &amp; RegEx symbols</h3>
<div class="tbl-wrap"><table class="l">
<tr><th>Operation</th><th>Symbol</th><th>Meaning</th><th>Example</th></tr>
<tr><td>Union (alternation)</td><td><code>|</code></td><td>in L or in M (or both)</td><td>L={001,10,111}, M={ε,001} ⇒ L∪M = {ε,001,10,111}</td></tr>
<tr><td>Concatenation</td><td><code>.</code> / juxtaposition</td><td>a word of L followed by a word of M</td><td>L.M = {001,10,111,001001,10001,111001}</td></tr>
<tr><td>Kleene star (closure)</td><td><code>*</code></td><td>0 or more repetitions (ε included)</td><td><code>a*</code> → ε, a, aa, aaa…</td></tr>
<tr><td>Kleene plus (positive closure)</td><td><code>+</code></td><td>1 or more repetitions</td><td><code>b+</code> → b, bb…; <code>\d+</code> → 1, 123…</td></tr>
<tr><td>Optional</td><td><code>?</code></td><td>0 or 1 time</td><td><code>ab?</code> → a, ab</td></tr>
<tr><td>Exact / min count</td><td><code>{n}</code> <code>{n,}</code></td><td>exactly n / at least n times</td><td><code>(a|b|c){3}</code>, <code>[a-z]{2,}</code></td></tr>
<tr><td>Intersection · Difference · Complement</td><td><code>∩</code> · <code>\</code> · <code>¬</code></td><td>common · in first not second · not in L</td><td>{a,b}∩{b} = {b}; {a,b}∖{b} = {a}</td></tr>
<tr><td>Grouping</td><td><code>( )</code></td><td>order of evaluation</td><td><code>(ab)*</code> → ε, ab, abab…</td></tr>
</table></div>
<p style="margin:4px 0"><b>Priority:</b> <span class="k">*</span> (and + ?) &gt; <span class="k">.</span> concatenation &gt; <span class="k">|</span> union. So <code>ab*|c</code> = <code>(a(b*)) | c</code>.</p>
<p style="margin:4px 0"><b>Regular expression (basis):</b> ε and ∅ are RegEx (L(ε)={ε}, L(∅)=∅); every symbol a is a RegEx (L(a)={a}); if E, F are RegEx then E|F, EF, E* and (E) are RegEx. A language is <b>regular</b> ⇔ it is denoted by a RegEx.</p>
</div>
<div class="card">
<h3>3. RegEx notation (slide 33)</h3>
<table>
<tr><th>Token</th><th>Matches</th><th>Set</th></tr>
<tr><td><code>\d</code></td><td>any digit</td><td><code>[0-9]</code></td></tr>
<tr><td><code>\s</code></td><td>whitespace</td><td><code>[ \t\n\r\f]</code></td></tr>
<tr><td><code>\w</code></td><td>letter, digit, _</td><td><code>[A-Za-z0-9_]</code></td></tr>
<tr><td><code>\D \S \W</code></td><td>the inverse</td><td><code>[^0-9]</code> …</td></tr>
<tr><td><code>.</code></td><td>any one character</td><td></td></tr>
<tr><td><code>[A-Z]</code></td><td>one capital letter</td><td></td></tr>
</table>
<p style="margin:4px 0">UNIX example: <code>[A-Z][a-z]*[ ][A-Z][A-Z]</code> = capitalised word + space + 2 capitals (a city and a state: "Paris TX").</p>
<p style="margin:4px 0">Uses: lexical analysers (compilers), search, text recognition, form validation.</p>
</div>
<div class="card">
<h3>4. Classic RegEx patterns over {a,b,c} (Exercise 2)</h3>
<div class="tbl-wrap"><table class="l pat">
<tr><td>All strings</td><td><code>(a|b|c)*</code> = <code>(a*b*c*)*</code></td></tr>
<tr><td>Three-letter strings</td><td><code>(a|b|c){3}</code></td></tr>
<tr><td>Without 'b'</td><td><code>(a|c)*</code></td></tr>
<tr><td>At most one 'a'</td><td><code>(b|c)* | (b|c)*a(b|c)*</code></td></tr>
<tr><td>At least one 'a'</td><td><code>(a|b|c)*a(a|b|c)*</code></td></tr>
<tr><td>Each 'a' followed by 'b'</td><td><code>(b|c|ab)*</code></td></tr>
<tr><td>Even length</td><td><code>((a|b|c)(a|b|c))*</code></td></tr>
<tr><td>Prefix 'ab'</td><td><code>ab(a|b|c)*</code></td></tr>
<tr><td>Suffix 'ab'</td><td><code>(a|b|c)*ab</code></td></tr>
<tr><td>Exactly 3 'a'</td><td><code>(b|c)*a(b|c)*a(b|c)*a(b|c)*</code></td></tr>
<tr><td>At least 3 'a'</td><td><code>(a|b|c)*a(a|b|c)*a(a|b|c)*a(a|b|c)*</code></td></tr>
</table></div>
</div>
<div class="card">
<h3>5. Solved exercises (slides 27–36)</h3>
<p style="margin:2px 0"><b>R = a(a|b)ba = {aaba, abba}</b>, <b>S = (ab)*|(ba)*</b></p>
<ol>
 <li>In R not S: <span class="ans">aaba</span></li>
 <li>In S not R: <span class="ans">ab</span> (or ε, abab)</li>
 <li>In both: <span class="ans">none!</span> R's words (length 4) are aaba, abba; S's words of length 4 are abab, baba ⇒ L(R)∩L(S) = ∅</li>
 <li>In neither: <span class="ans">b</span>, aa, bbb…</li>
</ol>
<p style="margin:4px 0"><b>Give the elements:</b></p>
<ul>
 <li><code>ab*|c</code> = <span class="ans">{c, a, ab, abb, abbb, …}</span></li>
 <li><code>(a+ b)</code> = <span class="ans">{ab, aab, aaab, …}</span> (+ = one or more)</li>
 <li><code>b*ab*ab*</code> = <span class="ans">words of {a,b} with exactly two a</span>: aa, aba, baab…</li>
 <li><code>(a|b*)*(c|d)*</code> = <span class="ans">any word of a,b followed by any word of c,d</span>: ε, ab, ba, cd, abdc…</li>
</ul>
</div>
<div class="card">
<h3>6. True or false? (slide 29)</h3>
<ul>
 <li><code>(a*|b*) = (a|b)*</code> → <span class="ans">False</span>: <i>ab</i> ∈ (a|b)* but not in a*|b*</li>
 <li><code>(a|b)*b = (a|b)*</code> → <span class="ans">False</span>: ε and <i>a</i> are not in (a|b)*b</li>
 <li><code>(a*b)* = (a|b)*b</code> → <span class="ans">False</span>: ε ∈ (a*b)* but ε ∉ (a|b)*b. (True only if we add ε: (a*b)* = ε | (a|b)*b)</li>
</ul>
<p style="margin:4px 0"><b>To prove "False"</b> → give ONE word that is in one side and not the other (counter-example).</p>
<h3 style="margin-top:8px">Exercises 3–5</h3>
<ul>
 <li>L1 = begins with a: <span class="ans"><code>a(a|b)*</code></span> · L2 = even length: <span class="ans"><code>((a|b)(a|b))*</code></span></li>
 <li>3-digit numbers: <code>\d{3}</code> · divisible by 5: <code>[0-9]*(0|5)</code> · start 4 end 7: <code>4[0-9]*7</code> (slide: <code>4.*7</code>)</li>
 <li>Email: <code>[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}</code></li>
</ul>
</div>
</div>

<!-- ================= CHAPTER 2 ================= -->
<h2 id="ch2" class="pb">Chapter 2 — Finite Automata <small>principles · Glushkov · minimisation</small></h2>
<div class="grid">
<div class="card">
<h3>1. Definition</h3>
<p style="margin:2px 0">A <b>finite automaton</b> (finite state machine) reads a string and answers <b>yes</b> if S ∈ L(G), <b>no</b> otherwise.</p>
<p style="margin:4px 0;text-align:center"><span class="m" style="font-size:14px">A = (Q, V<sub>T</sub>, δ, q0, F)</span></p>
<ul>
 <li><b>V<sub>T</sub></b>: finite alphabet · <b>Q</b>: finite set of states</li>
 <li><b>q0</b>: initial state · <b>F</b>: set of final (acceptor) states</li>
 <li><b>δ</b>: transition function <span class="m">δ : Q × V<sub>T</sub> → Q</span></li>
</ul>
<p style="margin:4px 0"><b>Accepted word</b>: w = a1a2…an is accepted if there is a <b>path</b> that starts in the initial state, follows the labels a1, a2, …, an and <b>ends in a final state</b>.</p>
<p style="margin:4px 0">Used in: hardware design, lexical analysis (compilers), text search, robots/planning, program verification, text compression.</p>
</div>
<div class="card">
<h3>2. Example — strings over {0,1} containing "01"</h3>
<p style="margin:2px 0">She reasons with <b>scenarios → one state each</b>:</p>
<ul>
 <li>q0: the first 0 has not appeared yet</li>
 <li>q1: a 0 appeared, waiting for a 1</li>
 <li>q2: "01" was met (final, stays forever)</li>
</ul>
<div class="fig">{{contains01}}</div>
</div>
<div class="card">
<h3>3. Example — even number of 0 AND of 1</h3>
<p style="margin:2px 0"><span class="m">M = ({q0,q1,q2,q3}, {0,1}, δ, q0, {q0})</span></p>
<div>
<table style="float:left;margin-right:10px">
<tr><th>δ</th><th>0</th><th>1</th></tr>
<tr><td class="s">→*q0</td><td>q3</td><td>q1</td></tr>
<tr><td class="s">q1</td><td>q2</td><td>q0</td></tr>
<tr><td class="s">q2</td><td>q1</td><td>q3</td></tr>
<tr><td class="s">q3</td><td>q0</td><td>q2</td></tr>
</table>
<div class="fig">{{even01}}</div>
</div><div style="clear:both"></div>
<p class="cap">q0 = (even 0, even 1) · q1 = (even 0, odd 1) · q2 = (odd, odd) · q3 = (odd 0, even 1)</p>
</div>
<div class="card">
<h3>4. Reading a diagram (slide 49) &amp; table (slide 47)</h3>
<div class="fig">{{ex49}}</div>
<p class="cap">Σ={a,b}, Q={1,2,3,4}, F={4}. Language = <b>(a|b)b</b> = {ab, bb}. State 3 is a <b>trap</b>: once there, never accepted.</p>
<p style="margin:4px 0">L = a(ab)*b, Q={q0,q1,q2}, V<sub>T</sub>={a,b,ab}: δ(q0,a)=q1, δ(q1,b)=q2, δ(q1,ab)=q1</p>
<div class="fig">{{aabb_star}}</div>
</div>
</div>

<h2 id="glushkov">Glushkov construction <small>RegEx → automaton</small></h2>
<div class="grid">
<div class="card">
<h3>Method — 3 steps</h3>
<ol>
 <li><b>Number</b> every symbol of the RegEx from 1 (each symbol appears once) → RE2.<br><span class="m">a*b(a|c)*b → a1* b2 (a3|c4)* b5</span><br>States: q0 = 0, Q = {0,1,…,n} (n = number of letters).</li>
 <li><b>Build A'</b>:
  <ol type="a">
   <li><b>Start letters</b> (can begin a word) → arcs <span class="m">0 → i</span> labelled a<sub>i</sub></li>
   <li><b>End letters</b> (can finish a word) → F = their numbers. <b>If ε ∈ L(RE) add 0 to F!</b></li>
   <li><b>Factors of length 2</b> a<sub>i</sub>a<sub>j</sub> (a<sub>j</sub> can come right after a<sub>i</sub>) → arc <span class="m">i → j</span> labelled a<sub>j</sub></li>
  </ol></li>
 <li><b>Erase the indices</b> (a3 → a) and draw the automaton A.</li>
</ol>
<p style="margin:4px 0"><b>Rule:</b> an arc always goes INTO the state of the letter it reads: reading a<sub>j</sub> ⇒ go to state j.</p>
</div>
<div class="card">
<h3>Example 1 — a*b(a|c)*b &nbsp;→&nbsp; a1* b2 (a3|c4)* b5</h3>
<ul>
 <li>Start letters = {a1, b2} · End letters = {b5} ⇒ F = {5}</li>
 <li>Factors: a1a1 a1b2 b2a3 b2c4 b2b5 a3a3 a3c4 c4a3 c4c4 a3b5 c4b5</li>
</ul>
<table>
<tr><th></th><th>successors</th></tr>
<tr><td class="s">ɸ</td><td>a1, b2</td></tr>
<tr><td class="s">a1</td><td>a1, b2</td></tr>
<tr><td class="s">b2</td><td>a3, c4, b5</td></tr>
<tr><td class="s">a3</td><td>a3, c4, b5</td></tr>
<tr><td class="s">c4</td><td>a3, c4, b5</td></tr>
<tr><td class="s" style="outline:2px solid var(--ink)">b5</td><td>ɸ</td></tr>
</table>
<div class="fig">{{gl1}}</div>
</div>
<div class="card">
<h3>Example — b(ab)* | (ba)*b &nbsp;→&nbsp; b1(a2b3)* | (b4a5)*b6</h3>
<div class="two">
<table>
<tr><th></th><th>successors</th></tr>
<tr><td class="s">ɸ</td><td>b1, b4, b6</td></tr>
<tr><td class="s" style="outline:2px solid var(--ink)">b1</td><td>a2</td></tr>
<tr><td class="s">a2</td><td>b3</td></tr>
<tr><td class="s" style="outline:2px solid var(--ink)">b3</td><td>a2</td></tr>
<tr><td class="s">b4</td><td>a5</td></tr>
<tr><td class="s">a5</td><td>b4, b6</td></tr>
<tr><td class="s" style="outline:2px solid var(--ink)">b6</td><td>ɸ</td></tr>
</table>
<div style="font-size:12.5px">Boxed = end letters ⇒ <b>F = {1, 3, 6}</b>.<br>b1 is an end letter because (a2b3)* can be empty.<br><br>⚠ From 0, reading <b>b</b> goes to 1, 4 <i>and</i> 6 ⇒ Glushkov usually gives an <b>NFA</b> → determinise it (Ch3).</div>
</div>
<div class="fig">{{gl2}}</div>
</div>
<div class="card">
<h3>Example 2 (slide 57, left blank) — (c+|a) b (ac)* b — solved</h3>
<p style="margin:2px 0"><span class="m">(c1+ | a2) b3 (a4 c5)* b6</span> &nbsp; (c+ = c c*, so c1 can follow c1)</p>
<div class="two">
<table>
<tr><th></th><th>successors</th></tr>
<tr><td class="s">ɸ</td><td>c1, a2</td></tr>
<tr><td class="s">c1</td><td>c1, b3</td></tr>
<tr><td class="s">a2</td><td>b3</td></tr>
<tr><td class="s">b3</td><td>a4, b6</td></tr>
<tr><td class="s">a4</td><td>c5</td></tr>
<tr><td class="s">c5</td><td>a4, b6</td></tr>
<tr><td class="s" style="outline:2px solid var(--ink)">b6</td><td>ɸ</td></tr>
</table>
<div style="font-size:12.5px">q0 = 0, Q = {0,…,6}, <b>F = {6}</b> (ε ∉ L).<br><br>Rows <b>b3</b> and <b>c5</b> have the same successors and both are non-final ⇒ states 3 and 5 can be <b>merged</b> (minimisation).</div>
</div>
<div class="fig">{{gl3}}</div>
<p class="cap">After minimisation (3 ≡ 5):</p>
<div class="fig">{{gl3min}}</div>
</div>
</div>

<h2 id="min" class="pb">Minimisation of automata <small>same language, fewest states</small></h2>
<div class="grid">
<div class="card">
<h3>Method</h3>
<p style="margin:2px 0">Why: less memory/computation, easier to read; used in compilers, pattern matching, model checking.</p>
<ol>
 <li><b>Remove unreachable states</b> (mark everything reachable from the start; delete the rest).</li>
 <li><b>Step0</b>: split into 2 groups → <b>(final states) (non-final states)</b>.</li>
 <li>For every state of a group, look <b>which group</b> each letter sends it to. States of a group that go to <b>different groups</b> are <b>distinguishable</b> → split the group.</li>
 <li>Repeat (Step1, Step2, …) until nothing splits any more.</li>
 <li>Each final group = <b>one state</b> ("fusion"). Initial = group containing the old initial; final = groups of old finals.</li>
</ol>
<p style="margin:4px 0"><b>Two states are distinguishable</b> if one word leads one of them to a final state and the other to a non-final one.</p>
</div>
<div class="card">
<h3>Example (slide 60) — F = {6, 7, 8}</h3>
<div class="two">
<table>
<tr><th></th><th>a</th><th>b</th></tr>
<tr><td class="s">→1</td><td>1</td><td>5</td></tr>
<tr><td class="s">2</td><td>2</td><td>5</td></tr>
<tr><td class="s">3</td><td>4</td><td>6</td></tr>
<tr><td class="s">4</td><td>3</td><td>8</td></tr>
<tr><td class="s">5</td><td>2</td><td>4</td></tr>
<tr><td class="s">*6</td><td>3</td><td>7</td></tr>
<tr><td class="s">*7</td><td>8</td><td>7</td></tr>
<tr><td class="s">*8</td><td>7</td><td>7</td></tr>
</table>
<div class="steps">Step0 : (6,7,8) (1,2,3,4,5)
Step1 : (6) (7,8) (1,2,3,4,5)
Step2 : (6) (7,8) (3) (4) (1,2,5)
Step3 : (6) (7,8) (3) (4) (1,2) (5)
→ stable ⇒ 6 states</div>
</div>
<ul style="font-size:12.5px">
 <li>Step1: 6 –a→ 3 (non-final) but 7,8 –a→ final ⇒ 6 alone.</li>
 <li>Step2: 3 –b→ 6 ∈ (6), 4 –b→ 8 ∈ (7,8), 1,2,5 stay inside ⇒ 3 and 4 alone.</li>
 <li>Step3: 5 –b→ 4 (now alone) but 1,2 –b→ 5 ⇒ 5 alone. 1 and 2 behave the same ⇒ merge.</li>
</ul>
<div class="fig">{{min1}}</div>
</div>
<div class="card wide">
<h3>Class exercise (board photo, slide 61) — minimise (a | ba | bba)* (b | bb | ε)</h3>
<div class="two">
<div>
<p style="margin:2px 0"><b>① Number:</b> <span class="m">(a1 | b2a3 | b4b5a6)* (b7 | b8b9 | ε10)</span></p>
<p style="margin:2px 0"><b>② Successors table</b> (as on the board):</p>
<table class="l">
<tr><td class="s">ɸ</td><td>a1 b2 b4 b7 b8 ε10</td></tr>
<tr><td class="s">a1</td><td>a1 b2 b4 b7 b8 ε10</td></tr>
<tr><td class="s">b2</td><td>a3</td></tr>
<tr><td class="s">a3</td><td>a1 b2 b4 b7 b8 ε10</td></tr>
<tr><td class="s">b4</td><td>b5</td></tr>
<tr><td class="s">b5</td><td>a6</td></tr>
<tr><td class="s">a6</td><td>a1 b2 b4 b7 b8 ε10</td></tr>
<tr><td class="s" style="outline:2px solid var(--ink)">b7</td><td>ɸ</td></tr>
<tr><td class="s">b8</td><td>b9</td></tr>
<tr><td class="s" style="outline:2px solid var(--ink)">b9</td><td>ɸ</td></tr>
<tr><td class="s" style="outline:2px solid var(--ink)">ε10</td><td>ɸ</td></tr>
</table>
<p style="margin:2px 0">Final letters ⇒ <b>F = {7, 9, 10}</b></p>
</div>
<div>
<p style="margin:2px 0"><b>③ Transition table</b> — boxed rows are identical:</p>
<table>
<tr><th></th><th>a</th><th>b</th><th>ε</th></tr>
<tr class="box"><td class="s">→0</td><td>1</td><td>2,4,7,8</td><td>10</td></tr>
<tr class="box"><td class="s">1</td><td>1</td><td>2,4,7,8</td><td>10</td></tr>
<tr><td class="s">2</td><td>3</td><td>-</td><td>-</td></tr>
<tr class="box"><td class="s">3</td><td>1</td><td>2,4,7,8</td><td>10</td></tr>
<tr><td class="s">4</td><td>-</td><td>5</td><td>-</td></tr>
<tr><td class="s">5</td><td>6</td><td>-</td><td>-</td></tr>
<tr class="box"><td class="s">6</td><td>1</td><td>2,4,7,8</td><td>10</td></tr>
<tr><td class="s">*7</td><td>-</td><td>-</td><td>-</td></tr>
<tr><td class="s">8</td><td>-</td><td>9</td><td>-</td></tr>
<tr><td class="s">*9</td><td>-</td><td>-</td><td>-</td></tr>
<tr><td class="s">*10</td><td>-</td><td>-</td><td>-</td></tr>
</table>
<p style="margin:2px 0"><b>④ Steps (her writing):</b></p>
<div class="steps">1) {7,9,10} {0,1,2,3,4,5,6,8}
2) {7,9,10} {8} {2,4,5} {0} {1} {3} {6}
3) {7,9,10} {8} {2} {4} {5} {0} {1} {3} {6}
4) {7,9,10} {0,1,3,6} {8} {2} {4} {5}  ← fusion (same behaviour)</div>
</div>
</div>
<div class="two">
<div class="fig">{{minclass}}</div>
<div style="font-size:12.5px">
<p style="margin:2px 0"><b>Why the fusions?</b> 7, 9, 10 have no exit at all ⇒ same behaviour. 0, 1, 3, 6 have the <b>same row</b> (a→1, b→2,4,7,8, ε→10) ⇒ one state "0,1,3,6".</p>
<p style="margin:6px 0" class="trap" ><b>Note:</b> with strict step-by-step refinement 0,1,3,6 are never separated, and <b>2 and 5</b> also behave the same (each only reads <i>a</i> and goes back into {0,1,3,6}) — so they could be merged into "2,5" too. Write her version, and mention this if you have time.</p>
<p style="margin:6px 0">Language check: "0,1,3,6" reads <i>a</i>, <i>ba</i> (via 2) or <i>bba</i> (via 4,5) and comes back; the end reads b, bb (via 8) or nothing (ε).</p>
</div>
</div>
</div>
</div>

<!-- ================= CHAPTER 3 ================= -->
<h2 id="ch3" class="pb">Chapter 3 — Deterministic &amp; non-deterministic automata</h2>
<div class="grid">
<div class="card">
<h3>1. Definitions</h3>
<ul>
 <li><b>Completely defined</b>: for each state q and each symbol s ∈ Σ there is <b>at least one</b> transition labelled s leaving q.</li>
 <li><b>Unambiguous</b>: for each state q and symbol s there is <b>at most one</b> transition labelled s leaving q.</li>
 <li><b>DFA</b> (deterministic) = completely defined <b>AND</b> unambiguous ⇒ <b>exactly one</b> arrow per (state, symbol). <b>No ε-arrows.</b></li>
 <li><b>NFA</b> (non-deterministic) = presents <b>ambiguity</b>: several arrows with the same symbol from one state, or ε-arrows. "We cannot deduce the next state."</li>
</ul>
<p style="margin:4px 0"><b>How to complete a DFA:</b> add a <b>dead state</b> (trap) that receives every missing transition and loops on all symbols.</p>
<p style="margin:4px 0"><b>Every NFA has an equivalent DFA</b> (same language) → subset construction below.</p>
</div>
<div class="card">
<h3>2. Activity (slide 66) — solved</h3>
<div class="fig">{{activity}}</div>
<table>
<tr><th>δ</th><th>0</th><th>1</th></tr>
<tr><td class="s">→q0</td><td>-</td><td>q1</td></tr>
<tr><td class="s">q1</td><td>-</td><td>{q0, q2}</td></tr>
<tr><td class="s">*q2</td><td>q1</td><td>q2</td></tr>
</table>
<ul style="font-size:12.5px">
 <li>q1 –1→ q0 <b>or</b> q2 ⇒ ambiguity ⇒ <b>NFA</b>; q0 and q1 have no 0-arrow ⇒ not completely defined.</li>
 <li><b>101</b>: q0 –1→ q1 –0→ ? no transition ⇒ <span class="ans">rejected (not modeled)</span></li>
 <li><b>1111</b>: q0→q1→q2→q2→q2 ⇒ <span class="ans">accepted</span></li>
 <li><b>1101</b>: q0→q1→q2 –0→ q1 –1→ q2 ⇒ <span class="ans">accepted</span></li>
</ul>
</div>
<div class="card">
<h3>3. Build a DFA from a sentence — her recipe</h3>
<ol>
 <li>List the strings of L: L = {0, 00, 01, 000, …}</li>
 <li>Draw the <b>shortest accepted word</b> as a path.</li>
 <li>Add the other arrows so that <b>every state has one arrow per symbol</b>.</li>
 <li>Words that can never be accepted → <b>dead state</b>.</li>
</ol>
<p style="margin:4px 0"><b>Starts with 0</b> over {0,1}:</p>
<div class="fig">{{starts0}}</div>
<p style="margin:4px 0"><b>Length exactly 2</b>: L = {00, 01, 10, 11}</p>
<div class="fig">{{len2}}</div>
</div>
<div class="card wide">
<h3>4. Contains "aabb" — and the complement trick</h3>
<div class="fig">{{aabb}}</div>
<p class="cap">State = how much of "aabb" is matched (A: nothing, B: a, C: aa, D: aab, E: found). D –a→ B because "aaba" ends with "a".</p>
<p style="margin:4px 0"><b>Does NOT contain aabb</b> → <b>flip the states</b>: 1. final → non-final, 2. non-final → final.</p>
<div class="fig">{{noaabb}}</div>
<p class="trap" style="padding:4px 8px;margin:4px 0">⚠ Flipping only works on a <b>complete DFA</b> (add the dead state first, never on an NFA).</p>
</div>
</div>

<h2 id="subset">NFA → DFA <small>subset construction</small></h2>
<div class="grid">
<div class="card">
<h3>Method (M = (Q,Σ,δ,q0,F) → M' with L(M) = L(M'))</h3>
<ol>
 <li>Q' = ϕ.</li>
 <li>Add <b>[q0]</b> to Q' and compute its transitions.</li>
 <li>For every state of Q' and every symbol, compute the <b>set</b> of reachable states: <span class="m">δ'([q1,q2], 0) = δ(q1,0) ∪ δ(q2,0)</span>. If the set is <b>new</b> → add it to Q' ("new state").</li>
 <li>Stop when no new state appears.</li>
 <li><b>Final states</b> of the DFA = every set that <b>contains</b> a final state of the NFA.</li>
</ol>
<p style="margin:4px 0">States never reached from [q0] (e.g. [q2] below) are <b>unreachable</b> → drop them. ϕ = dead state.</p>
<p style="margin:4px 0"><b>With ε-arrows</b>: start from ε-closure(q0) (q0 + everything reachable by ε only), and after each move take the ε-closure again.</p>
</div>
<div class="card">
<h3>Example 1 (class photo, slides 75–77) — F = {q2}</h3>
<div class="fig">{{nfa1}}</div>
<div class="two">
<table>
<tr><th>NFA</th><th>0</th><th>1</th></tr>
<tr><td class="s">→q0</td><td>q0</td><td>q1</td></tr>
<tr><td class="s">q1</td><td>{q1,q2}</td><td>q1</td></tr>
<tr><td class="s">*q2</td><td>q2</td><td>{q1,q2}</td></tr>
</table>
<div class="steps" style="font-size:11.5px">δ'([q0],0) = [q0]
δ'([q0],1) = [q1]
δ'([q1],0) = [q1,q2] ← new
δ'([q1],1) = [q1]
δ'([q1,q2],0) = {q1,q2}∪{q2}
            = [q1,q2]
δ'([q1,q2],1) = {q1}∪{q1,q2}
            = [q1,q2]</div>
</div>
<table>
<tr><th>DFA</th><th>0</th><th>1</th></tr>
<tr><td class="s">→q0</td><td>q0</td><td>q1</td></tr>
<tr><td class="s">q1</td><td>{q1,q2} = q3</td><td>q1</td></tr>
<tr><td class="s">*q3 = {q1,q2}</td><td>q3</td><td>q3</td></tr>
</table>
<div class="fig">{{dfa1}}</div>
</div>
<div class="card">
<h3>Example 2 (slide 78) — F = {q1}</h3>
<div class="two">
<table>
<tr><th></th><th>0</th><th>1</th></tr>
<tr><td class="s">→q0</td><td>{q0,q1}</td><td>{q1}</td></tr>
<tr><td class="s">*q1</td><td>ϕ</td><td>{q0,q1}</td></tr>
</table>
<div class="steps" style="font-size:11.5px">δ'([q0],0) = [q0,q1] ← new
δ'([q0],1) = [q1]
δ'([q1],0) = ϕ
δ'([q1],1) = [q0,q1]
δ'([q0,q1],0) = [q0,q1]
δ'([q0,q1],1) = [q0,q1]</div>
</div>
<div class="fig">{{dfa2}}</div>
<p class="cap">[q1] and [q0,q1] are final (they contain q1). ϕ is the dead state (often not drawn).</p>
</div>
<div class="card wide">
<h3>Application (slide 79) — ε-NFA → DFA — solved</h3>
<div class="two">
<div>
<div class="fig">{{enfa}}</div>
<p class="cap">Language = words over {a,b} that contain <b>aa</b> or <b>bb</b>.</p>
<p style="margin:2px 0">ε-closure(0) = {0,1,4} = <b>A</b> (start)</p>
</div>
<div class="tbl-wrap">
<table>
<tr><th>DFA state</th><th>a</th><th>b</th></tr>
<tr><td class="s">→A = {0,1,4}</td><td>{1,2,4} = B</td><td>{1,4,5} = C</td></tr>
<tr><td class="s">B = {1,2,4}</td><td>{1,2,3,4} = D</td><td>C</td></tr>
<tr><td class="s">C = {1,4,5}</td><td>B</td><td>{1,4,5,6} = E</td></tr>
<tr><td class="s">*D = {1,2,3,4}</td><td>D</td><td>{1,3,4,5} = F</td></tr>
<tr><td class="s">*E = {1,4,5,6}</td><td>{1,2,4,6} = G</td><td>E</td></tr>
<tr><td class="s">*F = {1,3,4,5}</td><td>D</td><td>{1,3,4,5,6} = H</td></tr>
<tr><td class="s">*G = {1,2,4,6}</td><td>{1,2,3,4,6} = I</td><td>E</td></tr>
<tr><td class="s">*H = {1,3,4,5,6}</td><td>I</td><td>H</td></tr>
<tr><td class="s">*I = {1,2,3,4,6}</td><td>I</td><td>H</td></tr>
</table>
</div>
</div>
<div class="two">
<div class="steps">Minimise:
Step0: (D,E,F,G,H,I) (A,B,C)
Step1: (D,…,I) (A) (B) (C)
  B –a→ final, C –b→ final, A never
  ⇒ A, B, C all different
  D…I only go to D…I ⇒ fusion
  ⇒ one accepting state "F"</div>
<div class="fig">{{edfa}}</div>
</div>
</div>
<div class="card wide">
<h3>Example — moves on a 3×3 chessboard (slides 80–86)</h3>
<div class="two">
<div>
<p style="margin:2px 0">States = squares 1…9; inputs <b>w</b> = move to an adjacent white square, <b>b</b> = adjacent black square. Start 1, final = opposite corner 9.</p>
<table>
<tr><th>NFA</th><th>w</th><th>b</th><th></th><th>w</th><th>b</th></tr>
<tr><td class="s">→1</td><td>2,4</td><td>5</td><td class="s">6</td><td>2,8</td><td>3,5,9</td></tr>
<tr><td class="s">2</td><td>4,6</td><td>1,3,5</td><td class="s">7</td><td>4,8</td><td>5</td></tr>
<tr><td class="s">3</td><td>2,6</td><td>5</td><td class="s">8</td><td>4,6</td><td>5,7,9</td></tr>
<tr><td class="s">4</td><td>2,8</td><td>1,5,7</td><td class="s">*9</td><td>6,8</td><td>5</td></tr>
<tr><td class="s">5</td><td>2,4,6,8</td><td>1,3,7,9</td><td></td><td></td><td></td></tr>
</table>
</div>
<div>
<table>
<tr><th>DFA</th><th>w</th><th>b</th></tr>
<tr><td class="s">→q0 = {1}</td><td>q1</td><td>q2</td></tr>
<tr><td class="s">q1 = {2,4}</td><td>q3</td><td>q4</td></tr>
<tr><td class="s">q2 = {5}</td><td>q3</td><td>q5</td></tr>
<tr><td class="s">q3 = {2,4,6,8}</td><td>q3</td><td>q6</td></tr>
<tr><td class="s">q4 = {1,3,5,7}</td><td>q3</td><td>q6</td></tr>
<tr><td class="s">*q5 = {1,3,7,9}</td><td>q3</td><td>q2</td></tr>
<tr><td class="s">*q6 = {1,3,5,7,9}</td><td>q3</td><td>q6</td></tr>
</table>
<p class="cap">7 states q0…q6 like on her slide; finals = the sets containing 9.</p>
</div>
</div>
</div>
</div>

<h2 id="exam">Exam-day checklist</h2>
<div class="grid">
<div class="card">
<h3>Which method for which question?</h3>
<table class="l">
<tr><th>Question says…</th><th>Do…</th></tr>
<tr><td>"Give the RegEx of…"</td><td>Pattern table (Ch1 §4)</td></tr>
<tr><td>"Give the elements / words of…"</td><td>List the 4–5 shortest words + "…"</td></tr>
<tr><td>"Is this equality true?"</td><td>Counter-example word</td></tr>
<tr><td>"Build the automaton of this RegEx"</td><td>Glushkov (number → successors → draw)</td></tr>
<tr><td>"Minimise"</td><td>Remove unreachable → Step0 (F)(non-F) → split → fusion</td></tr>
<tr><td>"Is it deterministic?"</td><td>Check complete + unambiguous (+ no ε)</td></tr>
<tr><td>"Convert NFA to DFA"</td><td>Subset construction, final = contains NFA final</td></tr>
<tr><td>"Doesn't contain / complement"</td><td>Complete DFA + flip states</td></tr>
<tr><td>"Is word w accepted?"</td><td>Follow the path; must END in a final state</td></tr>
</table>
</div>
<div class="card trap">
<h3>⚠ Mistakes that cost points</h3>
<ul>
 <li>Forgetting to mark the <b>initial arrow</b> and the <b>double circles</b>.</li>
 <li>Glushkov: forgetting to add <b>0 to F when ε ∈ L</b>; forgetting that x* makes the next letter a possible start/end letter.</li>
 <li>Minimisation: starting with anything else than <b>(finals)(non-finals)</b>; not deleting unreachable states first.</li>
 <li>NFA→DFA: forgetting a "new state" in the list, or forgetting that a set is final if it contains <b>at least one</b> NFA final state.</li>
 <li>A DFA must have <b>exactly one</b> arrow per symbol in every state → add the dead state.</li>
 <li>Complementing an NFA by flipping states — <b>wrong</b>, determinise first.</li>
</ul>
<p style="margin:6px 0">Tools to check yourself: <b>regexper.com</b> (RegEx → diagram) · <b>automatonsimulator.com</b></p>
</div>
<div class="card">
<h3>Still to come (course outline)</h3>
<p style="margin:2px 0">The outline announces 6 chapters; the slides in this folder cover the first part. Still coming: <b>Turing machine</b> (application of automata) and <b>applications of automata in AI</b>. Add their slides to <code>automata/</code> and this sheet can be extended.</p>
</div>
</div>
<footer>Made from the course slides (chapter1_regEx, chapter2_automata, chapter3_DFA) and the board photos of 04/11. Print: Ctrl+P → A4.</footer>
"""

html = BODY
for k, v in D.items():
    html = html.replace("{{" + k + "}}", v)
missing = re.findall(r"\{\{(\w+)\}\}", html)
assert not missing, missing

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Automata Cheat Sheet</title><style>{CSS}</style></head>
<body><div class="wrap">{html}</div></body></html>"""
import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write(page)
print("wrote", OUT, len(page))
