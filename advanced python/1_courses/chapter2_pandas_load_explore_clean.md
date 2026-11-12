# Chapter 2 — pandas I: Load, Explore and Clean
*Python for Data Science · GLSI · S2 — "Turn a messy file into a trusted dataset"*
Source: `Chapter2_pandas_Load_Explore_Clean_EN.pptx` (teacher's Drive link in `courses_links.txt`). Session: 1.5 h lecture + 3 h lab (Lab 2).

## Learning objectives
1. Explain Series and DataFrame and load CSV / Excel files
2. Get a first overview with `head`, `info`, `describe`
3. Select and filter data with `loc`, masks and `query`
4. Handle missing values, duplicates, wrong types, typos and outliers
5. Export clean data and document every cleaning decision

## Real data is messy
> "Analysts often spend more time preparing data than analysing it."

TunisMarket exports 12,060 order lines every night — missing prices, duplicated rows, city names typed 50 different ways, quantities of 999. Decisions taken on dirty data are wrong decisions.

## Series and DataFrame
- **index** = row labels (0, 1, 2…) · **columns** = variables, each with one dtype · **Series** = one column `df["city"]`
- A DataFrame is a table; each column is a Series (compare: spreadsheet / dictionary of lists).
```python
import pandas as pd
df = pd.DataFrame({"city": ["Tunis", "Sfax"], "quantity": [1, 3]})
df["city"]            # a Series
df.loc[0, "city"]     # one cell by label
```

## Load and first look — always look before you clean
```python
orders = pd.read_csv("data/orders.csv")
# pd.read_excel("file.xlsx", sheet_name="Sales")
orders.head(10)                    # first rows
orders.shape                       # (12060, 10)
orders.info()                      # types + missing counts
orders.describe()                  # quick statistics -> spot quantity max = 999
orders["status"].value_counts()    # check categories
```
Other formats: Excel, JSON, SQL, Parquet.

## Select and filter
```python
orders[["order_id", "city", "status"]]
mask = ((orders["status"] == "Delivered") & (orders["city"] == "Tunis") & (orders["quantity"] >= 3))
orders.loc[mask, ["order_id", "quantity"]]
orders.query("status == 'Delivered' and quantity >= 3")
```
`.loc[rows, columns]` by label or mask · combine with `&`, `|`, `~` · parentheses around every condition · `query()` is a readable alternative.

## Missing values: choose, don't guess
| Situation | Typical action | Example |
|---|---|---|
| Missing category | Fill with a label | payment_method → "Unknown" |
| Missing numeric value, business rule exists | Impute (median of the group) | unit_price → median price of the same product |
| Missing key field | Drop the rows | order_date missing → cannot place in time |
| Many missing values in a column | Ask the business; maybe drop the column | age missing for 3 % of customers |

**Never replace all missing values by 0**: it creates fake data and biases averages. Document every choice.

## Duplicates and data types
```python
orders.duplicated().sum()          # 60
orders = orders.drop_duplicates()
orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
orders = orders.dropna(subset=["order_date"])
orders["quantity"] = orders["quantity"].astype("int64")
orders.dtypes
```
`errors="coerce"` turns invalid dates into missing values · right types unlock `.dt` and `.str` · save results back: `df["col"] = ...`

## Text cleaning and outliers
```python
orders["city"].nunique()                                   # 50 spellings!
orders["city"] = orders["city"].str.strip().str.title()
orders["city"].nunique()                                   # 10
orders = orders[orders["quantity"] <= 10].copy()           # business rule: max 10 units per line
by_product = orders.groupby("product_id")["unit_price"]
median = by_product.transform("median")
orders["unit_price"] = orders["unit_price"].fillna(median)
```
A business rule beats a purely statistical rule · `transform` returns a column aligned with the rows — ideal for group-wise filling. *Is 999 a real order or a data-entry error? Who can confirm?*

## The cleaning workflow
1 **Raw file** (keep it untouched) → 2 **Explore** (head, info, describe, value_counts) → 3 **Decide** (drop, fill or fix? write it down) → 4 **Clean** (code the decisions in order) → 5 **Validate** (assert / counts before-after) → 6 **Export** (new clean CSV / Excel).
Lab 2 result: 12,060 raw rows → 11,965 clean rows (0.8 % removed).

## A reusable cleaning function
```python
def clean_orders(raw):
    df = raw.drop_duplicates().copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    df = df[df["quantity"] <= 10]
    df["payment_method"] = df["payment_method"].fillna("Unknown")
    return df

orders = clean_orders(pd.read_csv("data/orders.csv"))
orders.to_csv("orders_clean.csv", index=False)
```
Repeatable every night · same input → same output · CSV for pipelines, Excel for business users · pass `parse_dates=[...]` when reading the CSV again.

## Modern pandas: good habits (pandas 3.x; labs also run on 2.2)
- **Copy-on-Write**: a filtered DataFrame is a safe copy. Add `.copy()` when you plan to edit it.
- **String dtype**: text columns use a dedicated `str` dtype by default.
- **Avoid `inplace=True`**: assign back: `df["a"] = df["a"].fillna(0)`.
- **Method chaining**: `df.assign(...).query(...)`.

## Industry use cases: data quality
| Sector | Typical problem | Consequence if ignored |
|---|---|---|
| Banking | Duplicated transactions | Wrong balances, false fraud alerts |
| Healthcare | Different date formats across hospitals | Wrong patient timelines |
| Telecom | Missing usage records | Under-billing customers |
| Retail / e-commerce | Typos in city or product names | Wrong sales reports by region |

## Key takeaways
- DataFrame = table, Series = column; explore before you clean
- Masks and `.loc` filter rows; combine with `& | ~` and parentheses
- Every missing-value treatment is a decision — choose and document it
- Fix types, text and outliers with business rules
- Keep the raw file, export a new clean file, report what changed

## Short recap
1. Which method shows types and missing counts? → `df.info()`
2. Why not fill all missing values with 0? → it creates fake values and biases statistics
3. What does `errors="coerce"` do in `to_datetime`? → turns invalid dates into missing values (NaT)
4. How do you fill a missing price with the product's median? → `fillna(groupby(...).transform("median"))`
