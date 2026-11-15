# Mock DS: Answer key

> ⚠️ Open this **only after** you've finished the whole DS on paper under exam conditions (2 hours, no notes).
> Other correct answers are often possible (another column name, another data type size, another way of writing a query). If yours differs, send it to me and I'll tell you whether it's accepted.

---

## Exercise 1 (3 pts)

1. **a) Domain constraint**: the value must have the right data type.
2. **d) NOT NULL**
3. **a) FROM clause**
4. **c) INNER JOIN**
5. **b, c, d** are correct. **a is wrong**: GROUP BY always comes **after** WHERE. (For d: aggregate functions are written with parentheses, e.g. `COUNT(OrderID)`, `SUM(OrderQty)`.)
6.
   - **Relation**: a table.
   - **Tuple**: a row (a record).
   - **Attribute**: a column (a field).
   - **Domain**: the set of acceptable values a column can contain, depending on its data type.
7. **Degree** = number of **columns**. **Cardinality** = number of **rows** (records).
8. **Key** constraints, **domain** constraints, **referential integrity** constraints.
9. Minimize data duplication, avoid errors during data modifications, simplify data queries.
10. The **remainder** of a division (modulus). Example: `11 % 2 = 1`, so `hours % 2 = 0` means an even number of hours.
11. It's never kept as-is. It's split into **two one-to-many relationships** using a **junction (middle) table** that contains the primary keys of both tables as foreign keys.
12. Simplifying access to data, manipulating data, providing security.

---

## Exercise 2 (3 pts)

**1.**
```sql
CREATE DATABASE pharma_amira;
USE pharma_amira;
```

**2.**
- MedID → `INT` (whole number)
- MedicineName → `VARCHAR(100)` (text of variable length)
- **Price → `DECIMAL(6,3)`**: a number with fractions (Tunisian prices have 3 decimals)
- **ExpiryDate → `DATE`**: it stores dates
- Quantity → `INT`

**3.**
```sql
CREATE TABLE medicines (
  MedID INT,
  MedicineName VARCHAR(100),
  Price DECIMAL(6,3),
  ExpiryDate DATE,
  Quantity INT,
  PRIMARY KEY (MedID)
);
```

**4.** The card number is always 8 characters, so use a fixed-length `CHAR(8)`.
```sql
CREATE TABLE customers (
  CardNumber CHAR(8),
  FullName VARCHAR(100) NOT NULL,
  Email VARCHAR(255),
  City VARCHAR(50) DEFAULT 'Sousse',
  PRIMARY KEY (CardNumber)
);
```

**5.** The candidate keys are **Supplier ID, Tax number and Phone**: their values are unique in every row.
**Supplier name is NOT a candidate key**: "MediPlus" appears twice, so it doesn't uniquely identify a row.

**6.** **Supplier ID** is the best primary key: it's short, it never changes, and it's created just to identify suppliers. A phone number can change. Tax number and Phone are the **alternate keys**.

**7.** This is a **one-to-many (1:N)** relationship. The foreign key goes on the "many" side, so **SupplierID goes in the `medicines` table**.

**8.**
```sql
ALTER TABLE medicines ADD SupplierID VARCHAR(10);
ALTER TABLE medicines ADD FOREIGN KEY (SupplierID) REFERENCES suppliers(SupplierID);
```

---

## Exercise 3 (3 pts)

**1.**
- Teachers 1:N Courses
- Categories 1:N Courses
- Students M:N Courses
- Students 1:1 Student_cards

**2.** The M:N relationship is broken into two 1:N relationships using the **junction table `Enrollments`**. It contains StudentID and CourseID as **foreign keys**; together they form its **composite primary key**. It also stores the enrollment date and the grade.

**3.** ERD (draw these as boxes with crow's feet on the "many" side):
```
Teachers                Categories
PK TeacherID INT        PK CategoryID INT
   FullName VARCHAR(100)   Label VARCHAR(50)
   Email VARCHAR(255)
   Speciality VARCHAR(50)
      | 1                      | 1
      |                        |
      | N                      | N
Courses
PK CourseID INT
   Title VARCHAR(100)
   Price DECIMAL(6,2)
   Hours INT
FK TeacherID INT
FK CategoryID INT
      | 1
      | N
Enrollments                            Students
PK,FK StudentID INT   N ---------- 1   PK StudentID INT
PK,FK CourseID INT                        FullName VARCHAR(100)
      EnrollmentDate DATE                 BirthDate DATE
      Grade DECIMAL(4,2)                  Email VARCHAR(255)
                                                | 1
                                                | 1
                                         Student_cards
                                         PK CardNumber VARCHAR(10)
                                            IssueDate DATE
                                         FK StudentID INT (UNIQUE)
```

**4.**
```sql
CREATE TABLE enrollments (
  StudentID INT,
  CourseID INT,
  EnrollmentDate DATE,
  Grade DECIMAL(4,2),
  PRIMARY KEY (StudentID, CourseID),
  FOREIGN KEY (StudentID) REFERENCES students(StudentID),
  FOREIGN KEY (CourseID) REFERENCES courses(CourseID)
);
```

---

## Exercise 4 (3 pts)

**1.**
- Several values are stored in the same cell (Student ID, Student name, Lesson ID, Lesson price), which breaks **atomicity**.
- There are **repeating groups** of data (the instructor name, the agency city and the governorate are repeated).
- It's hard to update and query the data, and it's not easy to choose a primary key.

**2. 1NF.** Put one value per cell and separate the entities:
- **StudentLesson** (StudentID, StudentName, LessonID, LessonPrice): **PK = (StudentID, LessonID)**, a composite key, because S1 and S5 each appear twice.

  | StudentID | StudentName | LessonID | LessonPrice |
  |---|---|---|---|
  | S1 | Rim | L1 | 40 |
  | S2 | Hamza | L1 | 40 |
  | S3 | Nada | L2 | 45 |
  | S4 | Mehdi | L1 | 40 |
  | S5 | Lotfi | L3 | 50 |
  | S5 | Lotfi | L2 | 45 |
  | S6 | Wafa | L1 | 40 |
  | S1 | Rim | L3 | 50 |
  | S7 | Ines | L2 | 45 |

- **Instructor** (InstructorID, InstructorName): **PK = InstructorID**. Rows: I1 Sami Trabelsi, I2 Amel Ksouri.
- **Agency** (AgencyNo, AgencyCity, Governorate): **PK = AgencyNo**. Rows: 1 La Marsa Tunis; 2 Sousse Sousse; 3 Hammamet Nabeul.

**3.** A **partial dependency** is when a table has a composite primary key and a non-key attribute depends on **only one part** of that key.
- StudentName depends only on **StudentID**.
- LessonPrice depends only on **LessonID**.

**2NF:**
- **Student** (StudentID, StudentName): PK StudentID
- **Lesson** (LessonID, LessonPrice): PK LessonID. Rows: L1 40, L2 45, L3 50.
- **StudentLesson** (StudentID, LessonID): PK (StudentID, LessonID), both are FKs.

(The course version adds a new unique ID, like AppointmentID, instead of the link table. That's also accepted.)

**4.** A **transitive dependency** is when a non-key attribute depends on **another non-key attribute**. In Agency, **Governorate depends on AgencyCity**: if you change the city, you must change the governorate too.

**3NF:**
- **Agency** (AgencyNo, AgencyCity): PK AgencyNo, FK AgencyCity
- **City** (AgencyCity, Governorate): PK AgencyCity. Rows: La Marsa Tunis; Sousse Sousse; Hammamet Nabeul.

**5.**
```sql
CREATE TABLE StudentLesson (
  StudentID VARCHAR(10) NOT NULL,
  LessonID VARCHAR(10) NOT NULL,
  CONSTRAINT PK_StudentLesson PRIMARY KEY (StudentID, LessonID),
  FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
  FOREIGN KEY (LessonID) REFERENCES Lesson(LessonID)
);
```

---

## Exercise 5 (3 pts)

**1.**
```sql
CREATE TABLE employees (
  EmployeeID INT,
  EmployeeName VARCHAR(100),
  Department VARCHAR(50),
  AnnualSalary INT,
  PRIMARY KEY (EmployeeID)
);
```

**2.**
```sql
INSERT INTO employees (EmployeeID, EmployeeName, Department, AnnualSalary)
VALUES (1, 'Sami Ferchichi', 'Marketing', 52000),
       (2, 'Hela Mabrouk', 'Finance', 48000);
```

**3.**
```sql
SELECT * FROM employees ORDER BY EmployeeName ASC;
```

**4.**
```sql
SELECT EmployeeName, AnnualSalary / 12 AS MonthlySalary FROM employees;
```

**5.** Result: Sami Ferchichi.
```sql
SELECT * FROM employees WHERE Department = 'Marketing' AND AnnualSalary >= 50000;
```

**6.** Result: Hela, Slim, Ali, Nabil, Sara.
```sql
SELECT * FROM employees WHERE NOT AnnualSalary > 50000;
```

**7.** Result: Hela, Ali, Sara.
```sql
SELECT * FROM employees
WHERE Department IN ('Marketing', 'Finance', 'Legal') AND AnnualSalary < 50000;
```

**8.** Result: Hela, Slim, Ali, Sara. BETWEEN **includes** both limits, so Slim (30000) is in.
```sql
SELECT * FROM employees WHERE AnnualSalary BETWEEN 30000 AND 50000;
```

**9.** `S` followed by 3 underscores (exactly 3 more characters), then `%` (anything after). Result: Sami, Slim, Sonia, Sara.
```sql
SELECT * FROM employees WHERE EmployeeName LIKE 'S___%';
```

**10.**
```sql
DELETE FROM employees WHERE EmployeeID = 7;
```

**11.** Result: **Sami Ferchichi, Hela Mabrouk, Slim Gharbi, Nabil Hamdi**.
- 45000 and 61000 leave a remainder of 1000 when divided by 2000, so Ali and Sonia are out.
- Rym and Sara are in Legal, so they're out.

---

## Exercise 6 (3 pts)

**1.**
```sql
SELECT Customers.FullName, Customers.PhoneNumber, Bookings.BookingDate, Bookings.NumberOfGuests
FROM Customers INNER JOIN Bookings
ON Customers.CustomerID = Bookings.CustomerID;
```

**2.** Result: (1,10), (1,12), (1,14), **(2, NULL)**, (3,11), (4,13), **(5, NULL)**. **Mouna Kefi (2) and Tarek Mzali (5)** have no booking.
```sql
SELECT Customers.CustomerID, Bookings.BookingID
FROM Customers LEFT JOIN Bookings
ON Customers.CustomerID = Bookings.CustomerID;
```

**3.** Swap the tables:
```sql
SELECT Customers.CustomerID, Bookings.BookingID
FROM Bookings RIGHT JOIN Customers
ON Customers.CustomerID = Bookings.CustomerID;
```

**4.** 06-10 and 07-02 have 2 orders each; every other date has 1.
```sql
SELECT OrderDate, COUNT(OrderID) FROM orders GROUP BY OrderDate;
```

**5.** Result: Compost and Stones 20, Decking 250, Garden Decor 6, Lawn Care 52, Trees and Shrubs 20.
```sql
SELECT Department, SUM(OrderQty) FROM orders GROUP BY Department;
```

**6.** Result: 2022-06-01 → 1, 2022-06-10 → 2, 2022-06-25 → 1. WHERE filters the rows **before** grouping.
```sql
SELECT OrderDate, COUNT(OrderID) FROM orders
WHERE OrderDate BETWEEN '2022-06-01' AND '2022-06-30'
GROUP BY OrderDate;
```

**7.** Result: **Decking 2850, Garden Decor 2150, Lawn Care 2000**. Use HAVING because the condition is on a group, not on a row.
```sql
SELECT Department, SUM(OrderTotal) FROM orders
GROUP BY Department
HAVING SUM(OrderTotal) > 1500;
```

---

## Exercise 7 (2 pts)

**1.**
```sql
ALTER TABLE employees ADD Email VARCHAR(255);
```

**2.**
```sql
UPDATE employees SET AnnualSalary = AnnualSalary * 1.05 WHERE Department = 'Reception';
```

**3.** The average is 47,250. Result: **Sami (52000), Hela (48000), Rym (75000), Sonia (61000)**.
```sql
SELECT * FROM employees
WHERE AnnualSalary > (SELECT AVG(AnnualSalary) FROM employees);
```

**4.**
- **If ID 3 exists**: the old record is **deleted and replaced** by the new one, so Slim's salary becomes 32000 (it works like an update).
- **If ID 3 doesn't exist**: the record is simply **inserted** (it works like an INSERT INTO).

**5.** This illustrates **security**: users only see what you choose to show, and the salary stays hidden.
```sql
CREATE VIEW EmployeesPublic AS
SELECT EmployeeID, EmployeeName, Department FROM employees;
```

**6.**
```sql
ALTER TABLE employees CHANGE AnnualSalary Salary INT;
```

---

## Scoring

| Score | Meaning |
|---|---|
| 16–20 | Ready for the DS |
| 12–15 | Good. Review the exercises where you lost points |
| < 12 | Send me your answers and we'll go through the weak parts together |
