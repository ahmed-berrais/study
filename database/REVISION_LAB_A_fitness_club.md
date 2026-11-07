# Revision Lab A: "Carthage Fitness Club" (guided, covers every chapter)

> **DS scope: SQL operators → Views.** Ch1 (operators, relational model, keys, constraints, ERD, schema, normalization) + Ch2 (filtering, aliases, all joins incl. SELF/FULL, UNION, GROUP BY/HAVING, EXISTS/ANY/ALL, INSERT/UPDATE/DELETE/REPLACE, constraints, ALTER, subqueries, **views**).
> Parts 13–14 (functions, stored procedures) are **after views → NOT in the DS**. They're marked ⛔ at the end: skip them for now.
> Work in **MySQL**. Write every answer down (paper for theory/ERD, a `.sql` file for code). Don't look up solutions. Come back to me with your answers and I'll correct them.

---

## The scenario

Carthage Fitness Club wants a database. The manager's description:

- The club employs **coaches**. Each coach has an ID, a full name, a speciality and a monthly salary.
- The club has **rooms**. Each room has a code, a floor and a maximum capacity.
- The club runs **classes** (Crossfit, Yoga…). Each class has an ID, a name and a monthly price. **Each class is taught by exactly one coach and takes place in exactly one room.** A coach can teach several classes. A room can host several classes.
- **Members** have an ID, first name, last name, birth date, a unique email and a phone (some members never gave one).
- A member can enroll in **many classes**, and a class has **many members**. For each enrollment the club stores the **enrollment date** and the **fee actually paid** (it can differ from the price because of discounts).
- Every member gets **exactly one locker**, and a locker belongs to **exactly one member**. A locker has a number and a size (S/M/L).

Right now the manager keeps everything in **one spreadsheet**:

| CoachID | CoachName | Speciality | ClassID | ClassName | Room | RoomFloor | MemberIDs | MemberNames | FeesPaid |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Amine Bensalem | Fitness | CL1 | Crossfit | R1 | 1 | M1, M2, M4 | Sarra Mansour, Youssef Ayari, Omar Khelifi | 60, 60, 55 |
| C2 | Ines Trabelsi | Yoga | CL2 | Yoga Morning | R2 | 2 | M1, M3 | Sarra Mansour, Lina Haddad | 50, 50 |
| C3 | Karim Jlassi | Boxing | CL3 | Boxing Basics | R3 | 0 | M2, M4 | Youssef Ayari, Omar Khelifi | 70, 70 |
| C2 | Ines Trabelsi | Yoga | CL4 | Yoga Evening | R2 | 2 | M3 | Lina Haddad | 45 |
| C1 | Amine Bensalem | Fitness | CL5 | Cardio | R1 | 1 | M6, M1 | Ahmed Zribi, Sarra Mansour | 40, 40 |

---

## PART 1: Relational model and normalization (Ch1)

1. List **3 problems** with this spreadsheet (think: atomicity, repeating groups, update anomalies, choosing a primary key).
2. Is it in 1NF? Why or why not? Transform it into **1NF** (one value per cell) and show the resulting table(s).
3. In your 1NF table the key is composite. Which **composite key** did you pick? List every **partial dependency** you can find (non-key attribute → only part of the key).
4. Bring the design to **2NF**. Show the tables.
5. Find the **transitive dependency** hidden in the data (hint: look at `Room` and `RoomFloor` in the class table). Bring the design to **3NF**.
6. Give the **degree** and the **cardinality** of the original spreadsheet table.

## PART 2: Keys and constraints (Ch1 + Ch2)

7. For the `member` table, list the **candidate keys**. Which one do you choose as **primary key** and why? What do the others become (alternate keys), and which SQL constraint enforces them?
8. For each case below, name the **integrity constraint** that is violated (key / domain / referential integrity):
   - a) Inserting a member with `member_id = 'M1'` when M1 already exists.
   - b) Inserting `'sixty'` into `fee_paid DECIMAL(6,2)`.
   - c) Inserting an enrollment for member `'M99'`, who does not exist.
   - d) Inserting a class with `class_id = NULL`.
   - e) Inserting a coach with `salary = 'high'`.
9. Which constraint would you use for each rule? (`NOT NULL` / `UNIQUE` / `CHECK` / `DEFAULT` / `PRIMARY KEY` / `FOREIGN KEY`)
   - Room capacity must be between 5 and 50.
   - Two members can't share an email.
   - A member's last name is mandatory.
   - The enrollment date is today's date if none is given.
   - A locker size can only be 'S', 'M' or 'L'.

## PART 3: ERD (Ch1)

10. Draw the full **ERD** in crow's foot notation (two-compartment boxes, PK/FK marked, data types written):
    - `coach`, `room`, `class`, `member`, `enrollment`, `locker`
    - Write the cardinality on each line (1:1, 1:N, and the M:N **resolved** with a junction table).
11. Answer: which relationship is 1:1? Which are 1:N? Which was M:N, and **which table resolves it**? Its primary key is __________ (what kind of key?).
12. Rule check: on which side of each 1:N line did you put the **foreign key**? Explain the rule in one sentence.
13. For the 1:1 member-locker relationship, where do you put the FK, and **which extra constraint** guarantees it stays 1:1 and doesn't turn into 1:N?

## PART 4: Physical schema: CREATE, data types, constraints (Ch1 + Ch2)

14. `CREATE DATABASE carthage_fitness;` then select it. Show all databases.
15. Create **all 6 tables** with suitable data types (`INT`, `VARCHAR(n)`, `DECIMAL(p,s)`, `DATE`, `CHAR`…) and **every** constraint from Part 2:
    - PRIMARY KEY on every table (a **composite PK** for `enrollment`)
    - FOREIGN KEYs with `REFERENCES`
    - `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`
    - Use `AUTO_INCREMENT` for `locker_id`.
    - ⚠️ Think about the **order** you create the tables in. Why does it matter?
16. Display the structure of `enrollment` (`DESCRIBE` / `SHOW COLUMNS`).

## PART 5: Insert the data (Ch1: INSERT, Ch2)

17. Insert this data (write the INSERT statements yourself; use multi-row INSERT at least once):

**coach**

| coach_id | full_name | speciality | salary |
|---|---|---|---|
| C1 | Amine Bensalem | Fitness | 2200 |
| C2 | Ines Trabelsi | Yoga | 1800 |
| C3 | Karim Jlassi | Boxing | 2500 |
| C4 | Rania Gharbi | Swimming | 2000 |

**room**

| room_code | floor | capacity |
|---|---|---|
| R1 | 1 | 20 |
| R2 | 2 | 15 |
| R3 | 0 | 10 |

**class**

| class_id | class_name | price | coach_id | room_code |
|---|---|---|---|---|
| CL1 | Crossfit | 60 | C1 | R1 |
| CL2 | Yoga Morning | 50 | C2 | R2 |
| CL3 | Boxing Basics | 70 | C3 | R3 |
| CL4 | Yoga Evening | 45 | C2 | R2 |
| CL5 | Cardio | 40 | C1 | R1 |

**member**

| member_id | first_name | last_name | birth_date | email | phone |
|---|---|---|---|---|---|
| M1 | Sarra | Mansour | 2001-03-12 | sarra.m@mail.tn | 22145678 |
| M2 | Youssef | Ayari | 1998-07-30 | youssef.a@mail.tn | 55321987 |
| M3 | Lina | Haddad | 2004-11-02 | lina.h@mail.tn | NULL |
| M4 | Omar | Khelifi | 1995-01-25 | omar.k@mail.tn | 98765432 |
| M5 | Aya | Ben Ali | 2003-05-18 | aya.b@mail.tn | NULL |
| M6 | Ahmed | Zribi | 2000-09-09 | ahmed.z@mail.tn | 20111222 |

**enrollment**

| member_id | class_id | enroll_date | fee_paid |
|---|---|---|---|
| M1 | CL1 | 2026-09-01 | 60 |
| M1 | CL2 | 2026-09-03 | 50 |
| M2 | CL1 | 2026-09-02 | 60 |
| M2 | CL3 | 2026-09-10 | 70 |
| M3 | CL2 | 2026-09-05 | 50 |
| M3 | CL4 | 2026-10-01 | 45 |
| M4 | CL3 | 2026-09-15 | 70 |
| M4 | CL1 | 2026-10-02 | 55 |
| M6 | CL5 | 2026-10-05 | 40 |
| M1 | CL5 | 2026-10-06 | 40 |

**locker** (let AUTO_INCREMENT generate the id: don't insert it)

| size | member_id |
|---|---|
| M | M1 |
| L | M2 |
| S | M3 |
| L | M4 |
| M | M6 |

18. **Test your constraints.** Run each of these, write down the error you get, and say which constraint caught it:
    - `INSERT INTO enrollment VALUES ('M99','CL1','2026-10-10',60);`
    - `INSERT INTO room VALUES ('R9', 3, 100);`
    - `INSERT INTO member VALUES ('M7','Test','User','2000-01-01','sarra.m@mail.tn',NULL);`
    - `INSERT INTO locker (size, member_id) VALUES ('M','M1');`
    - `DELETE FROM coach WHERE coach_id = 'C1';` ← why is this refused?

## PART 6: ALTER TABLE (Ch2)

19. Add a column `join_date DATE` to `member`.
20. Change the `phone` column's type to `VARCHAR(15)` (use **MODIFY**).
21. Rename the column `speciality` to `specialty` in `coach` (use **CHANGE**). What is the difference between MODIFY and CHANGE?
22. Drop the column `join_date`.
23. Rename the table `room` to `gym_room`, then rename it back.
24. Suppose you had forgotten the FK from `class` to `coach`. Write the `ALTER TABLE … ADD FOREIGN KEY …` statement.

## PART 7: Operators and filtering (Ch1 operators + Ch2 filtering)

Write one query for each:

25. Every coach's name with their **yearly salary** (`salary * 12`), aliased `yearly_salary`.
26. Every coach's salary after a **10% raise**.
27. Every enrollment with the **discount** given (`class.price - fee_paid`). (You need a join or a subquery, so come back to this after Part 8 if you're stuck.)
28. Coaches whose salary is **not equal** to 2000 (write it two ways).
29. Members born **after** 2000-01-01.
30. Classes whose price is **between** 45 and 60.
31. Coaches whose specialty is **in** ('Yoga', 'Boxing').
32. Members whose last name **starts with** 'B'.
33. Members whose first name **ends with** 'a'.
34. Members whose first name has **'a' as the second letter**.
35. Members whose email **contains** 'h'.
36. Members whose first name **starts with 'S' and is at least 5 characters long**.
37. Members **without** a phone number. ⚠️ Why does `WHERE phone = NULL` return nothing?
38. Classes that are **NOT** in room R1.
39. Enrollments where the fee was **≥ 50 AND** the date is in **October 2026**.
40. Enrollments in CL1 **OR** CL3, sorted by fee **descending**, then by date ascending.
41. Enrollments whose `fee_paid` is a **multiple of 20** (use the modulus operator `%`).
42. Display `CONCAT(first_name, ' ', last_name)` as **"Full Name"** (an alias with a space: how do you write it?).

## PART 8: Joins and UNION (Ch2)

43. **INNER JOIN**: each class name with its coach's full name.
44. **3-table join**: each member's full name, the class name and the fee paid.
45. **4-table join**: each member's full name, class name, coach name and room floor.
46. **LEFT JOIN**: **all** members and their class ids, **including members who enrolled in nothing**. Who shows up with NULL?
47. **RIGHT JOIN**: all coaches and the classes they teach, **including coaches who teach nothing**. Who shows up with NULL?
48. Rewrite query 43 using the **comma syntax with table aliases** (`FROM class AS c, coach AS co WHERE …`).
49. The member's full name and locker size (which kind of relationship is this join following?).
50a. **SELF JOIN**: pairs of classes that take place **in the same room** (class1 name, class2 name, room). Avoid pairing a class with itself and avoid duplicate pairs (hint: `c1.class_id < c2.class_id`).
50b. **FULL OUTER JOIN**: all members and all lockers, matched or not. ⚠️ MySQL does **not** support `FULL OUTER JOIN`: write the standard syntax from the course, then the MySQL version (`LEFT JOIN … UNION … RIGHT JOIN`).
50c. **UNION**: one single list of **all people names** in the club (coaches' full names + members' full names). What's the difference between `UNION` and `UNION ALL`?

## PART 9: Aggregates, GROUP BY, HAVING (Ch2)

50d. Knowledge check: name the **4 join types supported in MySQL** according to the course, and say which join returns **only matching rows**.

51. How many members are there in total? What is the average coach salary?
52. Number of enrollments **per class** (show the class name), sorted by count descending.
53. Total money collected **per class**.
54. Total money paid **per member** (full name), but only members who paid **more than 100** → `HAVING`.
55. For each coach: the number of classes they teach. Use a **LEFT JOIN** so coaches with 0 classes appear with 0. (Hint: `COUNT(column)` vs `COUNT(*)`.)
56. Number of enrollments **per enroll_date**, only for dates **between** 2026-09-01 and 2026-09-30.
57. Rooms that host **at least 2 classes**.
57b. Knowledge check: which of these GROUP BY rules are **true**? (a) GROUP BY goes before WHERE; (b) the GROUP BY columns must also appear in SELECT; (c) the statement begins with SELECT; (d) an aggregate function must be followed by the column name in parentheses.
58. Explain: why does `WHERE COUNT(*) > 2` fail but `HAVING COUNT(*) > 2` works? In what order does MySQL run WHERE, GROUP BY, HAVING, ORDER BY?

## PART 10: Subqueries, EXISTS, ANY, ALL (Ch2)

58b. Name the **5 types of subqueries** from the course (single row, …) and the **3 clauses** a subquery can be placed in. Which type is a subquery that uses a column of the outer query?
58c. **Subquery in SELECT**: each class name with the number of members enrolled, computed with a subquery in the SELECT list: `(SELECT COUNT(*) FROM enrollment e WHERE e.class_id = c.class_id)`. What type of subquery is this?
59. **EXISTS**: coaches who teach at least one class.
60. **NOT EXISTS**: members who are enrolled in no class.
61. **ANY**: classes whose price is greater than **any** price paid by M3.
61b. **SOME**: same as 61 but written with `SOME`. Are ANY and SOME different?
62. **ALL**: the class(es) whose price is ≥ **all** other class prices (the most expensive).
63. **Subquery in WHERE**: members who paid more than the **average** fee_paid.
63b. **Nested subquery**: names of members enrolled in a class taught by 'Karim Jlassi' (subquery inside a subquery, **no join**).
64. **Subquery in FROM** (derived table, needs an alias!): for each member compute their number of enrollments, then from that result show `MAX`, `MIN` and `FLOOR(AVG(...))` of those numbers.
65. **INSERT … SELECT**: create a table `enrollment_archive` with the same structure as `enrollment`, then copy into it every enrollment from **September 2026**.
66. **UPDATE with subquery**: raise by 5% the salary of every coach who teaches **2 or more** classes.
67. **DELETE with subquery**: delete from `enrollment_archive` every row whose class is taught by coach C3.
68. **REPLACE INTO**: run `REPLACE INTO room VALUES ('R3', 0, 12);` then `REPLACE INTO room VALUES ('R4', 1, 25);`. Explain what happened in each case (when does REPLACE **update** and when does it **insert**?). Then do the same thing with the **second syntax** (like UPDATE): `REPLACE INTO room SET room_code='R4', floor=2, capacity=30;`
69. **UPDATE**: Lina changed her phone to `29876543`. **DELETE**: remove enrollment (M6, CL5). ⚠️ What happens if you forget the WHERE clause?

## PART 11: Views (Ch2)

70. Create a view `v_member_classes` showing member full name, class name, coach name, fee paid.
71. Query the view: only the rows for the coach "Ines Trabelsi".
72. Create a view `v_coach_public` with **only** `coach_id`, `full_name`, `specialty` (no salary). Which benefit of views does this illustrate?
73. Create `v_enrollment_simple` from `enrollment` (member_id, class_id, fee_paid) and **update through the view**: set the fee of (M4, CL1) to 60. Check the base table: did it change? Why?
74. Name the **3 benefits of views** from the course. Does a view store data?

## PART 12: Quick theory (knowledge checks style)

96. Relation, tuple, attribute, domain: define each in one line.
97. What does "the relational model is built on 3 concepts" refer to?
98. Logical schema vs physical schema: what is the difference?
99. Name 4 schema objects besides tables.
99b. Give the **3 uses of aliases** from the course knowledge check.
100. A "contact" column accepts only digits and anything else raises an error. Which constraint type is this? And "each field must contain at least one value": which SQL constraint?


---

# ⛔ OUT OF DS SCOPE: do these only after the exam (or for the final)

## ⛔ PART 13: Functions (after views: NOT in DS)

75. Numeric: on `salary / 7`, show `CEIL`, `FLOOR`, `ROUND(…, 2)`. And `MOD(17, 5)`.
76. `FORMAT(salary * 12, 2)` for each coach. What type does FORMAT return?
77. String: `UPPER(last_name)`, `LOWER(first_name)`, `CHAR_LENGTH(first_name)`, `LEFT(first_name, 3)`.
78. `CONCAT_WS(' - ', member_id, first_name, last_name)`.
79. Initials: e.g. "S.M." for Sarra Mansour (combine CONCAT + LEFT).
80. Dates: for each member show `YEAR(birth_date)`, `MONTHNAME(birth_date)`, `DAYNAME(birth_date)`.
81. Each member's **age in years** (use `CURDATE()` and either `DATEDIFF` or `YEAR`/`TIMESTAMPDIFF`).
82. Each enrollment's date + 30 days with `ADDDATE` (**both** syntaxes: `INTERVAL 30 DAY` and `, 30`).
83. The `QUARTER()` of each enrollment date.
84. Number of days between each enrollment and 2026-12-31 (`DATEDIFF`).
85. `IFNULL(phone, 'no phone')` for each member.
86. `COALESCE(phone, email, 'unknown')`: what does it return for M3?
87. `NULLIF(price, 50)` for each class. For which classes does it return NULL?
88. `IF(fee_paid < price, 'discount', 'full price')` for each enrollment (join needed).
89. `CASE`: label each member by age: `< 23` → 'Junior', `23–29` → 'Adult', `≥ 30` → 'Senior'.

## ⛔ PART 14: Stored procedures (after views: NOT in DS)

90. `GetAllCoaches()`: no parameter, returns all coaches. Call it.
91. `GetClassesCheaperThan(maxPrice DECIMAL(6,2))`: one parameter. Call it with 50.
92. `GetMembersOfClass(cid VARCHAR(5))`: returns the full names of members enrolled in a class. Call it for 'CL1'.
93. `GetEnrollmentsBetween(d1 DATE, d2 DATE)`: two parameters. Call it for October 2026.
94. Drop the procedure `GetAllCoaches`.
95. Give 3 reasons to use stored procedures (from the course).

---

✅ When you finish (or get stuck), send me your answers **part by part**. I'll correct each one and explain what you missed.
