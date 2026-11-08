"""All diagrams of the Information System revision guide (drawn with uml.py)."""
from uml import Diagram


def uc_basic():
    d = Diagram(700, 300)
    d.boundary(200, 20, 310, 265, "Web site  (the system)")
    d.actor("L", 90, 140, "Lector")
    d.actor("A", 620, 140, "Admin")
    d.uc("check", 285, 85, "Check content")
    d.uc("nav", 285, 200, "Navigate")
    d.uc("man", 425, 70, "Manage content")
    d.uc("pub", 425, 150, "Publish content")
    d.uc("def", 425, 230, "Define navigation")
    for u in ("check", "nav"):
        d.assoc("L", u)
    for u in ("man", "pub", "def"):
        d.assoc("A", u)
    d.text(90, 215, "← actor (outside)", 10, "#c62828", bold=True)
    d.text(285, 262, "↑ use case (inside)", 10, "#c62828", bold=True)
    d.text(355, 296, "rectangle = system boundary", 10, "#c62828", bold=True)
    return d.svg()


def uc_rel():
    d = Diagram(720, 360)
    d.uc("login", 95, 45, "Log in")
    d.uc("verif", 300, 45, "Verify authentication\ninformation")
    d.include("login", "verif")
    d.text(440, 40, "INCLUDE: Log in ALWAYS does Verify.", 11, anchor="start", bold=True)
    d.text(440, 56, "Arrow: base UC → included UC", 10.5, anchor="start")
    d.uc("err", 95, 135, "Display error")
    d.uc("verif2", 300, 135, "Verify authentication\ninformation")
    d.extend("err", "verif2")
    d.text(440, 130, "EXTEND: Display error happens SOMETIMES", 11, anchor="start", bold=True)
    d.text(440, 146, "(only if the info is wrong).", 10.5, anchor="start")
    d.text(440, 162, "Arrow: optional UC → base UC", 10.5, anchor="start")
    d.uc("stock", 215, 225, "Manage stock")
    d.uc("add", 120, 310, "Add stock")
    d.uc("del", 310, 310, "Delete stock")
    d.gen("add", "stock")
    d.gen("del", "stock")
    d.actor("U", 520, 290, "User")
    d.actor("Ad", 660, 290, "Admin")
    d.gen("Ad", "U")
    d.text(215, 350, "Generalization of UCs: Add / Delete are kinds of Manage", 10, "#555")
    d.text(590, 350, "Admin is a kind of User (does all User does + more)", 10, "#555")
    return d.svg()


def uc_mult():
    d = Diagram(720, 200)
    d.actor("B", 60, 45, "Bank")
    d.uc("t", 260, 50, "Transfer funds")
    d.assoc("B", "t", mb="1..n", arrow=True)
    d.text(160, 110, "multiplicity at the UC end: the Bank", 10, "#555")
    d.text(160, 124, "runs SEVERAL transfers (parallel, in turn…)", 10, "#555")
    d.actor("P", 430, 45, "Player")
    d.uc("c", 630, 50, "Play cards")
    d.assoc("P", "c", ma="2..n", arrow=True)
    d.text(540, 110, "multiplicity at the actor end: SEVERAL", 10, "#555")
    d.text(540, 124, "players are needed for ONE game", 10, "#555")
    d.actor("U1", 60, 160, "User")
    d.uc("s", 210, 165, "Sign in")
    d.assoc("U1", "s", arrow=True)
    d.actor("U2", 320, 160, "User")
    d.uc("b", 470, 165, "Display balance")
    d.assoc("b", "U2", arrow=True)
    d.actor("U3", 560, 160, "User")
    d.uc("i", 650, 165, "Search info", w=110)
    d.assoc("U3", "i")
    return d.svg()


def library():
    d = Diagram(700, 330)
    d.boundary(215, 15, 270, 305, "Library management system")
    d.actor("M", 90, 90, "Member")
    d.actor("Li", 610, 230, "Librarian")
    ucs = [("s", "Search for a book"), ("b", "Borrow a book"), ("r", "Return a book"),
           ("a", "Add a new book"), ("rm", "Remove a book"), ("reg", "Register a new member")]
    for i, (k, t) in enumerate(ucs):
        d.uc(k, 350, 55 + i * 50, t)
    for k in ("s", "b", "r"):
        d.assoc("M", k)
    for k in ("a", "rm", "reg"):
        d.assoc("Li", k)
    return d.svg()


def training():
    d = Diagram(720, 460)
    d.boundary(165, 15, 385, 435, "Training management system")
    d.actor("E", 70, 180, "Employee")
    d.actor("TM", 640, 110, "Training\nmanager")
    d.actor("TO", 640, 360, "Training\norganization")
    left = [("req", "Submit training\nrequest"), ("cat", "Consult training\ncatalog"),
            ("choose", "Choose a session"), ("unav", "Report\nunavailability"),
            ("feed", "Submit feedback +\nattendance proof")]
    right = [("rev", "Review request\n(approve/reject)"), ("search", "Search suitable\ntraining"),
             ("mcat", "Maintain catalog"), ("reg", "Register employee\nin a session"),
             ("cancel", "Request\ncancellation"), ("inv", "Verify invoice")]
    for i, (k, t) in enumerate(left):
        d.uc(k, 270, 60 + i * 75, t, w=150)
    for i, (k, t) in enumerate(right):
        d.uc(k, 450, 55 + i * 72, t, w=150)
    d.extend("cat", "req")
    d.extend("search", "rev", cond="approved")
    for k in ("req", "choose", "unav", "feed"):
        d.assoc("E", k)
    for k in ("rev", "mcat", "reg", "cancel", "inv"):
        d.assoc("TM", k)
    for k in ("reg", "cancel", "inv"):
        d.assoc("TO", k)
    return d.svg()


def textile():
    d = Diagram(720, 530)
    d.boundary(150, 10, 460, 480, "Product information system (textile)")
    d.actor("E", 70, 115, "Employee\n(all personnel)")
    d.actor("En", 70, 320, "Engineer")
    d.actor("P", 70, 440, "Personnel\nmanagement\nsystem")
    d.gen("En", "E")
    d.uc("light", 260, 45, "Light authentication")
    d.uc("cons", 260, 120, "Consult products")
    d.uc("chk", 465, 75, "Check a product exists")
    d.uc("brw", 465, 150, "Browse information")
    d.uc("print", 260, 235, "Print documents")
    d.uc("log", 480, 245, "Save in access log")
    d.uc("upd", 260, 350, "Update products")
    d.uc("strong", 260, 445, "Strong authentication")
    d.uc("add", 480, 320, "Add product")
    d.uc("mod", 480, 375, "Modify product")
    d.uc("rem", 480, 430, "Remove product")
    d.assoc("E", "cons")
    d.assoc("En", "upd")
    d.assoc("P", "strong")
    d.include("cons", "light")
    d.include("upd", "strong")
    d.gen("chk", "cons")
    d.gen("brw", "cons")
    for k in ("add", "mod", "rem"):
        d.gen(k, "upd")
    d.include("cons", "log", via=[(375, 120), (375, 210)])
    d.include("upd", "log")
    d.extend("print", "cons")
    d.extend("print", "upd")
    return d.svg()


def medialib():
    d = Diagram(720, 510)
    d.boundary(150, 10, 500, 490, "Media library system")
    d.actor("E", 70, 240, "Employee")
    d.uc("mm", 265, 100, "Manage members")
    d.uc("am", 490, 50, "Add member")
    d.uc("um", 490, 98, "Update member")
    d.uc("dm", 490, 146, "Delete member")
    d.uc("mw", 265, 225, "Manage works")
    d.uc("aw", 490, 195, "Add work")
    d.uc("mow", 490, 243, "Modify work")
    d.uc("dw", 490, 291, "Delete work")
    d.uc("co", 265, 330, "Check out a work")
    d.uc("sm", 520, 345, "Search member")
    d.uc("ret", 265, 400, "Return a work")
    d.uc("disp", 520, 410, "Manage disputes")
    d.uc("legal", 520, 470, "Manage legal\nproceedings")
    d.uc("login", 265, 470, "Log in")
    for k in ("mm", "mw", "co", "ret", "login"):
        d.assoc("E", k)
    for k in ("am", "um", "dm"):
        d.gen(k, "mm")
    for k in ("aw", "mow", "dw"):
        d.gen(k, "mw")
    d.include("co", "sm")
    d.extend("disp", "ret", cond="late > 3 weeks")
    d.extend("legal", "disp", cond="> 1 year")
    return d.svg()


def ecommerce_uc():
    d = Diagram(720, 470)
    d.boundary(165, 10, 440, 450, "E-commerce website")
    d.actor("V", 70, 75, "Visitor")
    d.actor("C", 70, 300, "Customer")
    d.actor("S", 650, 160, "Seller")
    d.actor("A", 650, 360, "Admin")
    d.gen("C", "V")
    d.uc("browse", 290, 45, "Browse products")
    d.uc("login", 290, 110, "Register / Log in")
    d.uc("cart", 280, 190, "Manage cart")
    d.uc("order", 280, 250, "Place an order")
    d.uc("pay", 280, 310, "Pay the order")
    d.uc("track", 280, 370, "Track an order")
    d.uc("fb", 280, 430, "Send feedback")
    d.uc("prod", 495, 140, "Manage products")
    d.uc("acc", 495, 210, "Process orders /\naccept payment", w=140)
    d.uc("users", 495, 360, "Manage users")
    for k in ("browse", "login"):
        d.assoc("V", k)
    for k in ("cart", "order", "pay", "track", "fb"):
        d.assoc("C", k)
    for k in ("prod", "acc"):
        d.assoc("S", k)
    d.assoc("A", "users")
    d.include("order", "login", via=[(395, 250), (395, 118)])
    return d.svg()


def room_uc():
    d = Diagram(720, 410)
    d.boundary(170, 10, 450, 390, "Reservation system")
    d.actor("S", 70, 60, "Student")
    d.actor("T", 70, 210, "Teacher")
    d.actor("H", 70, 345, "Head teacher\n(of a program)")
    d.gen("H", "T")
    d.uc("sched", 300, 55, "Consult room schedule")
    d.uc("room", 300, 135, "Reserve a room")
    d.uc("eq", 300, 210, "Reserve equipment")
    d.uc("avail", 510, 172, "Check availability")
    d.uc("sum", 300, 285, "Consult hourly summary")
    d.uc("edit", 300, 360, "Edit program's\nhourly summary", w=150)
    d.assoc("S", "sched")
    for k in ("sched", "room", "eq", "sum"):
        d.assoc("T", k)
    d.assoc("H", "edit")
    d.include("room", "avail")
    d.include("eq", "avail")
    return d.svg()


# ------------------------------------------------------------------ class diagrams
def class_box():
    d = Diagram(330, 150)
    d.cls("b", 165, 75, "BankAccount",
          ["- number: String", "- balance: double"],
          ["+ deposit(amount: double): void", "+ getBalance(): double"])
    return d.svg()


def class_rel():
    d = Diagram(720, 420)
    d.cls("cu", 80, 45, "Customer", w=100)
    d.cls("or", 330, 45, "Order", w=100)
    d.assoc("cu", "or", label="places", ma="1", mb="0..*")
    d.text(410, 40, "ASSOCIATION: a customer places 0 or many orders;", 10.5, anchor="start", bold=True)
    d.text(410, 55, "an order is placed by exactly 1 customer.", 10.5, anchor="start")
    d.cls("u", 205, 130, "User", w=90)
    d.cls("st", 110, 210, "Student", w=90)
    d.cls("te", 300, 210, "Teacher", w=90)
    d.gen("st", "u")
    d.gen("te", "u")
    d.text(410, 165, "GENERALIZATION (inheritance, \"is a\"):", 10.5, anchor="start", bold=True)
    d.text(410, 180, "a Student IS A User → inherits id, name…", 10.5, anchor="start")
    d.text(410, 195, "Java: class Student extends User", 10.5, anchor="start")
    d.cls("tm", 80, 290, "Team", w=100)
    d.cls("dv", 330, 290, "Developer", w=100)
    d.assoc("tm", "dv", ma="1", mb="1..*", kind="agg")
    d.text(410, 285, "AGGREGATION (empty ◇, \"has\"): the developer", 10.5, anchor="start", bold=True)
    d.text(410, 300, "can exist without the team (he can change team).", 10.5, anchor="start")
    d.cls("o2", 80, 375, "Order", w=100)
    d.cls("ol", 330, 375, "OrderLine", w=100)
    d.assoc("o2", "ol", ma="1", mb="1..*", kind="comp")
    d.text(410, 370, "COMPOSITION (filled ◆, \"made of\"): an order line", 10.5, anchor="start", bold=True)
    d.text(410, 385, "can't exist without its order (delete order → lines die).", 10.5, anchor="start")
    return d.svg()


def assoc_class():
    d = Diagram(720, 190)
    d.cls("s", 90, 50, "Student", w=100)
    d.cls("c", 400, 50, "Course", w=100)
    d.assoc("s", "c", label="enrolls in", ma="0..*", mb="1..*")
    d.cls("e", 245, 150, "Enrollment", ["- grade: double", "- date: Date"], w=130)
    d.lines.append('<path d="M245,50 L245,112" stroke="#333" stroke-dasharray="5,4" fill="none"/>')
    d.text(480, 125, "ASSOCIATION CLASS: the grade belongs", 10.5, anchor="start", bold=True)
    d.text(480, 140, "neither to the student alone nor to the", 10.5, anchor="start")
    d.text(480, 155, "course alone, but to the PAIR (student, course).", 10.5, anchor="start")
    d.text(480, 170, "Typical with many-to-many (* — *).", 10.5, anchor="start")
    return d.svg()


def room_class():
    d = Diagram(760, 520)
    d.cls("u", 330, 50, "User", ["- id: int", "- name: String"])
    d.cls("s", 130, 150, "Student", ["- studentNumber: String"])
    d.cls("t", 470, 150, "Teacher", ["- teacherNumber: String"])
    d.gen("s", "u")
    d.gen("t", "u")
    d.cls("p", 120, 330, "Program", ["- programID: int", "- name: String"])
    d.cls("h", 360, 330, "HourlySummary", ["- hsID: int", "- totalHours: double"], ["+ compute(): void"])
    d.cls("r", 630, 310, "Reservation", ["- reservationID: int", "- date: Date", "- startTime: Time", "- endTime: Time"])
    d.cls("c", 470, 465, "Classroom", ["- roomNumber: int", "- capacity: int"])
    d.cls("e", 660, 465, "Equipment", ["- equipmentID: int", "- type: String"])
    d.assoc("t", "p", label="is head teacher of", ma="1", mb="0..1")
    d.assoc("t", "h", label="has", ma="1", mb="0..*")
    d.assoc("h", "p", label="belongs to", ma="0..*", mb="1")
    d.assoc("t", "r", label="makes", ma="1", mb="0..*")
    d.assoc("r", "c", label="concerns", ma="0..*", mb="0..1")
    d.assoc("r", "e", label="uses", ma="0..*", mb="0..*", side=-1)
    return d.svg()


def ecom_class():
    d = Diagram(760, 570)
    d.cls("u", 380, 70, "User", ["- id: int", "- name: String", "- email: String", "- password: String"], ["+ login(): boolean", "+ logout(): void"])
    d.cls("cu", 120, 225, "Customer", ["- address: String"], ["+ placeOrder(): Order"])
    d.cls("se", 380, 225, "Seller", ["- shopName: String"], ["+ addProduct(p: Product)"])
    d.cls("ad", 630, 225, "Admin", [], ["+ manageUsers(): void"])
    for k in ("cu", "se", "ad"):
        d.gen(k, "u")
    d.cls("ca", 120, 365, "Cart", ["- createdAt: Date"], ["+ getTotal(): double"])
    d.cls("or", 380, 365, "Order", ["- orderID: int", "- date: Date", "- status: String"], ["+ getTotal(): double"])
    d.cls("pr", 640, 365, "Product", ["- productID: int", "- name: String", "- price: double", "- stock: int"])
    d.cls("pa", 230, 485, "Payment", ["- amount: double", "- method: String"])
    d.cls("ol", 500, 485, "OrderLine", ["- quantity: int", "- unitPrice: double"])
    d.assoc("cu", "ca", label="owns", ma="1", mb="1")
    d.assoc("cu", "or", label="places", ma="1", mb="0..*")
    d.assoc("se", "pr", label="sells", ma="1", mb="0..*")
    d.assoc("or", "pa", label="paid by", ma="1", mb="0..1")
    d.assoc("or", "ol", ma="1", mb="1..*", kind="comp")
    d.assoc("ol", "pr", label="refers to", ma="0..*", mb="1")
    d.assoc("ca", "pr", label="contains", ma="0..*", mb="0..*", via=[(120, 555), (740, 555), (740, 365)])
    return d.svg()


def mines_class():
    d = Diagram(760, 510)
    d.cls("g", 380, 45, "Game", ["- state: String"], ["+ start(): void", "+ end(lost: boolean): void"])
    d.cls("b", 140, 195, "Board", ["- rows: int", "- columns: int"], ["+ uncover(c: Cell): void", "+ mark(c: Cell): void"])
    d.cls("t", 420, 195, "Timer", ["- seconds: int"], ["+ start(): void", "+ stop(): void"])
    d.cls("m", 640, 195, "MineCounter", ["- remaining: int"], ["+ increment(): void", "+ decrement(): void"])
    for k in ("b", "t", "m"):
        d.assoc("g", k, ma="1", mb="1", kind="comp")
    d.cls("c", 140, 370, "Cell", ["- covered: boolean", "- flagged: boolean"], ["+ uncover(): void", "+ toggleFlag(): void"])
    d.assoc("b", "c", ma="1", mb="1..*", kind="comp")
    d.assoc("c", "c", label="neighbour of", ma="0..8", mb="0..8", via=[(130, 478), (30, 478), (30, 398)])
    d.cls("ct", 500, 370, "Content", [], [], stereo="abstract")
    d.assoc("c", "ct", label="contains", ma="1", mb="1")
    d.cls("em", 380, 465, "Empty", [], [], w=90)
    d.cls("mi", 500, 465, "Mine", [], [], w=90)
    d.cls("nu", 640, 465, "Number", ["- value: int"], [], w=110)
    for k in ("em", "mi", "nu"):
        d.gen(k, "ct")
    return d.svg()


def team_class():
    d = Diagram(760, 540)
    d.cls("co", 110, 50, "Company", ["- name: String"])
    d.cls("tm", 400, 50, "Team", ["- id: String", "- logo: String"])
    d.assoc("tm", "co", label="works for", ma="0..*", mb="1")
    d.cls("dv", 400, 200, "Developer", ["- idNumber: int", "- lastName: String", "- firstName: String", "- email: String"], [], stereo="abstract")
    d.assoc("tm", "dv", ma="1", mb="1..*", kind="agg")
    d.cls("pc", 660, 200, "Computer", ["- serialNumber: String"])
    d.assoc("dv", "pc", label="uses", ma="1..*", mb="1")
    d.cls("pg", 220, 350, "Programmer", [], ["+ writeCode(): void"])
    d.cls("ds", 580, 350, "Designer", [], ["+ interactWithUsers(): void", "+ createModels(): void"])
    d.gen("pg", "dv")
    d.gen("ds", "dv")
    d.cls("la", 220, 500, "Language", ["- name: String"])
    d.cls("mm", 580, 500, "ModelingMethod", ["- name: String"])
    d.assoc("pg", "la", label="specialized in", ma="0..*", mb="1..*")
    d.assoc("ds", "mm", label="expert in", ma="0..*", mb="1")
    return d.svg()


def team_obj():
    d = Diagram(760, 420)
    o = dict(obj=True, fill="#f2fbf4")
    d.cls("ts", 110, 45, "techSoft : Company", ['name = "TechSoft"'], **o)
    d.cls("dev", 400, 45, "dev : Team", ['id = "DEV"', 'logo = "DEV+"'], **o)
    d.cls("ali", 200, 190, "ali : Programmer", ['firstName = "Ali"'], **o)
    d.cls("zied", 400, 190, "zied : Programmer", ['firstName = "Zied"'], **o)
    d.cls("anis", 600, 190, "anis : Designer", ['firstName = "Anis"'], **o)
    d.cls("ada", 66, 190, "ada : Language", ['name = "Ada"'], **o)
    d.cls("java", 300, 320, "java : Language", ['name = "Java"'], **o)
    d.cls("pc", 500, 320, "pc1 : Computer", [], **o)
    d.cls("uml", 672, 320, "uml : ModelingMethod", ['name = "UML"'], **o)
    d.assoc("dev", "ts")
    for k in ("ali", "zied", "anis"):
        d.assoc("dev", k)
    d.assoc("ali", "ada")
    d.assoc("zied", "java")
    d.assoc("anis", "uml")
    d.assoc("zied", "pc")
    d.assoc("anis", "pc")
    d.assoc("ali", "pc", via=[(200, 395), (500, 395)])
    return d.svg()


ALL = {k: v for k, v in globals().items() if callable(v) and k not in ("Diagram",)}
