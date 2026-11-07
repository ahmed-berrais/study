# Revision Lab B: "Medina Market" online shop (exam-style)

> **DS scope: from SQL operators to Views.** Answer on **paper**.
> Harder than Lab A: you get only the text and a messy table, and you design everything yourself. No syntax is given; choose what to use. Do Lab A first.

---

## The scenario

Medina Market sells Tunisian handmade products online.

- **Suppliers** (artisans) have an ID, a name, a city and a phone (not always known). A supplier provides several products; each product comes from **one** supplier.
- **Categories** have an ID and a label (Pottery, Textile, Food…). Each product belongs to one category.
- **Products** have a code, a name, a unit price, a stock quantity and an optional discount rate.
- **Customers** have an ID, name, email (unique), city and registration date.
- Each customer can have **at most one loyalty card** (card number, points, issue date). Each card belongs to exactly one customer.
- A customer places **orders** (order number, date, status: pending / shipped / delivered). An order contains **several products**, and a product can appear in **many orders**. For each order line the shop stores the **quantity** and the **unit price at the moment of sale**.

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

## Section 1: Design

1. Give one concrete example from this spreadsheet of each anomaly: insertion, update, deletion.
2. Normalize step by step to **1NF → 2NF → 3NF**. At each step, state the rule, the dependency you removed, and the resulting tables with their keys.
3. Draw the final **ERD** (crow's foot) with all the tables, attributes and data types, PKs/FKs and every cardinality.
4. Why store the unit price on each order line when the product already has a price? Is that redundancy?
5. Candidate keys, primary key and alternate key(s) of the customer table.
6. Degree and cardinality of your order line table once the data below is stored.

## Section 2: Implementation

7. Write the CREATE statements for the whole database with appropriate types and these rules:
   - price strictly positive, stock never negative, discount between 0 and 0.5
   - status limited to the 3 values
   - unique email, mandatory names
   - registration date = today by default
   - order number generated automatically
   - the order line table identified by order + product
   - a customer can never have two loyalty cards

8. The data:

**supplier**: (S1, Dar Sfax, Sfax, 74111222), (S2, Nabeul Ceramics, Nabeul, 72333444), (S3, Cap Bon Foods, Nabeul, no phone), (S4, Djerba Weavers, Djerba, 75555666)

**category**: (1, Textile), (2, Pottery), (3, Food), (4, Jewelry)

**product**:

| code | name | price | stock | discount | supplier | category |
|---|---|---|---|---|---|---|
| P1 | Couffin | 35 | 40 | none | S1 | 1 |
| P2 | Fouta | 25 | 100 | 0.10 | S1 | 1 |
| P3 | Nabeul Plate | 80 | 15 | 0.20 | S2 | 2 |
| P4 | Harissa | 12 | 200 | none | S3 | 3 |
| P5 | Olive Oil 1L | 30 | 60 | 0.05 | S3 | 3 |
| P6 | Clay Vase | 120 | 5 | none | S2 | 2 |

**customer**: (K1, Mariem Saidi, mariem@mail.tn, Tunis, 2026-01-15), (K2, Hedi Chebbi, hedi@mail.tn, Sousse, 2026-03-02), (K3, Salma Rekik, salma@mail.tn, Sfax, 2026-06-20), (K4, Nour Feki, nour@mail.tn, Tunis, 2026-08-11), (K5, Walid Mejri, walid@mail.tn, Bizerte, 2026-10-01)

**loyalty card**: (LC100, 320 points, 2026-02-01, K1), (LC101, 90 points, 2026-04-10, K2), (LC102, 150 points, 2026-09-01, K4)

**orders**: 1→K1 2026-09-02 delivered, 2→K2 2026-09-05 delivered, 3→K1 2026-09-20 shipped, 4→K3 2026-10-03 shipped, 5→K4 2026-10-15 pending, 6→K2 2026-10-28 pending

**order lines**: build them yourself from the spreadsheet (O1…O6 → orders 1…6).

   - a) Write the order line rows as a table.
   - b) Insert the products in one statement.
   - c) Insert customer K5 without giving the registration date.

9. Describe 4 insertions the DBMS would refuse: one per constraint type (key, domain, referential integrity, uniqueness). For each, explain why it's refused.
10. Modify the structure: add a country to customers (default Tunisia); widen the supplier phone to 20 characters; rename stock to quantity_in_stock; remove country; rename the orders table to customer_order.

## Section 3: Queries

Write one SQL query for each request.

**Filtering and operators**

11. Products with their price after discount. What happens for products with no discount? Rewrite the query to show only discounted products.
12. The stock value of each product, under a clear heading, from the highest down.
13. Products priced between 20 and 80 that are not food.
14. Customers from Tunis or Sfax (two ways).
15. Customers whose name contains "ri".
16. Products whose name has exactly 7 characters.
17. Suppliers whose phone is unknown.
18. Order lines whose quantity is odd.
19. The different cities customers come from (each city once).

**Joins**

20. Each product with its category label and supplier name.
21. Each order: number, date, customer name, status.
22. Every order line in full: customer name, order date, product name, quantity, line total.
23. All customers with their card number, including customers with no card.
24. All suppliers with their products, including suppliers with none, using the opposite join from 23.
25. Products never ordered (two ways: with a join, and with a subquery).
26. Pairs of customers who live in the same city (no self-pairs, no duplicates).
27. All customers and all loyalty cards, matched or not.
28. One list of every city in the database (customers and suppliers), without duplicates.

**Grouping**

29. The total amount of each order, from the biggest down.
30. Total spent per customer (name), only customers who spent more than 150.
31. Number of products per category, including categories with none.
32. Quantity sold per product, only products sold 5 times or more.
33. Number of orders per status.
34. Revenue per order date, for October 2026 only.

**Subqueries and data changes**

35. Products more expensive than the average product price.
36. Customers who ordered at least one pottery product.
37. Products more expensive than every food product (two ways: with and without MAX).
38. Products whose price equals one of the unit prices in order 5.
39. Each customer name with their number of orders, computed in the column list.
40. Names of customers who bought a product from Cap Bon Foods, using nested subqueries only.
41. From the totals of each order: the biggest, smallest and average (rounded down) order total.
42. A table big_orders (order number, total) exists. Fill it with every order whose total is over 100.
43. Add 50 points to every card whose owner has placed 2 or more orders.
44. Delete from big_orders the orders of customers living in Sousse.
45. Category 4 becomes "Jewellery & Silver" and a new category 5 "Cosmetics" is added, both with the statement that replaces a row if its key exists or inserts it otherwise. Write each one in a different syntax and explain what happens to each.
46. Order 5 is now shipped: update it. Then reduce the stock of every product in order 5 by the quantity ordered.
47. Classify each subquery you wrote in 35–44 by type.

## Section 4: Views

48. A view summarizing each order: number, customer name, date, status, total.
49. Using that view: pending orders with a total over 50.
50. A catalog view for customers: product name, category, price, discounted price, **without** stock or supplier. Which benefit of views is this?
51. Through a simple view on one table, change the price of P6. Explain why the base table changes.

## Section 5: Explain in your own words

52. Primary key, candidate key, alternate key, composite key, foreign key: define each, with an example from this lab.
53. Partial dependency and transitive dependency: one example of each from this lab.
54. Inner vs left vs right vs full join, with an example from this lab where the results differ. What is a self join?
55. Row filter vs group filter. Union with and without duplicates. The two ways of altering a column. Deleting rows vs dropping a table.
56. Why are M:N relationships never kept as-is in the physical model?
57. View vs table: does a view take storage? Can you modify data through it?

---

✅ Send me your ERD, your normalization steps and your queries, section by section. I'll correct everything.
