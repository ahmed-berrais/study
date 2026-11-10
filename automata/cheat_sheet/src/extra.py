"""Extra sections added so the sheet is self-sufficient."""

CSS = r"""
details{background:#f3fbf6;border:1px solid #bfe3cc;border-radius:8px;padding:4px 10px;margin:6px 0}
summary{cursor:pointer;color:#0b7a3e;font-weight:600}
details[open] summary{margin-bottom:4px}
.ex{margin:8px 0 2px;font-weight:600;color:var(--ink)}
.tag{display:inline-block;font-size:11px;font-weight:700;color:#fff;background:var(--teal);border-radius:99px;padding:0 8px;margin-left:6px;vertical-align:middle}
.tag.warn{background:#e0a100}
"""

# ---------- Chapter 1: RegEx simplification ----------
REGEX_SIMPL = r"""
<div class="card wide">
<h3>7. Simplifying a RegEx — the rules (identities) <span class="tag warn">not on her slides, but needed for "simplify" / "true or false"</span></h3>
<div class="two">
<div class="tbl-wrap"><table class="l">
<tr><th>Family</th><th>Rule</th></tr>
<tr><td class="s">Union |</td><td><code>r|s = s|r</code> · <code>r|r = r</code> · <code>r|∅ = r</code> · <code>(r|s)|t = r|(s|t)</code></td></tr>
<tr><td class="s">Concatenation</td><td><code>εr = rε = r</code> · <code>∅r = r∅ = ∅</code> · <code>r(s|t) = rs|rt</code> · <code>(s|t)r = sr|tr</code> · <b>rs ≠ sr</b></td></tr>
<tr><td class="s">Star basics</td><td><code>∅* = ε</code> · <code>ε* = ε</code> · <code>(r*)* = r*</code> · <code>r*r* = r*</code></td></tr>
<tr><td class="s">Star + ε</td><td><code>ε|rr* = r*</code> · <code>(ε|r)* = r*</code> · <code>(ε|r)r* = r*</code> · <code>ε|r* = r*</code></td></tr>
<tr><td class="s">Plus</td><td><code>rr* = r*r = r+</code> · <code>r* = ε|r+</code> · <code>r+|ε = r*</code></td></tr>
<tr><td class="s">Sliding</td><td><code>(rs)*r = r(sr)*</code> &nbsp; e.g. <code>(ab)*a = a(ba)*</code></td></tr>
<tr><td class="s">Big one</td><td><code>(r|s)* = (r*s*)* = (r*|s*)* = (r*s)*r* = r*(sr*)*</code></td></tr>
<tr><td class="s">Absorption</td><td>if L(r) ⊆ L(s): <code>r|s = s</code>. e.g. <code>a | a* = a*</code>, <code>ab | (a|b)* = (a|b)*</code></td></tr>
<tr><td class="s">Star absorption</td><td><code>r*(r|s)* = (r|s)*</code> · <code>(r|s)*r* = (r|s)*</code></td></tr>
</table></div>
<div>
<p style="margin:2px 0"><b>❌ FALSE equalities (classic traps)</b></p>
<ul>
 <li><code>(r|s)* ≠ r*|s*</code> &nbsp; (ab is a counter-example)</li>
 <li><code>(r|s)* ≠ r*s*</code> &nbsp; (ba)</li>
 <li><code>(rs)* ≠ r*s*</code> &nbsp; (aab is in a*b*, not in (ab)*)</li>
 <li><code>r+ ≠ r*</code> &nbsp; (ε)</li>
</ul>
<p style="margin:6px 0 2px"><b>Worked simplifications</b></p>
<div class="steps">(a|ε)a*          = a*            (ε|r)r* = r*
ε | aa* | a       = a* | a = a*   absorption
a*(a|b)*          = (a|b)*        star absorption
(a|b)*(a|b)*      = (a|b)*        r*r* = r*
(a*b*)*a(a|b)*    = (a|b)*a(a|b)*
b*(ab*)*          = (a|b)*        r*(sr*)* = (r|s)*
(ab)*a | a(ba)*   = a(ba)*        sliding, then r|r = r
∅a | b            = b             ∅r = ∅, r|∅ = r</div>
<p style="margin:6px 0 2px"><b>How to check an equality fast:</b> list all words of length 0, 1, 2 (and 3) on both sides. One word in one side only ⇒ <b>False</b>. If you want to say <b>True</b>, justify with the rules above.</p>
</div>
</div>
</div>
"""

# ---------- Chapter 2: extended transition / trace ----------
TRACE = r"""
<div class="card">
<h3>5. Is a word accepted? — how to write the trace</h3>
<p style="margin:2px 0"><b>Extended function δ*</b> (reads a whole word):</p>
<ul>
 <li><code>δ*(q, ε) = q</code> · <code>δ*(q, wa) = δ(δ*(q, w), a)</code></li>
 <li><b>L(A) = { w ∈ Σ* | δ*(q0, w) ∈ F }</b></li>
</ul>
<p style="margin:4px 0">Trace of <b>1101</b> on the "contains 01" automaton:</p>
<div class="steps">(q0, 1101) ⊢ (q0, 101) ⊢ (q0, 01)
⊢ (q1, 1) ⊢ (q2, ε)   q2 ∈ F ⇒ accepted ✔</div>
<p style="margin:4px 0">Short form also OK: <span class="m">q0 –1→ q0 –1→ q0 –0→ q1 –1→ q2 ✔</span></p>
<ul style="font-size:12.5px">
 <li><b>Rejected</b> if: the path ends in a non-final state, OR a transition is missing ("blocked").</li>
 <li><b>NFA</b>: accepted if <b>at least one</b> path ends in a final state — try all choices.</li>
</ul>
</div>
"""

# ---------- Glushkov rules for any expression ----------
GLUSHKOV_RULES = r"""
<div class="card">
<h3>Glushkov for ANY expression — First / Last / Follow rules</h3>
<p style="margin:2px 0">For hard expressions, compute bottom-up: <b>N</b> = nullable (can give ε?), <b>First</b> = start letters, <b>Last</b> = end letters, <b>Follow</b> = factors of length 2.</p>
<div class="tbl-wrap"><table class="l" style="font-size:12px">
<tr><th>E</th><th>N(E)</th><th>First(E)</th><th>Last(E)</th><th>new Follow</th></tr>
<tr><td>a<sub>i</sub></td><td>no</td><td>{a<sub>i</sub>}</td><td>{a<sub>i</sub>}</td><td>–</td></tr>
<tr><td>ε</td><td>yes</td><td>∅</td><td>∅</td><td>–</td></tr>
<tr><td>F | G</td><td>N(F) or N(G)</td><td>First(F) ∪ First(G)</td><td>Last(F) ∪ Last(G)</td><td>–</td></tr>
<tr><td>F G</td><td>N(F) and N(G)</td><td>First(F) ∪ First(G) <i>if N(F)</i></td><td>Last(G) ∪ Last(F) <i>if N(G)</i></td><td>Last(F) → First(G)</td></tr>
<tr><td>F*</td><td>yes</td><td>First(F)</td><td>Last(F)</td><td>Last(F) → First(F)</td></tr>
<tr><td>F+</td><td>N(F)</td><td>First(F)</td><td>Last(F)</td><td>Last(F) → First(F)</td></tr>
<tr><td>F?</td><td>yes</td><td>First(F)</td><td>Last(F)</td><td>–</td></tr>
</table></div>
<p style="margin:4px 0">Then: arcs <b>0 → First</b>, arcs <b>i → j</b> for each Follow pair, <b>F = Last</b> (+ <b>0</b> if N(E) = yes).</p>
<p style="margin:4px 0"><b>Check:</b> number of states = number of letters + 1.</p>
</div>
"""

THOMPSON = r"""
<div class="card">
<h3>Other method: Thompson (RegEx → ε-NFA) <span class="tag">if asked</span></h3>
<p style="margin:2px 0">Build small blocks and glue them with ε-arrows (one start, one final per block):</p>
<ul>
 <li><b>a</b>: i –a→ f</li>
 <li><b>F|G</b>: new i –ε→ start(F) and start(G); final(F), final(G) –ε→ new f</li>
 <li><b>FG</b>: final(F) –ε→ start(G)</li>
 <li><b>F*</b>: new i –ε→ start(F) and –ε→ new f; final(F) –ε→ start(F) and –ε→ f</li>
</ul>
<p style="margin:4px 0">Gives many ε-arrows → remove them with ε-closure (Ch3). Her course uses <b>Glushkov</b> (no ε, fewer states): use Glushkov unless the question says Thompson.</p>
</div>
"""

# ---------- Ch3: NFA formal definition ----------
NFA_DEF = r"""<p style="margin:4px 0"><b>Formal NFA</b>: <span class="m">N = (Q, Σ, δ, q0, F)</span> with <span class="m">δ : Q × (Σ ∪ {ε}) → P(Q)</span> (a <b>set</b> of states, possibly ∅). For a DFA: <span class="m">δ : Q × Σ → Q</span> (exactly one state).</p>
"""

# ---------- Ch3: epsilon removal ----------
EPSILON = r"""
<div class="card wide">
<h3>ε-transitions: ε-closure and how to remove them <span class="tag warn">her slides use ε (slides 73, 79) — full method here</span></h3>
<div class="two">
<div>
<ul>
 <li><b>ε-arrow</b> = change state <b>without reading</b> any letter.</li>
 <li><b>ε-closure(q)</b> = q itself + every state reachable from q using <b>only ε-arrows</b> (follow chains: q –ε→ p –ε→ r ⇒ r too).</li>
 <li>ε-closure of a set = union of the closures.</li>
</ul>
<p style="margin:4px 0"><b>Subset construction with ε</b> (= NFA→DFA + closures):</p>
<ol>
 <li>Start state of the DFA = <b>ε-closure(q0)</b>.</li>
 <li>For a DFA state S and a letter x: <b>move</b> = all states reachable from S by one x-arrow, then take the <b>ε-closure</b> of that.<br><span class="m">δ'(S, x) = ε-closure( ∪<sub>q∈S</sub> δ(q, x) )</span></li>
 <li>Repeat for every new set. Final = sets containing an NFA final state.</li>
</ol>
<p style="margin:4px 0"><b>Example (slide 73, first NFA)</b> — F = {q2}</p>
<div class="fig">{{eps73}}</div>
<p class="cap">ε-closure(q1) = {q1, q2} · ε-closure(q2) = {q2} · ε-closure(q3) = {q3}</p>
</div>
<div>
<table>
<tr><th>DFA state</th><th>0</th><th>1</th></tr>
<tr><td class="s">→*A = {q1,q2}</td><td>{q1,q3}→cl = {q1,q2,q3} = B</td><td>{q2,q3} = C</td></tr>
<tr><td class="s">*B = {q1,q2,q3}</td><td>B</td><td>C</td></tr>
<tr><td class="s">*C = {q2,q3}</td><td>{q3} = D</td><td>C</td></tr>
<tr><td class="s">D = {q3}</td><td>ϕ</td><td>ϕ</td></tr>
<tr><td class="s">ϕ (dead)</td><td>ϕ</td><td>ϕ</td></tr>
</table>
<div class="steps" style="font-size:11.5px">A on 0: q1–0→q1, q2–0→q3 ⇒ {q1,q3}
      ε-closure ⇒ {q1,q2,q3}  (q1 –ε→ q2)
A on 1: q1–1→q2, q2–1→{q2,q3} ⇒ {q2,q3}</div>
<div class="fig">{{eps73dfa}}</div>
<p class="cap">A is final because ε-closure(q1) contains q2: the empty word is accepted.</p>
</div>
</div>
</div>
"""

# ---------- Extra methods section ----------
EXTRAS = r"""
<h2 id="extra" class="pb">Extra methods <small>not (yet) on her slides — but classic exam questions</small></h2>
<div class="grid">
<div class="card">
<h3>A. Automaton → RegEx (Arden's lemma)</h3>
<p style="margin:2px 0"><b>Arden:</b> if <span class="m">X = rX | s</span> (and ε ∉ L(r)) then <span class="m">X = r*s</span>.</p>
<ol>
 <li>One unknown X<sub>q</sub> per state = "words that lead from q to a final state".</li>
 <li>For each arrow q –a→ p write <span class="m">aX<sub>p</sub></span>; add <span class="m">| ε</span> if q is final.</li>
 <li>Solve from the final states backwards, using Arden for loops.</li>
 <li>Answer = X<sub>q0</sub>.</li>
</ol>
<p style="margin:4px 0"><b>Example: "contains 01"</b> (Ch2 §2)</p>
<div class="steps">X0 = 1X0 | 0X1
X1 = 0X1 | 1X2
X2 = 0X2 | 1X2 | ε = (0|1)X2 | ε
⇒ X2 = (0|1)*            Arden
⇒ X1 = 0*1(0|1)*         Arden
⇒ X0 = 1*0 0*1(0|1)*     Arden
RegEx = 1*00*1(0|1)*</div>
<p style="margin:4px 0"><b>Example: slide 49</b>: X1 = aX2|bX2, X2 = aX3|bX4, X3 = (a|b)X3, X4 = ε ⇒ X3 = (a|b)*∅ = ∅ (dead state!), X2 = b, <b>X1 = (a|b)b</b>.</p>
</div>
<div class="card">
<h3>B. Automaton → RegEx (state elimination)</h3>
<ol>
 <li>Add a new start <b>i –ε→ q0</b> and a new final: every old final <b>–ε→ f</b>.</li>
 <li>Remove the other states one by one. For each path <b>p –x→ q –y→ r</b> with a loop <b>z</b> on q, write on p→r: <span class="m">(old label) | x z* y</span>.</li>
 <li>Several arrows between the same 2 states → join with |.</li>
 <li>At the end only i → f remains: its label is the RegEx.</li>
</ol>
<p style="margin:4px 0">Same "contains 01" example: remove q1 ⇒ q0 –00*1→ q2; remove q0 (loop 1) ⇒ i –1*00*1→ q2; remove q2 (loop 0|1) ⇒ <b>1*00*1(0|1)*</b>. ✔ same as Arden.</p>
</div>
<div class="card">
<h3>C. Operations on automata</h3>
<ul>
 <li><b>Complement</b> ¬L: complete DFA, then flip final / non-final.</li>
 <li><b>Union / intersection</b> (product construction): states = pairs (p, q), one from each DFA; <span class="m">δ((p,q), x) = (δ1(p,x), δ2(q,x))</span>; start (p0, q0).<br>Final for <b>∩</b>: both final. Final for <b>∪</b>: at least one final.</li>
 <li><b>Concatenation, star</b>: easiest via RegEx (L1L2, L*) then Glushkov.</li>
</ul>
<p style="margin:4px 0"><b>Example:</b> L1 = contains a (P0 → P1*), L2 = ends with b (Q0 → Q1*)</p>
<table>
<tr><th></th><th>a</th><th>b</th><th>∩</th><th>∪</th></tr>
<tr><td class="s">→(P0,Q0)</td><td>(P1,Q0)</td><td>(P0,Q1)</td><td></td><td></td></tr>
<tr><td class="s">(P0,Q1)</td><td>(P1,Q0)</td><td>(P0,Q1)</td><td></td><td>*</td></tr>
<tr><td class="s">(P1,Q0)</td><td>(P1,Q0)</td><td>(P1,Q1)</td><td></td><td>*</td></tr>
<tr><td class="s">(P1,Q1)</td><td>(P1,Q0)</td><td>(P1,Q1)</td><td>*</td><td>*</td></tr>
</table>
</div>
<div class="card">
<h3>D. Regular or NOT regular?</h3>
<p style="margin:2px 0"><b>Kleene's theorem:</b> L is regular ⇔ described by a RegEx ⇔ recognised by a finite automaton (DFA = NFA = ε-NFA in power).</p>
<p style="margin:4px 0">A finite automaton has <b>finite memory</b>: it cannot count without limit.</p>
<table class="l">
<tr><th>Regular ✔</th><th>NOT regular ✘</th></tr>
<tr><td>a*b* (aⁿbᵐ)</td><td>{aⁿbⁿ | n ≥ 0} = {ε, ab, aabb, …}</td></tr>
<tr><td>even number of a</td><td>same number of 0 and 1</td></tr>
<tr><td>contains / starts / ends with "ab"</td><td>{0ⁱ1ʲ | 0 ≤ i ≤ j}</td></tr>
<tr><td>number of a divisible by 3</td><td>palindromes, balanced parentheses</td></tr>
<tr><td>any finite language</td><td>{aⁿ | n prime}, {a<sup>n²</sup>}</td></tr>
</table>
<p style="margin:4px 0"><b>Pumping lemma:</b> if L is regular, there is p such that every w ∈ L with |w| ≥ p splits as w = xyz with |xy| ≤ p, |y| ≥ 1 and <b>xy<sup>k</sup>z ∈ L for all k ≥ 0</b>.</p>
<p style="margin:4px 0"><b>Proof aⁿbⁿ is not regular:</b> take w = a<sup>p</sup>b<sup>p</sup>. |xy| ≤ p ⇒ y is only a's. Pump k = 2: xy²z has more a's than b's ∉ L. Contradiction ⇒ not regular.</p>
</div>
<div class="card">
<h3>E. Chomsky hierarchy (where automata fit)</h3>
<table class="l">
<tr><th>Type</th><th>Languages</th><th>Machine</th></tr>
<tr><td>3</td><td>Regular (RegEx)</td><td>Finite automaton</td></tr>
<tr><td>2</td><td>Context-free (aⁿbⁿ, parentheses)</td><td>Pushdown automaton (stack)</td></tr>
<tr><td>1</td><td>Context-sensitive (aⁿbⁿcⁿ)</td><td>Linear bounded automaton</td></tr>
<tr><td>0</td><td>Recursively enumerable</td><td>Turing machine</td></tr>
</table>
<p style="margin:4px 0">Type 3 ⊂ Type 2 ⊂ Type 1 ⊂ Type 0: each machine is more powerful than the one above it.</p>
</div>
<div class="card">
<h3>F. Minimisation — the table (pairs) method <span class="tag">alternative</span></h3>
<ol>
 <li>Draw the triangle of all pairs {p, q}.</li>
 <li>Mark ✗ every pair with one final and one non-final.</li>
 <li>Repeat: mark {p,q} if for some letter x the pair {δ(p,x), δ(q,x)} is already marked.</li>
 <li>Unmarked pairs = equivalent ⇒ merge.</li>
</ol>
<p style="margin:4px 0">Same result as her "Step" method; use hers in the exam.</p>
</div>
</div>
"""

# ---------- Chapter 5 / 6 previews ----------
PREVIEW = r"""
<h2 id="ch5">Chapter 5 — Turing machine <small>preview: her slides are not out yet, so her notation may differ</small></h2>
<div class="grid">
<div class="card">
<h3>Definition</h3>
<p style="margin:2px 0"><span class="m">M = (Q, Σ, Γ, δ, q0, B, F)</span></p>
<ul>
 <li>Q states · Σ input alphabet · <b>Γ tape alphabet</b> (Σ ⊂ Γ) · <b>B</b> = blank symbol</li>
 <li>q0 initial · F final (accepting) states</li>
 <li><span class="m">δ : Q × Γ → Q × Γ × {L, R}</span>: <span class="m">δ(q, a) = (p, b, R)</span> = "in state q reading a: write b, move Right, go to p"</li>
</ul>
<p style="margin:4px 0"><b>How it works:</b> infinite tape, a read/write head. Unlike a FA it can <b>write</b> and move <b>both ways</b>. It accepts when it reaches a final state; it rejects when it is blocked (no transition) in a non-final state; it may also <b>loop forever</b>.</p>
<p style="margin:4px 0">Configuration notation: <span class="m">X a q1 b b</span> = tape "Xabb", head on the letter right after q1.</p>
<table class="l">
<tr><th></th><th>FA</th><th>Turing machine</th></tr>
<tr><td>Memory</td><td>states only</td><td>infinite tape</td></tr>
<tr><td>Head</td><td>reads, moves right</td><td>reads + writes, L or R</td></tr>
<tr><td>Recognises</td><td>regular languages</td><td>everything computable</td></tr>
</table>
</div>
<div class="card wide">
<h3>Classic example: L = {aⁿbⁿ | n ≥ 1}</h3>
<p style="margin:2px 0">Idea: mark the first a as <b>X</b>, go right to the first b, mark it <b>Y</b>, come back, repeat.</p>
<div class="tbl-wrap"><table>
<tr><th>δ</th><th>a</th><th>b</th><th>X</th><th>Y</th><th>B</th></tr>
<tr><td class="s">→q0</td><td>(q1,X,R)</td><td>-</td><td>-</td><td>(q3,Y,R)</td><td>-</td></tr>
<tr><td class="s">q1</td><td>(q1,a,R)</td><td>(q2,Y,L)</td><td>-</td><td>(q1,Y,R)</td><td>-</td></tr>
<tr><td class="s">q2</td><td>(q2,a,L)</td><td>-</td><td>(q0,X,R)</td><td>(q2,Y,L)</td><td>-</td></tr>
<tr><td class="s">q3</td><td>-</td><td>-</td><td>-</td><td>(q3,Y,R)</td><td>(q4,B,R)</td></tr>
<tr><td class="s">*q4</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr>
</table></div>
<div class="steps" style="font-size:11.5px">q0 aabb ⊢ X q1 abb ⊢ Xa q1 bb ⊢ X q2 aYb
⊢ q2 XaYb ⊢ X q0 aYb ⊢ XX q1 Yb ⊢ XXY q1 b
⊢ XX q2 YY ⊢ X q2 XYY ⊢ XX q0 YY ⊢ XXY q3 Y
⊢ XXYY q3 B ⊢ XXYYB q4   accepted ✔</div>
<p style="margin:4px 0">q0 = find next a · q1 = go right to a b · q2 = go back left · q3 = check only Y's remain · q4 = accept.</p>
</div>
</div>

<h2 id="ch6">Chapter 6 — Automata in AI <small>preview</small></h2>
<div class="grid">
<div class="card">
<h3>Where automata are used in AI</h3>
<ul>
 <li><b>NLP</b>: tokenisers and lexers are DFAs built from RegEx; morphology (word forms) with finite-state transducers.</li>
 <li><b>Data cleaning / extraction</b>: RegEx to find emails, dates, phone numbers before training a model.</li>
 <li><b>Agents, robots, games</b>: behaviour as a finite state machine (states = Idle, Patrol, Attack; transitions = events).</li>
 <li><b>Chatbots</b>: dialogue states (greeting → question → answer → goodbye).</li>
 <li><b>Speech / sequences</b>: probabilistic automata, Hidden Markov Models (states + transition probabilities).</li>
 <li><b>Verification</b>: model checking of critical / embedded systems, checking an AI policy never reaches a "bad" state.</li>
</ul>
</div>
<div class="card">
<h3>Mealy / Moore machines (automata with output)</h3>
<ul>
 <li><b>Moore</b>: output depends on the <b>state</b> only (e.g. traffic light: state Green ⇒ output "go").</li>
 <li><b>Mealy</b>: output depends on <b>state + input</b>; written on the arrow as <span class="m">input / output</span> (e.g. <span class="m">coin / unlock</span>).</li>
 <li>Used for controllers, vending machines, protocol design.</li>
</ul>
</div>
</div>
"""

# ---------- Practice ----------
PRACTICE = r"""
<h2 id="practice" class="pb">Practice — new exercises, answers hidden <small>tap "Answer" only after trying</small></h2>
<div class="grid">
<div class="card">
<h3>Chapter 1 — RegEx</h3>
<p class="ex">P1. Over {a,b}: RegEx for words with an <b>odd</b> number of a.</p>
<details><summary>Answer</summary><code>b*ab*(ab*ab*)*</code> — one a, then a's come in pairs. Words: a, ba, aaa, abab…</details>
<p class="ex">P2. Words over {a,b} that do <b>not contain "aa"</b>.</p>
<details><summary>Answer</summary><code>(b|ab)*(ε|a)</code> — every a is followed by b, except maybe a last a.</details>
<p class="ex">P3. List the 5 shortest words of <code>(a|bb)*b</code>.</p>
<details><summary>Answer</summary>b, ab, aab, bbb, aaab (lengths 1, 2, 3, 3, 4)</details>
<p class="ex">P4. True or false: <code>(ab)*a = a(ba)*</code> ? &nbsp; <code>(a|b)* = a*b*</code> ?</p>
<details><summary>Answer</summary>1st <b>True</b> (sliding rule: both give a, aba, ababa…). 2nd <b>False</b>: ba ∈ (a|b)* but ba ∉ a*b*.</details>
<p class="ex">P5. Simplify: <code>(a|ε)*</code> · <code>ε | a*a</code> · <code>a*(a|b)* | b</code> · <code>(a*b)*a*</code></p>
<details><summary>Answer</summary><code>a*</code> · <code>a*</code> · <code>(a|b)*</code> · <code>(a|b)*</code></details>
<p class="ex">P6. RegEx for numbers (no leading 0 except "0") divisible by 10 — digits d = [0-9].</p>
<details><summary>Answer</summary><code>0 | [1-9][0-9]*0</code></details>
</div>
<div class="card">
<h3>Chapter 2 — Glushkov &amp; minimisation</h3>
<p class="ex">P7. Glushkov automaton of <code>(a|b)*abb</code>.</p>
<details><summary>Answer</summary>
<span class="m">(a1|b2)* a3 b4 b5</span><br>
ɸ: a1 b2 a3 · a1: a1 b2 a3 · b2: a1 b2 a3 · a3: b4 · b4: b5 · <b>b5</b>: ɸ ⇒ F = {5}<br>
Arcs: 0,1,2 –a→ 1 and 3; 0,1,2 –b→ 2; 3 –b→ 4; 4 –b→ 5. It is an <b>NFA</b> (a goes to 1 and 3). Rows 0, 1, 2 are identical ⇒ merge as "0,1,2". See P13 for the DFA.
</details>
<p class="ex">P8. Glushkov automaton of <code>(ab|b)*a</code>.</p>
<details><summary>Answer</summary>
<span class="m">(a1b2 | b3)* a4</span> — ɸ: a1 b3 a4 · a1: b2 · b2: a1 b3 a4 · b3: a1 b3 a4 · <b>a4</b>: ɸ ⇒ F = {4}<br>
Arcs: 0 –a→ 1, 0 –b→ 3, 0 –a→ 4; 1 –b→ 2; 2 and 3 have the same arcs as 0 (rows 0, 2, 3 identical ⇒ merge).
</details>
<p class="ex">P9. Minimise (F = {E}). Remove unreachable states first.</p>
<table>
<tr><th></th><th>a</th><th>b</th></tr>
<tr><td class="s">→A</td><td>B</td><td>C</td></tr>
<tr><td class="s">B</td><td>B</td><td>D</td></tr>
<tr><td class="s">C</td><td>B</td><td>C</td></tr>
<tr><td class="s">D</td><td>B</td><td>E</td></tr>
<tr><td class="s">*E</td><td>B</td><td>C</td></tr>
<tr><td class="s">G</td><td>E</td><td>A</td></tr>
</table>
<details><summary>Answer</summary>
G is unreachable (no arrow goes to G) ⇒ delete it.
<div class="steps">Step0: (E) (A,B,C,D)
Step1: (E) (D) (A,B,C)      D –b→ E final
Step2: (E) (D) (B) (A,C)    B –b→ D
Step3: stable: A and C: a→B, b→C</div>
Result: 4 states "A,C", B, D, E — it is the DFA of (a|b)*abb.
</details>
<p class="ex">P10. With the DFA of P9: are <b>abb</b>, <b>abab</b>, <b>babb</b> accepted?</p>
<details><summary>Answer</summary>abb: A→B→D→E ✔ · abab: A→B→D→B→D ✘ (D not final) · babb: A→C→B→D→E ✔</details>
</div>
<div class="card">
<h3>Chapter 3 — DFA / NFA</h3>
<p class="ex">P11. DFA over {0,1}: words that <b>end with 01</b>.</p>
<details><summary>Answer</summary><div class="fig">{{p_end01}}</div>S0 = nothing useful · S1 = last letter 0 · S2 = ends with 01.</details>
<p class="ex">P12. DFA over {a,b}: number of a <b>divisible by 3</b>.</p>
<details><summary>Answer</summary><div class="fig">{{p_mod3}}</div>State = (number of a) mod 3; b changes nothing.</details>
<p class="ex">P13. Determinise the NFA of P7 (after merging 0,1,2 into S: S –a→ {S,3}, S –b→ S, 3 –b→ 4, 4 –b→ 5).</p>
<details><summary>Answer</summary>
<div class="steps">δ'([S],a) = [S,3] ← new
δ'([S],b) = [S]
δ'([S,3],a) = [S,3]
δ'([S,3],b) = [S,4] ← new
δ'([S,4],a) = [S,3]
δ'([S,4],b) = [S,5] ← new
δ'([S,5],a) = [S,3]
δ'([S,5],b) = [S]
A=[S], B=[S,3], C=[S,4], *D=[S,5]</div>
<div class="fig">{{p_abb}}</div>Same as P9's minimal DFA ✔
</details>
<p class="ex">P14. NFA: q0 –a→ {q0,q1}, q0 –b→ q0, q1 –b→ q2, F = {q2}. Convert to a DFA. Which language?</p>
<details><summary>Answer</summary>
<div class="steps">δ'([q0],a) = [q0,q1] ← new    δ'([q0],b) = [q0]
δ'([q0,q1],a) = [q0,q1]      δ'([q0,q1],b) = [q0,q2] ← new
δ'([q0,q2],a) = [q0,q1]      δ'([q0,q2],b) = [q0]</div>
<div class="fig">{{p_endab}}</div>Language: words ending with <b>ab</b> = <code>(a|b)*ab</code>.
</details>
<p class="ex">P15. ε-NFA: q0 –a→ q0, q0 –ε→ q1, q1 –b→ q1, F = {q1}. Convert to a DFA.</p>
<details><summary>Answer</summary>ε-closure(q0) = {q0,q1} (final, contains q1). [q0,q1] –a→ cl{q0} = [q0,q1]; –b→ [q1]. [q1] –b→ [q1], –a→ ϕ.<div class="fig">{{p_astarbstar}}</div>Language: <code>a*b*</code>.</details>
<p class="ex">P16. DFA for "does NOT end with 01".</p>
<details><summary>Answer</summary>Take P11 (complete DFA) and flip: S0, S1 final; S2 non-final.</details>
</div>
<div class="card">
<h3>Mixed / extra</h3>
<p class="ex">P17. RegEx of the DFA of P12 (number of a divisible by 3) — use Arden.</p>
<details><summary>Answer</summary>
<div class="steps">X0 = bX0 | aX1 | ε
X1 = bX1 | aX2      ⇒ X1 = b*aX2
X2 = bX2 | aX0      ⇒ X2 = b*aX0
⇒ X0 = bX0 | ab*ab*aX0 | ε = (b | ab*ab*a)X0 | ε
⇒ X0 = (b | ab*ab*a)*</div>
</details>
<p class="ex">P18. Is L = {aⁿb²ⁿ | n ≥ 0} regular?</p>
<details><summary>Answer</summary>No. Pumping lemma with w = a<sup>p</sup>b<sup>2p</sup>: y contains only a's, xy²z has too many a's ∉ L.</details>
<p class="ex">P19. Run the Turing machine (Ch5) on <b>aab</b>.</p>
<details><summary>Answer</summary>q0 aab ⊢ X q1 ab ⊢ Xa q1 b ⊢ X q2 aY ⊢ q2 XaY ⊢ X q0 aY ⊢ XX q1 Y ⊢ XXY q1 B → no transition, q1 not final ⇒ <b>rejected</b> ✔ (aab ∉ aⁿbⁿ)</details>
<p class="ex">P20. Is this automaton deterministic? 1 –a→ 2, 1 –b→ 1, 2 –a→ 2, 2 –a→ 1, 2 –b→ 1.</p>
<details><summary>Answer</summary>No: from 2, reading a goes to 2 <b>and</b> 1 ⇒ ambiguous ⇒ NFA (it is complete though).</details>
</div>
</div>
"""

CHECKLIST_ROWS = r"""
<tr><td>"Simplify the RegEx"</td><td>Identities table (Ch1 §7)</td></tr>
<tr><td>"Give the RegEx of this automaton"</td><td>Arden equations or state elimination</td></tr>
<tr><td>Automaton with ε-arrows</td><td>ε-closure + subset construction</td></tr>
<tr><td>"Is L regular?"</td><td>Build a FA/RegEx (yes) or pumping lemma (no)</td></tr>
<tr><td>"L1 ∩ L2", "L1 ∪ L2"</td><td>Product construction</td></tr>"""

STILL_TO_COME = r"""<h3>Coverage</h3>
<p style="margin:2px 0">✔ Everything in her 3 slide files (chapters 1–3) + all board exercises.<br>✔ Extra methods that exercises often need (simplification, ε-removal, automaton → RegEx, product, regular or not).<br>◐ Chapters 5–6 (Turing machine, automata in AI) are a <b>preview</b>: her slides are not out yet, so check her notation when they are.</p>"""
