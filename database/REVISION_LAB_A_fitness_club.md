# Revision Lab A: "Carthage Fitness Club"

> **DS scope: from SQL operators to Views.** Answer on **paper**, like in the DS.
> No syntax is given in the questions. You decide which statement, clause or operator to use.
> Don't look at your notes while answering. Afterwards, send me your answers part by part and I'll correct them.

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

## PART 1: Relational model and normalization

1. List **3 problems** with this spreadsheet.
2. Is it in 1NF? Justify. Transform it into **1NF** and show the resulting table(s).
3. Which **composite key** does your 1NF table need? List every **partial dependency**.
4. Bring the design to **2NF**. Show the tables with their keys.
5. Find the **transitive dependency** in the data and bring the design to **3NF**.
6. Give the **degree** and the **cardinality** of the original spreadsheet.

## PART 2: Keys and constraints

7. List the **candidate keys** of the member table. Which one do you choose as primary key and why? What do the others become, and how do you guarantee them in SQL?
8. For each situation, would the DBMS accept it? If not, which **integrity constraint** is violated?
   - a) A new member with the ID of an existing member.
   - b) The text "sixty" stored as a fee paid.
   - c) An enrollment for a member ID that doesn't exist.
   - d) A class without a class ID.
   - e) A coach whose salary is the word "high".
   - f) Deleting coach C1 while classes still refer to him.
   - g) A second locker for member M1.
9. Which SQL constraint enforces each rule?
   - Room capacity must be between 5 and 50.
   - Two members can't share an email.
   - A member's last name is mandatory.
   - The enrollment date is today's date if none is given.
   - A locker size can only be S, M or L.
   - The locker number is generated automatically.

## PART 3: ERD

10. Draw the full **ERD** in crow's foot notation: every entity with its attributes and data types, PKs and FKs marked, and the cardinality written on every relationship.
11. Which relationship is 1:1? Which are 1:N? Which was M:N, how did you resolve it, and what kind of primary key does the new table have?
12. On which side of a 1:N relationship does the foreign key go? Why?
13. For the member-locker relationship: where do you put the FK, and what stops it from becoming 1:N?

## PART 4: Physical schema

14. Write the statement that creates the database `carthage_fitness`.
15. Write the CREATE statements for **all 6 tables**, with suitable data types and **every** constraint from Part 2. In what order must you create them, and why?

## PART 5: Inserting data

Here is the data to store:

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

**locker** (the number is generated automatically)

| size | member_id |
|---|---|
| M | M1 |
| L | M2 |
| S | M3 |
| L | M4 |
| M | M6 |

16. Insert all the **coaches** in a single statement.
17. Insert member M3 (careful with the missing phone).
18. Insert the lockers without giving the locker number.

## PART 6: Modifying the structure

19. Add a join date to the member table.
20. Change the type of the phone column so it can hold 15 characters.
21. Rename the column speciality to specialty, keeping its type. What's the difference between the two ways of altering a column you used in 20 and 21?
22. Remove the join date column.
23. Rename the room table to gym_room.
24. The foreign key from class to coach was forgotten when the table was created. Add it.

## PART 7: Operators and filtering

Write the SQL query for each request.

25. Each coach's name with their yearly salary, under the heading yearly_salary.
26. Each coach's salary after a 10% raise.
27. Coaches whose salary is different from 2000 (write it two ways).
28. Members born after 1 January 2000.
29. Classes whose price is between 45 and 60.
30. Coaches whose speciality is Yoga or Boxing (write it two ways).
31. Members whose last name starts with B.
32. Members whose first name ends with a.
33. Members whose first name has a as the second letter.
34. Members whose email contains h.
35. Members whose first name starts with S and has at least 5 letters.
36. Members who never gave a phone number. Explain why comparing the phone with NULL using "=" returns nothing.
37. Classes that are not in room R1.
38. Enrollments with a fee of at least 50 made in October 2026.
39. Enrollments in CL1 or CL3, from the highest fee to the lowest, then by date.
40. Enrollments whose fee is a multiple of 20.
41. Each member's first and last name joined into one column with the heading "Full Name".
42. Every distinct fee amount that has been paid.

## PART 8: Joins and UNION

43. Each class name with the full name of its coach.
44. Each member's full name, the name of each class they're in, and the fee paid.
45. Each member's full name, class name, coach name and the floor of the room.
46. **All** members with the IDs of their classes, including members who enrolled in nothing. Who appears with empty values?
47. **All** coaches with the classes they teach, including coaches who teach nothing. Write it with the opposite join from question 46.
48. Rewrite question 43 without the JOIN keyword, using table aliases.
49. Each member's full name with their locker size.
50. Pairs of classes that take place in the same room (no class paired with itself, no pair listed twice).
51. All members and all lockers, whether they match or not.
52. One single list of all people's names in the club (coaches and members), without duplicates. What would change if you wanted to keep duplicates?

## PART 9: Aggregates and grouping

53. The total number of members, and the average coach salary.
54. The number of enrollments per class (show the class name), from the most popular class down.
55. The total money collected per class.
56. The total paid per member (full name), only for members who paid more than 100.
57. The number of classes each coach teaches, with coaches who teach none showing 0.
58. The number of enrollments per enrollment date, for September 2026 only.
59. Rooms that host at least 2 classes.
60. Why can't a condition on a count go in the same place as a condition on a column? In what order are these clauses processed: the row filter, the grouping, the group filter, and the sorting?

## PART 10: Subqueries

61. Coaches who teach at least one class (use a subquery, no join).
62. Members enrolled in no class (use a subquery, no join).
63. Classes whose price is higher than at least one of the fees paid by M3 (write it two ways).
64. The most expensive class(es), without using MAX.
65. Members who paid more than the average fee.
66. Names of members enrolled in a class taught by Karim Jlassi, using subqueries only (no join).
67. Each class name with its number of enrolled members, computed by a subquery placed in the column list.
68. For each member, count their enrollments. Then, from that result, give the highest, lowest and average (rounded down) number of enrollments.
69. An archive table with the same structure as enrollment exists. Copy into it every enrollment from September 2026.
70. Raise by 5% the salary of every coach who teaches 2 or more classes.
71. Delete from the archive every row whose class is taught by coach C3.
72. Write a statement that stores room R3 with capacity 12: it must replace the existing R3. Then store room R4 (floor 1, capacity 25), which doesn't exist yet. Explain what the DBMS does in each case. Write the R4 statement in **both** syntaxes from the course.
73. Lina changed her phone to 29876543: update it. Then remove the enrollment of M6 in CL5. What happens if you forget the condition?
74. For each subquery you wrote in 61–71, say its type (from the 5 types in the course).

## PART 11: Views

75. A view showing each member's full name, class name, coach name and fee paid.
76. Using that view: only the rows of the coach Ines Trabelsi.
77. A view showing coaches **without** their salary. Which benefit of views does this illustrate?
78. A view on enrollment showing only member, class and fee. Through this view, change the fee of (M4, CL1) to 60. Does the base table change? Why?
79. Name the 3 benefits of views. Does a view store data?

## PART 12: Theory (DS style)

80. Define relation, tuple, attribute and domain in one line each.
81. What are the 3 concepts the relational model is built on?
82. What's the difference between the logical and the physical schema?
83. Name 4 schema objects other than tables.
84. A "contact" column accepts only digits; anything else gives an error. Which constraint type is this? And "every field must contain a value": which SQL constraint?
85. Give the 3 uses of aliases.
86. Name the join types in the course. Which one returns only matching rows?
87. True or false? (a) GROUP BY comes before WHERE. (b) The grouped columns should also appear in SELECT. (c) The statement begins with SELECT. (d) An aggregate function is followed by the column name in parentheses.
88. Name the 5 types of subqueries and the clauses a subquery can be placed in.
89. Difference between: deleting rows / dropping a column / dropping a table.

---

✅ Send me your answers part by part (a photo of your ERD and your papers is fine). I'll correct everything.
