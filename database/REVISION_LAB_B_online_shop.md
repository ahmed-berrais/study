# Revision Lab B: "Medina Market" online shop (exam-style, less guidance)

> **DS scope: SQL operators → Views.** Questions after views (functions, stored procedures) are marked ⛔ at the end: skip them.
> Same coverage as Lab A, but **you** decide the design. This is how a DS question looks: a text, a messy table, and "design + implement + query". Do Lab A first.
> No hints this time. If a question doesn't say which syntax to use, choose yourself.

---

## The scenario

Medina Market sells Tunisian handmade products online.

- **Suppliers** (artisans) have an ID, a name, a city and a phone. A supplier provides several products; each product comes from **one** supplier.
- **Categories** have an ID and a label (Pottery, Textile, Food…). Each product belongs to one category.
- **Products** have a code, a name, a unit price, a stock quantity and an optional discount rate (many products have no discount).
- **Customers** have an ID, name, email (unique), city and registration date.
- Each customer can have **at most one loyalty card** (card number, points, issue date); each card belongs to exactly one customer.
- A customer places **orders** (order number, date, status: 'pending' / 'shipped' / 'delivered'). An order contains **several products**, and a product can appear in **many orders**. For each order line the shop stores the **quantity** and the **unit price at the moment of sale**.

The shop's old invoice spreadsheet:

| OrderNo | OrderDate | CustID | CustName | CustCity | Products | Qty | UnitPrices | Supplier | SupplierCity |
|---|---|---|---|---|---|---|---|---|---|
| O1 | 2026-09-02 | K1 | Mariem Saidi | Tunis | Couffin, Harissa | 2, 3 | 35, 12 | Dar Sfax / Cap Bon Foods | Sfax / Nabeul |
| O2 | 2026-09-05 | K2 | Hedi Chebbi | Sousse | Nabeul Plate | 1 | 80 | Nabeul Ceramics | Nabeul |
| O3 | 2026-09-20 | K1 | Mariem Saidi | Tunis | Fouta, Nabeul Plate | 4, 2 | 25, 75 | Dar Sfax / Nabeul Ceramics | Sfax / Nabeul |
| O4 | 2026-10-03 | K3 | Salma Rekik | Sfax | Harissa, Olive Oil 1L | 10, 2 | 12, 30 | Cap Bon Foods / Cap Bon Foods | Nabeul / Nabeul |
| O5 | 2026-10-15 | K4 | Nour Feki | Tunis | Fouta, Couffin, Olive Oil 1L | 1, 1, 3 | 25, 35, 30 | Dar Sfax / Dar Sfax / Cap Bon Foods | Sfax / Sfax / Nabeul |
| O6 | 2026-10-28 | K2 | Hedi Chebbi | Sousse | Couffin | 2 | 35 | Dar Sfax | Sfax |

---

## Section 1: Design (Ch1)

1. Identify **all anomalies** of this spreadsheet (insertion, update, deletion) with one concrete example each, using this data.
2. Normalize step by step to **1NF → 2NF → 3NF**. For each step state the rule, the dependency you removed, and the resulting tables with their keys.
3. Draw the final **ERD** (crow's foot) with all 7 tables: `supplier`, `category`, `product`, `customer`, `loyalty_card`, `orders`, `order_line`. Show PKs, FKs, data types, and the cardinality of every relationship.
4. Why do we store `unit_price` in `order_line` when `product` already has a price? (Is it redundancy, or not?)
5. List the candidate keys of `customer`. Primary key? Alternate key(s)?
6. Give the degree of your `order_line` table and its cardinality after you insert the data below.

## Section 2: Implementation (Ch1 + Ch2)

7. Create the database `medina_market` and all 7 tables with **appropriate types** and **all constraints**:
   - price > 0, stock ≥ 0, discount between 0 and 0.5 (CHECK)
   - status limited to the 3 values
   - email UNIQUE, names NOT NULL
   - registration date DEFAULT today
   - order_line: composite PK + 2 FKs
   - loyalty_card: guarantee the 1:1
   - `orders.order_no` AUTO_INCREMENT (an INT this time)
8. Insert the data:

**supplier**: (S1, Dar Sfax, Sfax, 74111222), (S2, Nabeul Ceramics, Nabeul, 72333444), (S3, Cap Bon Foods, Nabeul, NULL), (S4, Djerba Weavers, Djerba, 75555666)

**category**: (1, Textile), (2, Pottery), (3, Food), (4, Jewelry)

**product** (code, name, price, stock, discount, supplier, category):

| code | name | price | stock | discount | supplier | category |
|---|---|---|---|---|---|---|
| P1 | Couffin | 35 | 40 | NULL | S1 | 1 |
| P2 | Fouta | 25 | 100 | 0.10 | S1 | 1 |
| P3 | Nabeul Plate | 80 | 15 | 0.20 | S2 | 2 |
| P4 | Harissa | 12 | 200 | NULL | S3 | 3 |
| P5 | Olive Oil 1L | 30 | 60 | 0.05 | S3 | 3 |
| P6 | Clay Vase | 120 | 5 | NULL | S2 | 2 |

**customer**: (K1, Mariem Saidi, mariem@mail.tn, Tunis, 2026-01-15), (K2, Hedi Chebbi, hedi@mail.tn, Sousse, 2026-03-02), (K3, Salma Rekik, salma@mail.tn, Sfax, 2026-06-20), (K4, Nour Feki, nour@mail.tn, Tunis, 2026-08-11), (K5, Walid Mejri, walid@mail.tn, Bizerte, 2026-10-01)

**loyalty_card**: (LC100, 320 points, 2026-02-01, K1), (LC101, 90 points, 2026-04-10, K2), (LC102, 150 points, 2026-09-01, K4)

**orders**: order 1→K1 2026-09-02 delivered, 2→K2 2026-09-05 delivered, 3→K1 2026-09-20 shipped, 4→K3 2026-10-03 shipped, 5→K4 2026-10-15 pending, 6→K2 2026-10-28 pending

**order_line**: build it **yourself** from the spreadsheet (orders O1…O6 → 1…6, use the quantities and the unit prices at the time of sale).

9. Write 4 INSERTs that **must fail** (one for each: key, domain/CHECK, referential integrity, UNIQUE) and explain each error.
10. ALTER: add `country VARCHAR(30) DEFAULT 'Tunisia'` to customer; change `phone` to `VARCHAR(20)`; rename `stock` to `quantity_in_stock` (CHANGE); drop `country`; rename table `orders` → `customer_order` and back.

## Section 3: Queries (Ch1 operators + Ch2)

Write **one** SQL statement for each.

**Filtering and operators**

11. Products with their price after discount: `price * (1 - discount)`. What happens for products whose discount is NULL? Rewrite it to show only discounted products (`IS NOT NULL`).
12. Stock value of each product (`price * stock`), aliased `stock_value`, sorted descending.
13. Products priced between 20 and 80 that are **not** in category 3.
14. Customers from Tunis **or** Sfax (2 ways: `OR` and `IN`).
15. Customers whose name contains "ri" (case insensitive).
16. Products whose name has exactly 7 characters (with `LIKE` and `_`).
17. Suppliers without a phone.
18. Order lines whose quantity is odd (`%`).

**Joins**

19. Each product with its category label and supplier name.
20. Each order: order number, date, customer name, status.
21. Full detail of every order line: customer name, order date, product name, quantity, line total (`quantity * unit_price`).
22. All customers and their loyalty card number, **including** customers without a card.
23. All suppliers and their products, **including** suppliers with no product (RIGHT JOIN this time, so choose your table order carefully).
24. Products **never ordered** (2 ways: LEFT JOIN … IS NULL, and NOT EXISTS).
24b. SELF JOIN: pairs of customers who live in the **same city** (no self-pairs, no duplicates).
24c. FULL OUTER JOIN of `customer` and `loyalty_card`: give the course syntax, then the MySQL equivalent.
25. `UNION`: one list of all cities appearing in the database (customers and suppliers), without duplicates.

**Grouping**

26. Total amount of each order (`SUM(quantity * unit_price)`), sorted descending.
27. Total spent by each customer (name). Show only customers who spent **more than 150**.
28. Number of products per category, **including** categories with 0 products.
29. Quantity sold per product: show only products sold in quantity ≥ 5.
30. Number of orders per status.
31. Revenue per order date, only for orders placed **between** 2026-10-01 and 2026-10-31.
32. The city with the most customers (`ORDER BY … LIMIT 1`).

**Subqueries**

33. Products more expensive than the **average** product price.
34. Customers who placed **at least one** order containing Pottery (EXISTS).
35. Products whose price is **greater than ALL** Food products' prices.
36. Products whose price is **equal to ANY** unit price that appears in order 5.
36b. Correlated subquery in SELECT: each customer name with their number of orders.
36c. Nested subquery (no joins): names of customers who bought a product supplied by 'Cap Bon Foods'.
36d. Classify each subquery you wrote in 33–36c: single row / multiple row / multiple column / correlated / nested.
37. From a derived table of order totals: the max, min and FLOOR(AVG) order total.
38. Create `big_orders` (order_no, total) and fill it with INSERT…SELECT for orders with total > 100.
39. UPDATE with subquery: add 50 loyalty points to every card whose owner has **2 or more** orders.
40. DELETE with subquery: delete from `big_orders` the orders whose customer lives in Sousse.
41. REPLACE INTO `category` for (4, 'Jewellery & Silver') and (5, 'Cosmetics'). Explain both results. Then redo the second one with the `REPLACE INTO … SET …` syntax.
42. UPDATE: mark order 5 as 'shipped'. Decrease the stock of every product in order 5 by its ordered quantity (UPDATE with a join **or** a subquery).

## Section 4: Views (Ch2), the last DS topic

43. View `v_order_summary`: order no, customer name, date, status, total.
44. Use the view: pending orders whose total > 50.
45. View `v_product_catalog` for customers (name, category, price, discounted price), **without** stock or supplier. Which view benefit is this?
46. Update the catalog price of P6 through a simple single-table view. Explain why it works on the base table.

## Section 5: Explain in your own words (exam theory)

55. Difference between a primary key, a candidate key, an alternate key, a composite key and a foreign key.
56. What's a partial dependency? A transitive dependency? Give one example of each **from this lab**.
57. INNER vs LEFT vs RIGHT JOIN, with an example from this lab where the results differ.
58. WHERE vs HAVING. UNION vs UNION ALL. MODIFY vs CHANGE. DELETE vs DROP.
59. Why are M:N relationships never kept in the physical model?
60. View vs table: does a view take storage? Can you UPDATE through it?

---

# ⛔ OUT OF DS SCOPE (functions and stored procedures come after views)

47. Functions: for each customer show `UPPER(name)`, the first 3 letters of the city, `CHAR_LENGTH(email)`, `CONCAT_WS(' | ', id, name, city)`.
48. For each order: `DAYNAME(date)`, `QUARTER(date)`, the expected delivery date `ADDDATE(date, INTERVAL 7 DAY)`, and the days since order (`DATEDIFF(CURDATE(), date)`).
49. `FORMAT` the revenue per order with 2 decimals; show `CEIL` and `FLOOR` of the average unit price.
50. `COALESCE(phone, 'no phone')` for suppliers; `NULLIF(discount, 0.10)` for products: explain the output.
51. `CASE` on loyalty points: < 100 → 'Bronze', 100–299 → 'Silver', ≥ 300 → 'Gold'.
52. Procedure `GetOrdersOfCustomer(cid VARCHAR(5))`: lists orders + totals of one customer. Call it for K1.
53. Procedure `GetProductsInPriceRange(minP DECIMAL(8,2), maxP DECIMAL(8,2))`. Call it for 20 and 50.
54. Procedure `GetLowStock()` with no parameter: products with stock < 20. Call it, then drop it.

---

✅ Send me your ERD (photo or text), your normalization steps and your `.sql`, section by section, and I'll correct everything.
