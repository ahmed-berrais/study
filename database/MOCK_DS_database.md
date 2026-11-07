# Mock DS: Database Engineering

**Duration:** 2 hours · **Documents:** not allowed · **Total:** 20 points
**Scope:** Chapter I (SQL operators, relational model, keys, constraints, ERD, schema, normalization) + Chapter II (filtering, joins, grouping, updates, ALTER, subqueries, views)
**Write all SQL statements on paper (MySQL syntax).**

---

## Exercise 1: Course questions (3 points)

**A. Choose the correct answer(s).**

1. You're creating a table for an online store. The column "Contact details" stores phone numbers using numeric values only. Any attempt to insert other values gives an error. This column is an example of:
   - a) Domain constraint
   - b) Key constraint
   - c) Referential integrity constraint
2. You need to make sure each field in a column contains a value. Which constraint do you use?
   - a) FOREIGN KEY
   - b) CHECK
   - c) UNIQUE
   - d) NOT NULL
3. You're copying data between tables. Which syntax item identifies the name of the existing table you copy from?
   - a) FROM clause
   - b) SELECT command
   - c) TABLE keyword
4. Which join returns only the records that have matching values in both tables?
   - a) RIGHT JOIN
   - b) LEFT JOIN
   - c) INNER JOIN
5. Which of these are correct rules for using GROUP BY? (several answers)
   - a) Place the GROUP BY clause before the WHERE clause.
   - b) Make sure the GROUP BY columns are also present in the SELECT.
   - c) Begin the statement with a SELECT clause.
   - d) An aggregate function must be followed by the name of the column in parentheses.

**B. Answer briefly.**

6. Define: relation, tuple, attribute, domain.
7. What is the difference between the **degree** and the **cardinality** of a table?
8. Name the three relational integrity constraints.
9. Give the three aims of normalization.
10. What does the `%` operator return? Give an example.
11. How is a many-to-many relationship handled in a relational database?
12. Give the three benefits of using views.

---

## Exercise 2: Data types, constraints and keys (3 points)

Mrs. Amira Ben Salah owns a small pharmacy named **"Pharma Amira"** in Sousse. She wants a database called `pharma_amira`.

**Task 1.** She wants to store information about medicines:

| Med ID | Medicine name | Price | Expiry date | Quantity |
|---|---|---|---|---|
| 1 | Doliprane 1000mg | 8.750 | 2027-03-01 | 120 |
| 2 | Augmentin 1g | 12.500 | 2026-12-15 | 40 |
| 3 | Smecta | 4.300 | 2028-01-20 | 75 |

1. Write the SQL statement that creates the database and selects it.
2. Choose a suitable data type for each column and justify your choice for Price and Expiry date.
3. Write the complete SQL statement that creates the `medicines` table, with Med ID as primary key.

**Task 2.** She wants to store customer information:

- The **card number** is always **8 characters** long and contains alphanumeric values (e.g. CARD0001).
- The **full name** varies in length, up to a maximum of 100 characters. It is mandatory.
- The **email** is at most 255 characters.
- Most customers live in **Sousse**, so the city should be filled in automatically with "Sousse" if no value is given.

4. Write the complete SQL statement that creates the `customers` table with the relevant data types and constraints.

**Task 3.** Review the following supplier table:

| Supplier ID | Tax number | Supplier name | Phone |
|---|---|---|---|
| SP01 | 1234567A | MediPlus | 73111222 |
| SP02 | 7654321B | PharmaDis | 73333444 |
| SP03 | 1122334C | MediPlus | 73555666 |

5. Identify the candidate keys. Is "Supplier name" a candidate key? Justify.
6. Which candidate key is the best choice for the primary key? What do we call the others?
7. Each supplier provides many medicines, and each medicine comes from one supplier. What type of relationship is this? In which table do you put the foreign key?
8. The `medicines` table already exists. Write the statements that add a `SupplierID` column to it and make it a foreign key that references the `suppliers` table.

---

## Exercise 3: Database schema and ERD (3 points)

An online learning platform, **"EduTN"**, wants to design its database. The main tables are:

| Table | Description |
|---|---|
| Teachers | Teacher ID, full name, email, speciality |
| Categories | Category ID, label |
| Courses | Course ID, title, price, number of hours |
| Students | Student ID, full name, birth date, email |
| Student_cards | Card number, issue date |
| Enrollments | Enrollment date, final grade |

The relationships are:
- Each teacher teaches one or many courses. Each course is taught by one teacher.
- Each course belongs to one category. A category contains many courses.
- A student can enroll in many courses, and a course can have many students.
- Each student has one and only one student card. Each card belongs to one student.

1. Give the type of each relationship (1:1, 1:N, M:N).
2. Explain how the relationship between Students and Courses is represented in the database.
3. Draw the entity relationship diagram (ERD) of the 6 tables: attributes, data types, primary keys (PK), foreign keys (FK) and cardinalities.
4. Write the SQL statement that creates the `enrollments` table.

---

## Exercise 4: Normalization (3 points)

The driving school **"Auto-école Ennour"** keeps its data in this table:

| Instructor ID | Instructor name | Agency No | Agency city | Governorate | Student ID | Student name | Lesson ID | Lesson price |
|---|---|---|---|---|---|---|---|---|
| I1 | Sami Trabelsi | 1 | La Marsa | Tunis | S1, S2, S3 | Rim, Hamza, Nada | L1, L1, L2 | 40, 40, 45 |
| I1 | Sami Trabelsi | 2 | Sousse | Sousse | S4, S5 | Mehdi, Lotfi | L1, L3 | 40, 50 |
| I2 | Amel Ksouri | 2 | Sousse | Sousse | S5, S6 | Lotfi, Wafa | L2, L1 | 45, 40 |
| I2 | Amel Ksouri | 3 | Hammamet | Nabeul | S1, S7 | Rim, Ines | L3, L2 | 50, 45 |

1. Why is this table in an unnormalized form? Give two reasons.
2. Apply the **first normal form** (1NF). Give the resulting tables and their primary keys.
3. Define a **partial dependency**. Find the partial dependencies in your student table and apply the **second normal form** (2NF).
4. Define a **transitive dependency**. Find the one in the agency data and apply the **third normal form** (3NF).
5. Write the SQL statement that creates the table linking students and lessons.

---

## Exercise 5: Inserting, deleting and filtering data (3 points)

The hotel **"Dar Djerba"** has eight employees in four departments. Here is the `employees` table:

| EmployeeID | EmployeeName | Department | AnnualSalary |
|---|---|---|---|
| 1 | Sami Ferchichi | Marketing | 52000 |
| 2 | Hela Mabrouk | Finance | 48000 |
| 3 | Slim Gharbi | Reception | 30000 |
| 4 | Rym Toumi | Legal | 75000 |
| 5 | Ali Saadi | Marketing | 45000 |
| 6 | Sonia Ben Amor | Finance | 61000 |
| 7 | Nabil Hamdi | Reception | 28000 |
| 8 | Sara Jaziri | Legal | 39000 |

Write the SQL statement for each request.

1. Create the `employees` table.
2. Insert the first two records.
3. Display all the data in the table, sorted in alphabetical order of employee name.
4. Display only the name and the monthly salary of each employee (call the column `MonthlySalary`).
5. Use the AND operator to find employees in the Marketing department who earn $50,000 or more.
6. Use the NOT operator to find employees who do not earn over $50,000.
7. Use the IN operator to find Marketing, Finance and Legal employees whose annual salary is below $50,000.
8. Use the BETWEEN operator to find employees who earn between $30,000 and $50,000.
9. Use the LIKE operator to find employees whose names start with "S" and are at least 4 characters long.
10. Delete the employee with ID 7.
11. Give the result of this query on the **original** table:
    ```sql
    SELECT EmployeeName FROM employees
    WHERE AnnualSalary % 2000 = 0 AND Department <> 'Legal';
    ```

---

## Exercise 6: Joining and grouping data (3 points)

**Part A.** The café **"Sidi Bou Said"** stores its customers and bookings:

**Customers**

| CustomerID | FullName | PhoneNumber |
|---|---|---|
| 1 | Yassine Amri | 22111333 |
| 2 | Mouna Kefi | 55222444 |
| 3 | Fares Belhaj | 98333555 |
| 4 | Olfa Sassi | 20444666 |
| 5 | Tarek Mzali | 29555777 |

**Bookings**

| BookingID | BookingDate | TableNumber | NumberOfGuests | CustomerID |
|---|---|---|---|---|
| 10 | 2026-06-03 | 5 | 2 | 1 |
| 11 | 2026-06-03 | 2 | 4 | 3 |
| 12 | 2026-06-10 | 7 | 3 | 1 |
| 13 | 2026-06-15 | 1 | 6 | 4 |
| 14 | 2026-07-01 | 5 | 2 | 1 |

1. Write an INNER JOIN statement that shows the full name and phone number of each customer with their booking date and number of guests.
2. Write a LEFT JOIN statement that shows every customer ID with the related booking ID, **including customers who haven't booked yet**. Which customers appear with NULL?
3. Rewrite question 2 using a RIGHT JOIN.

**Part B.** The garden shop **"Jnina"** has this `orders` table:

| OrderID | Department | OrderDate | OrderQty | OrderTotal |
|---|---|---|---|---|
| 1 | Lawn Care | 2022-05-05 | 12 | 500 |
| 2 | Decking | 2022-05-22 | 150 | 1450 |
| 3 | Compost and Stones | 2022-05-27 | 20 | 780 |
| 4 | Trees and Shrubs | 2022-06-01 | 15 | 400 |
| 5 | Garden Decor | 2022-06-10 | 2 | 1250 |
| 6 | Lawn Care | 2022-06-10 | 10 | 400 |
| 7 | Decking | 2022-06-25 | 100 | 1400 |
| 8 | Trees and Shrubs | 2022-07-02 | 5 | 300 |
| 9 | Garden Decor | 2022-07-02 | 4 | 900 |
| 10 | Lawn Care | 2022-07-04 | 30 | 1100 |

4. Retrieve the number of orders placed on each day.
5. Retrieve the total order quantity of each department.
6. Retrieve the number of orders placed on each day between 1 June 2022 and 30 June 2022.
7. Retrieve the departments whose total order amount is greater than 1500. Give the result.

---

## Exercise 7: Updating and managing the database (2 points)

Use the `employees` table from Exercise 5. **Each question is independent and uses the original table.**

1. Add a column `Email` (maximum 255 characters) to the table.
2. Increase the salary of every Reception employee by 5%.
3. Write a query that shows the employees who earn more than the average salary. Give the result.
4. Explain what this statement does if the employee with ID 3 already exists, and if they don't exist:
   ```sql
   REPLACE INTO employees (EmployeeID, EmployeeName, Department, AnnualSalary)
   VALUES (3, 'Slim Gharbi', 'Reception', 32000);
   ```
5. Create a view `EmployeesPublic` that shows the employee ID, name and department only. Which benefit of views does this illustrate?
6. Rename the column `AnnualSalary` to `Salary`, keeping the same data type.

---

*Good luck!*
