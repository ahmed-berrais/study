# Rundown before the mock DS: Joins, GROUP BY/HAVING, subqueries, UPDATE, ALTER, views

Every example below uses these two small tables. Learn the results by heart: the DS asks for results too.

**Customers**

| CustomerID | FullName |
|---|---|
| 1 | Amal |
| 2 | Bilel |
| 3 | Chaima |

**Bookings**

| BookingID | BookingDate | Guests | CustomerID |
|---|---|---|---|
| 10 | 2026-06-01 | 2 | 1 |
| 11 | 2026-06-01 | 4 | 1 |
| 12 | 2026-06-05 | 3 | 2 |
| 13 | 2026-06-09 | 5 | NULL |

Chaima (3) has **no booking**. Booking 13 has **no customer**.

---

## 1. Filtering (WHERE)

| Need | Write |
|---|---|
| Both conditions true | `WHERE a AND b` |
| At least one true | `WHERE a OR b` |
| Opposite | `WHERE NOT Country = 'Mexico'` |
| In a list | `WHERE Country IN ('Germany','UK')` (= several ORs) |
| In a range | `WHERE Price BETWEEN 10 AND 20` (**includes** 10 and 20) |
| Text pattern | `WHERE Name LIKE 'a%'` |
| Missing value | `WHERE Phone IS NULL` (⚠️ never `= NULL`) |
| Not equal | `<>` or `!=` (both are correct) |

**LIKE patterns:** `%` = any number of characters (even 0), `_` = exactly 1 character.

| Pattern | Meaning |
|---|---|
| `'a%'` | starts with a |
| `'%i'` | ends with i |
| `'%li%'` | contains "li" |
| `'_a%'` | a is the 2nd letter |
| `'a___%'` | starts with a, **at least 4** characters |
| `'a%i'` | starts with a and ends with i |

**Sorting:** `ORDER BY col ASC` (the default) or `DESC`. With several columns, `ORDER BY Dept, Salary DESC` sorts by Dept first, then by Salary within each Dept.

**Arithmetic in SELECT:** `SELECT Salary / 12 AS MonthlySalary`. `%` gives the remainder: `x % 2 = 0` means even.

**Aliases:**
- Column: `SELECT FullName AS Name`.
- With a space: `AS "Full Name"`.
- Table: `FROM Customers AS c`.
- Concatenate two columns into one: `CONCAT(First, ' ', Last) AS FullName`.
- The 3 uses of aliases: concatenate output into one column, create distinct names when working with several tables, rename a long or technical name.

---

## 2. JOINS

A join links records of several tables using a **common column** (PK = FK).

**General form**
```sql
SELECT T1.col, T2.col
FROM T1  <TYPE> JOIN  T2
ON T1.common_col = T2.common_col;
```

### INNER JOIN: only the rows that match in both tables
```sql
SELECT Customers.FullName, Bookings.BookingID
FROM Customers INNER JOIN Bookings
ON Customers.CustomerID = Bookings.CustomerID;
```
| FullName | BookingID |
|---|---|
| Amal | 10 |
| Amal | 11 |
| Bilel | 12 |

Chaima and booking 13 are **missing**.

### LEFT JOIN: ALL rows of the LEFT table, plus the matches (NULL if none)
```sql
SELECT Customers.FullName, Bookings.BookingID
FROM Customers LEFT JOIN Bookings
ON Customers.CustomerID = Bookings.CustomerID;
```
| FullName | BookingID |
|---|---|
| Amal | 10 |
| Amal | 11 |
| Bilel | 12 |
| **Chaima** | **NULL** |

👉 Key phrase in the DS: "**including customers who haven't made any booking**" means LEFT JOIN with Customers on the left.

### RIGHT JOIN: ALL rows of the RIGHT table, plus the matches
```sql
SELECT Customers.FullName, Bookings.BookingID
FROM Customers RIGHT JOIN Bookings
ON Customers.CustomerID = Bookings.CustomerID;
```
| FullName | BookingID |
|---|---|
| Amal | 10 |
| Amal | 11 |
| Bilel | 12 |
| **NULL** | **13** |

💡 `A LEFT JOIN B` gives the same result as `B RIGHT JOIN A`. To turn a LEFT into a RIGHT, **swap the tables**.

### FULL OUTER JOIN (= FULL JOIN): all rows from both sides
```sql
SELECT ... FROM Customers FULL OUTER JOIN Bookings
ON Customers.CustomerID = Bookings.CustomerID;
```
Result: the 3 matches **+ Chaima/NULL + NULL/13**.
(MySQL doesn't run it. The equivalent is `LEFT JOIN … UNION … RIGHT JOIN`.)

### SELF JOIN: a table joined with itself (you need 2 aliases)
```sql
SELECT a.FullName, b.FullName
FROM Customers a, Customers b
WHERE a.City = b.City AND a.CustomerID < b.CustomerID;
```
(`<` avoids pairing a row with itself and avoids duplicate pairs.)

### Join without the JOIN keyword (comma + WHERE + aliases)
```sql
SELECT c.FullName, b.BookingID
FROM Customers AS c, Bookings AS b
WHERE c.CustomerID = b.CustomerID;     -- same result as INNER JOIN
```

### 3 tables
```sql
SELECT ... FROM A
INNER JOIN B ON A.id = B.a_id
INNER JOIN C ON B.id = C.b_id;
```

**Course:** MySQL supports 4 types: **INNER, LEFT, RIGHT, SELF**.

---

## 3. UNION

UNION combines the results of 2 SELECTs. Both must have the **same number of columns**, similar data types, and the columns in the same order.
```sql
SELECT City FROM Customers
UNION                -- removes duplicates
SELECT City FROM Suppliers;
```
`UNION ALL` keeps the duplicates.

---

## 4. Aggregates, GROUP BY, HAVING

**Aggregate functions:** `COUNT()`, `SUM()`, `AVG()`, `MAX()`, `MIN()`

**GROUP BY** groups rows that have the same value, so you can compute an aggregate per group.

**Clause order (memorize it):**
```sql
SELECT    col, AGG(col)
FROM      table
WHERE     condition on ROWS        -- before grouping
GROUP BY  col
HAVING    condition on GROUPS      -- after grouping, can use COUNT/SUM...
ORDER BY  col;
```

**Examples on Bookings:**
```sql
-- number of bookings per date
SELECT BookingDate, COUNT(BookingID) FROM Bookings GROUP BY BookingDate;
```
Result: 06-01 → 2, 06-05 → 1, 06-09 → 1.

```sql
-- total guests per customer, only customers with more than 4 guests
SELECT CustomerID, SUM(Guests) FROM Bookings
GROUP BY CustomerID
HAVING SUM(Guests) > 4;
```
Groups: 1 → 6, 2 → 3, NULL → 5. Result: **1 → 6 and NULL → 5** (GROUP BY puts the NULLs in their own group).

```sql
-- per date, but only in June (row filter BEFORE grouping)
SELECT BookingDate, COUNT(*) FROM Bookings
WHERE BookingDate BETWEEN '2026-06-01' AND '2026-06-30'
GROUP BY BookingDate;
```

```sql
-- the course example: sort by the count
SELECT COUNT(CustomerID), Country FROM Customers
GROUP BY Country
HAVING COUNT(CustomerID) > 4
ORDER BY COUNT(CustomerID) DESC;
```

```sql
-- GROUP BY + LEFT JOIN: show customers with 0 bookings too
SELECT Customers.FullName, COUNT(Bookings.BookingID) AS NbBookings
FROM Customers LEFT JOIN Bookings ON Customers.CustomerID = Bookings.CustomerID
GROUP BY Customers.FullName;
```
Result: Amal 2, Bilel 1, Chaima **0**. `COUNT(column)` doesn't count NULLs; `COUNT(*)` would give Chaima 1.

**⚠️ Traps**
- **WHERE vs HAVING**: WHERE filters **rows** and can't use COUNT/SUM. HAVING filters **groups**.
- GROUP BY comes **after** WHERE, never before.
- Columns in SELECT that aren't aggregated must be in GROUP BY.
- "Per X", "for each X", "by X" all mean `GROUP BY X`.

---

## 5. Subqueries

A subquery is a query **inside** another query, written **between parentheses**. It can go in **SELECT, FROM or WHERE** (most often WHERE), and also inside INSERT, UPDATE and DELETE.

**5 types (course):**
- **Single row**: returns 0 or 1 row.
- **Multiple row**: returns 1 or more rows.
- **Multiple column**: returns 1 or more columns.
- **Correlated**: uses a column of the outer query.
- **Nested**: a subquery inside another subquery.

```sql
-- compared with one value
SELECT * FROM Products WHERE Price > (SELECT AVG(Price) FROM Products);

-- EXISTS: true if the subquery returns at least 1 row
SELECT SupplierName FROM Suppliers
WHERE EXISTS (SELECT ProductName FROM Products
              WHERE Products.SupplierID = Suppliers.SupplierID AND Price = 20);

-- ANY (= SOME): true if the condition holds for AT LEAST ONE value
SELECT ProductName FROM Products
WHERE ProductID = ANY (SELECT ProductID FROM OrderDetails WHERE Quantity > 100);

-- ALL: true if the condition holds for EVERY value
SELECT ProductName FROM Products
WHERE ProductID = ALL (SELECT ProductID FROM OrderDetails WHERE Quantity = 10);

-- in FROM (a derived table, which MUST have an alias)
SELECT MAX(items), MIN(items), FLOOR(AVG(items))
FROM (SELECT orderNumber, COUNT(orderNumber) AS items
      FROM orderdetails GROUP BY orderNumber) AS lineitems;
```

---

## 6. INSERT / UPDATE / DELETE / REPLACE

```sql
INSERT INTO Customers (CustomerID, FullName) VALUES (4, 'Dhia');
INSERT INTO Customers (CustomerID, FullName) VALUES (5,'Eya'), (6,'Fedi');   -- several rows

UPDATE Employees SET Salary = Salary * 1.10 WHERE Dept = 'Sales';   -- +10%
UPDATE Customers SET FullName = 'Amel', City = 'Tunis' WHERE CustomerID = 1;

DELETE FROM Customers WHERE CustomerID = 3;
```
⚠️ **UPDATE or DELETE without WHERE changes or deletes EVERY row.**

**REPLACE INTO**: if the key already exists, the old row is **deleted and replaced** (works like an update). If not, the row is **inserted**.
```sql
REPLACE INTO Customers (CustomerID, FullName) VALUES (1, 'Amal B.');   -- syntax 1, like INSERT
REPLACE INTO Customers SET CustomerID = 7, FullName = 'Ghada';         -- syntax 2, like UPDATE
```

**With subqueries:**
```sql
INSERT INTO agent1 SELECT * FROM agents WHERE agent_code = ANY (SELECT agent_code FROM customer WHERE cust_country = 'UK');
UPDATE agent1 SET commission = commission + .02 WHERE 2 >= (SELECT COUNT(cust_code) FROM customer WHERE customer.agent_code = agent1.agent_code);
DELETE FROM customer1 WHERE agent_code = ANY (SELECT agent_code FROM agents WHERE working_area = 'London');
```
Copying data from another table: `INSERT INTO new_table SELECT … FROM old_table WHERE …` (the **FROM clause** names the existing table).

---

## 7. ALTER TABLE (changing the STRUCTURE, not the data)

| Action | Syntax |
|---|---|
| Add a column | `ALTER TABLE Employees ADD Email VARCHAR(255);` |
| Change the type | `ALTER TABLE Employees MODIFY COLUMN Email VARCHAR(100);` |
| Rename a column (and give the type) | `ALTER TABLE Employees CHANGE Email BusinessEmail VARCHAR(50);` |
| Delete a column | `ALTER TABLE Employees DROP COLUMN Email;` |
| Rename the table | `ALTER TABLE OrderStatus RENAME OrderDeliveryStatus;` |
| Add a foreign key | `ALTER TABLE Orders ADD FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID);` |

- **MODIFY** changes the type, keeping the same name.
- **CHANGE** changes the name, and you must rewrite the type.
- **UPDATE** changes the **data** (values). **ALTER** changes the **structure** (columns).
- **DELETE FROM** removes rows. **DROP COLUMN** removes a column. **DROP TABLE** removes the whole table.

---

## 8. Constraints (as written in CREATE TABLE)
```sql
CREATE TABLE Students (
  StudentID INT AUTO_INCREMENT,
  Email VARCHAR(255) UNIQUE,                 -- no duplicates
  Name VARCHAR(100) NOT NULL,                -- mandatory
  Age INT CHECK (Age >= 18),                 -- a rule on the values
  City VARCHAR(50) DEFAULT 'Tunis',          -- automatic value
  DeptID INT,
  PRIMARY KEY (StudentID),
  FOREIGN KEY (DeptID) REFERENCES Departments(DeptID)
);
-- composite primary key:  PRIMARY KEY (StudentID, CourseID)
```
**3 types:**
- **Key**: the PK is unique and never NULL.
- **Domain**: valid type or range of values.
- **Referential integrity**: a FK value must exist in the referenced table.

---

## 9. Views

A **view** is a virtual table. It **stores no data**; it shows data from the base tables.
```sql
CREATE VIEW OrdersView AS SELECT OrderID, Quantity, Cost FROM Orders;

SELECT * FROM OrdersView;                          -- use it like a table
UPDATE OrdersView SET Cost = 250 WHERE OrderID = 2; -- changes the BASE table (Orders)
```
**3 benefits:**
1. **Simplifying access** to data: no need to retype complex joins.
2. **Manipulating data**: filter or update the base table through it.
3. **Security**: show only some columns and hide the sensitive ones.

---

## 10. Quick self-test (answers below; cover them first)

1. "List all employees, including those without a department." Which join?
2. "Departments with more than 3 employees." WHERE or HAVING?
3. Is the value 50 included in `BETWEEN 10 AND 50`?
4. Rename the column `tel` to `phone`: MODIFY or CHANGE?
5. What happens with `UPDATE Employees SET Salary = 0;`?
6. Does a view take storage space?
7. `A LEFT JOIN B` can be rewritten as…?
8. LIKE pattern for "second letter is o"?

<details><summary>Answers</summary>

1. LEFT JOIN, with Employees on the left.
2. HAVING (the condition is on COUNT).
3. Yes, BETWEEN includes both limits.
4. CHANGE (`CHANGE tel phone VARCHAR(20)`).
5. Every employee's salary becomes 0, because there's no WHERE.
6. No, it's virtual.
7. `B RIGHT JOIN A`.
8. `'_o%'`

</details>
