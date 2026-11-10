from fa import FA

D = {}

# ---------- Chapter 2 ----------
f = FA(380, 130)
f.state("q0", 50, 85, init="left"); f.state("q1", 185, 85); f.state("q2", 320, 85, final=True)
f.loop("q0", "1"); f.loop("q1", "0"); f.loop("q2", "0,1")
f.edge("q0", "q1", "0"); f.edge("q1", "q2", "1")
D["contains01"] = f.svg("DFA for strings containing 01")

f = FA(330, 230)
f.state("q0", 70, 55, init="left", final=True); f.state("q1", 260, 55)
f.state("q3", 70, 185); f.state("q2", 260, 185)
for a, b, l in [("q0", "q1", "1"), ("q1", "q0", "1"), ("q0", "q3", "0"), ("q3", "q0", "0"),
                ("q1", "q2", "0"), ("q2", "q1", "0"), ("q3", "q2", "1"), ("q2", "q3", "1")]:
    f.edge(a, b, l, bend=16)
D["even01"] = f.svg("DFA even number of 0 and 1")

f = FA(400, 210)
f.state("1", 50, 110, init="left"); f.state("2", 160, 110)
f.state("3", 270, 50, dead=True); f.state("4", 270, 170, final=True)
f.edge("1", "2", "a", bend=14); f.edge("1", "2", "b", bend=-14)
f.edge("2", "3", "a"); f.edge("2", "4", "b"); f.loop("3", "a,b", "right")
f.note(205, 15, "3 = dead state (trap)")
D["ex49"] = f.svg("automaton slide 49")

f = FA(380, 110)
f.state("q0", 50, 70, init="left"); f.state("q1", 185, 70); f.state("q2", 320, 70, final=True)
f.edge("q0", "q1", "a"); f.edge("q1", "q2", "b"); f.loop("q1", "ab")
D["aabb_star"] = f.svg("a(ab)*b")

# Glushkov a*b(a|c)*b
f = FA(500, 230)
f.state("0", 40, 115, init="up"); f.state("1", 140, 115); f.state("2", 240, 115)
f.state("4", 350, 50); f.state("3", 350, 180); f.state("5", 460, 115, final=True)
f.edge("0", "1", "a"); f.edge("0", "2", "b", bend=-55); f.loop("1", "a", "down")
f.edge("1", "2", "b"); f.edge("2", "3", "a"); f.edge("2", "4", "c"); f.edge("2", "5", "b", lo=-10)
f.loop("3", "a", "down"); f.loop("4", "c", "up")
f.edge("3", "4", "c", bend=24, t=0.28); f.edge("4", "3", "a", bend=24, t=0.28)
f.edge("3", "5", "b"); f.edge("4", "5", "b")
D["gl1"] = f.svg("Glushkov a*b(a|c)*b")

# Glushkov b(ab)*|(ba)*b
f = FA(430, 250)
f.state("0", 40, 125, init="left"); f.state("1", 150, 50, final=True); f.state("2", 270, 50); f.state("3", 390, 50, final=True)
f.state("4", 150, 150); f.state("5", 270, 150); f.state("6", 210, 225, final=True)
f.edge("0", "1", "b"); f.edge("1", "2", "a"); f.edge("2", "3", "b", bend=14); f.edge("3", "2", "a", bend=14)
f.edge("0", "4", "b"); f.edge("4", "5", "a", bend=14); f.edge("5", "4", "b", bend=14)
f.edge("0", "6", "b"); f.edge("5", "6", "b")
D["gl2"] = f.svg("Glushkov b(ab)*|(ba)*b")

# Glushkov (c+|a)b(ac)*b
f = FA(520, 230)
f.state("0", 40, 115, init="left"); f.state("1", 145, 50); f.state("2", 145, 180)
f.state("3", 255, 115); f.state("4", 370, 50); f.state("5", 370, 180); f.state("6", 480, 115, final=True)
f.edge("0", "1", "c"); f.edge("0", "2", "a"); f.loop("1", "c", "up")
f.edge("1", "3", "b"); f.edge("2", "3", "b"); f.edge("3", "4", "a"); f.edge("3", "6", "b", lo=-10)
f.edge("4", "5", "c", bend=24, t=0.28); f.edge("5", "4", "a", bend=24, t=0.28); f.edge("5", "6", "b")
D["gl3"] = f.svg("Glushkov (c+|a)b(ac)*b")

f = FA(470, 200)
f.state("0", 40, 100, init="left"); f.state("1", 145, 40); f.state("2", 145, 160)
f.state("35", 265, 100, rx=24, label="3,5"); f.state("4", 330, 30); f.state("6", 420, 100, final=True)
f.edge("0", "1", "c"); f.edge("0", "2", "a"); f.loop("1", "c", "up")
f.edge("1", "35", "b"); f.edge("2", "35", "b"); f.edge("35", "4", "a", bend=12); f.edge("4", "35", "c", bend=12)
f.edge("35", "6", "b")
D["gl3min"] = f.svg("minimised (c+|a)b(ac)*b")

# Minimisation example 1 (slide 60)
f = FA(450, 240)
f.state("12", 60, 70, init="left", rx=22, label="1,2"); f.state("5", 60, 190)
f.state("3", 220, 70); f.state("4", 220, 190)
f.state("6", 380, 70, final=True); f.state("78", 380, 190, final=True, rx=22, label="7,8")
f.loop("12", "a", "up"); f.edge("12", "5", "b", bend=-20); f.edge("5", "12", "a", bend=-20)
f.edge("5", "4", "b"); f.edge("3", "4", "a", bend=20); f.edge("4", "3", "a", bend=20)
f.edge("3", "6", "b"); f.edge("6", "3", "a", bend=22, lo=10); f.edge("4", "78", "b"); f.edge("6", "78", "b")
f.loop("78", "a,b", "right")
D["min1"] = f.svg("minimised automaton slide 60")

# Class exercise (a|ba|bba)*(b|bb|eps)
f = FA(470, 270)
f.state("0136", 210, 130, init="down", rx=36, label="0,1,3,6")
f.state("2", 60, 50); f.state("4", 60, 215); f.state("5", 210, 245)
f.state("8", 400, 40); f.state("7910", 395, 200, final=True, rx=34, label="7,9,10")
f.loop("0136", "a", "up")
f.edge("0136", "2", "b", bend=14); f.edge("2", "0136", "a", bend=14)
f.edge("0136", "4", "b"); f.edge("4", "5", "b"); f.edge("5", "0136", "a", bend=-20, lo=-10)
f.edge("0136", "8", "b"); f.edge("8", "7910", "b"); f.edge("0136", "7910", "b, ε", lo=-12)
D["minclass"] = f.svg("class exercise minimised")

# ---------- Chapter 3 ----------
f = FA(330, 140)
f.state("q0", 50, 60, init="left"); f.state("q1", 170, 60); f.state("q2", 290, 60, final=True)
f.edge("q0", "q1", "1", bend=22); f.edge("q1", "q0", "1", bend=22)
f.edge("q1", "q2", "1", bend=-20); f.edge("q2", "q1", "0", bend=-20); f.loop("q2", "1", "right")
D["activity"] = f.svg("activity slide 66")

f = FA(330, 210)
f.state("A", 50, 60, init="left"); f.state("B", 200, 60, final=True); f.state("C", 50, 170, dead=True)
f.edge("A", "B", "0"); f.edge("A", "C", "1"); f.loop("B", "0,1", "right"); f.loop("C", "0,1", "right")
f.note(95, 200, "C = dead state (catches every 'wrong' word)")
D["starts0"] = f.svg("DFA starts with 0")

f = FA(470, 100)
for i, (s, fin) in enumerate([("A", 0), ("B", 0), ("C", 1), ("D", 0)]):
    f.state(s, 50 + i * 120, 60, init="left" if s == "A" else None, final=bool(fin), dead=(s == "D"))
f.edge("A", "B", "0,1"); f.edge("B", "C", "0,1"); f.edge("C", "D", "0,1"); f.loop("D", "0,1", "up")
D["len2"] = f.svg("DFA length 2")


def aabb(comp):
    f = FA(560, 170)
    for i, s in enumerate("ABCDE"):
        fin = (s != "E") if comp else (s == "E")
        f.state(s, 50 + i * 115, 100, init="left" if s == "A" else None, final=fin)
    f.loop("A", "b", "up"); f.edge("A", "B", "a", bend=12); f.edge("B", "A", "b", bend=12)
    f.edge("B", "C", "a"); f.loop("C", "a", "up"); f.edge("C", "D", "b")
    f.edge("D", "B", "a", bend=-55, lo=-10, t=0.3); f.edge("D", "E", "b"); f.loop("E", "a,b", "up")
    return f.svg("aabb")


D["aabb"] = aabb(False)
D["noaabb"] = aabb(True)

f = FA(400, 150)
f.state("q0", 50, 90, init="left"); f.state("q1", 200, 90); f.state("q2", 340, 90, final=True)
f.loop("q0", "0"); f.loop("q1", "0,1"); f.loop("q2", "0,1")
f.edge("q0", "q1", "1"); f.edge("q1", "q2", "0", bend=16); f.edge("q2", "q1", "1", bend=16)
D["nfa1"] = f.svg("NFA example 1")

f = FA(400, 130)
f.state("q0", 50, 80, init="left", label="q0"); f.state("q1", 190, 80, label="q1")
f.state("q3", 330, 80, final=True, label="q3")
f.loop("q0", "0"); f.loop("q1", "1"); f.loop("q3", "0,1")
f.edge("q0", "q1", "1"); f.edge("q1", "q3", "0")
f.note(250, 125, "q3 = [q1,q2]")
D["dfa1"] = f.svg("DFA example 1")

f = FA(380, 200)
f.state("q0", 55, 60, init="left", rx=22, label="[q0]"); f.state("q01", 300, 60, final=True, rx=28, label="[q0,q1]")
f.state("q1", 55, 165, final=True, rx=22, label="[q1]")
f.edge("q0", "q01", "0"); f.edge("q0", "q1", "1"); f.edge("q1", "q01", "1"); f.loop("q01", "0,1", "up")
D["dfa2"] = f.svg("DFA example 2")

# epsilon NFA slide 79
f = FA(400, 250)
f.state("0", 40, 125, init="up"); f.state("1", 140, 60); f.state("2", 250, 60); f.state("3", 360, 60, final=True)
f.state("4", 140, 190); f.state("5", 250, 190); f.state("6", 360, 190, final=True)
f.edge("0", "1", "ε"); f.edge("0", "4", "ε", lo=-10)
f.loop("1", "a,b"); f.edge("1", "2", "a"); f.edge("2", "3", "a"); f.loop("3", "a,b")
f.loop("4", "a,b", "down"); f.edge("4", "5", "b"); f.edge("5", "6", "b"); f.loop("6", "a,b", "down")
D["enfa"] = f.svg("epsilon NFA")

f = FA(380, 220)
f.state("A", 50, 110, init="left"); f.state("B", 180, 40); f.state("C", 180, 180)
f.state("F", 320, 110, final=True)
f.edge("A", "B", "a"); f.edge("A", "C", "b", lo=-10); f.edge("B", "C", "b", bend=20); f.edge("C", "B", "a", bend=20)
f.edge("B", "F", "a"); f.edge("C", "F", "b", lo=-10); f.loop("F", "a,b", "right")
D["edfa"] = f.svg("DFA for epsilon NFA")
