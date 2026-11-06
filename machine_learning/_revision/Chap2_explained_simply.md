# Chapter 2 (Supervised Learning: Regression), explained simply, slide by slide

Source: `machine_learning/Chap2_Supervised_Learning_Regression.pdf` (63 slides). I opened every slide as an image, so pictures and formulas are included.
For each part: **what's on the slide → the idea in simple words → a tiny example with numbers → 🎯 what you need for the exam.**
All the numbers below were re-checked in Python.

**Words you'll see everywhere**
- **x** = input / feature / independent variable (e.g. house size).
- **y** = real answer / target / label / dependent variable (e.g. the real price, from the data).
- **ŷ** = **predicted** answer = what the line says. The slides also write it **f_w,b(x)** or **h_θ(x)**; all three mean the same thing.
- **w, b** (or β0, β1, …) = **parameters**: the numbers the model *learns*.
- **m** = number of examples (rows in the data).

---

## Part 1: Slides 1–6, what supervised learning and regression are

**Slide 2:** supervised learning trains on **labelled** data. Each example = input + correct output (the *label*). The model compares its prediction with the correct answer and adjusts itself to reduce the error.

**Slide 3:** two main types.
- **Classification:** predicts a **category** (spam / not spam).
- **Regression:** predicts a **number** (price, temperature).

**Slide 5:** regression finds a mathematical function that links the features to a numerical target (house price from size, location, rooms; tomorrow's temperature; crypto prices).

**Tiny example:** a teacher gives you 100 corrected exercises (input + answer). You study them, then solve a new one alone. Corrected exercises = labelled data, the new exercise = unseen data.

🎯 **Exam:** define supervised learning; say whether a problem is classification or regression. Examples: "predict the price of a car" → regression. "Predict whether a tumour is benign or malignant" → classification.

---

## Part 2: Slides 7–13, linear regression, the line and residuals

**Slide 7:** linear regression fits a **straight line** between the features and a continuous target. It **assumes** the relationship is linear.

**Slide 8 (picture: two boxes)**

| Simple linear regression | Multiple linear regression |
|---|---|
| **one** input → output | **two or more** inputs → output |
| study hours (⏰) → exam score | study hours + attendance + sleep hours → exam score |
| Y = β0 + β1·X + ε | Y = β0 + β1X1 + β2X2 + … + βnXn + ε |

**ε (epsilon)** = the error term: the part of y the line can't explain (luck, things we didn't measure).

**Slide 9 (picture: a pipeline)**
`Train data → Supervised algorithm → Model → Test data → Error rate`
- **Training:** learn from known data with the correct answers.
- **Test:** check on **unseen** data.
- **Error rate = number of errors / total number of tests.**
⚠ Error rate counts right vs wrong answers, which is a **classification** idea. For regression we measure *how far off* we are (MSE, MAE, RMSE, Part 5). The pipeline idea (train → test) is still correct.

**Slide 10:** `Y = wx + b`
- Y = dependent variable (what we predict), X = independent variable (what we know).
- **w = slope:** how much Y changes when X goes up by 1.
- **b = intercept:** the value of Y when X = 0 (where the line crosses the y-axis).

**Tiny example:** ŷ = 2x + 1
| x | ŷ |
|---|---|
| 0 | 1 ← that's b |
| 1 | 3 |
| 2 | 5 ← each +1 in x adds +2 to ŷ, that's w |

**Slide 11:** the goal is a line through the cloud of points with **minimal deviation**. The deviation of each point from the line is called the **error**. Once you have the line, you can predict (e.g. height from weight). Simple linear regression is closely related to the correlation between x and y.

**Slide 12:** the **regression line (line of best fit)** is the line where the **sum of the squared residuals is the smallest**: ŷ = wx + b.
(The slide says "slope **m**": that's **w**. Same thing.)

**Slide 13 (picture: red line, blue dots, dashed gaps d1, d2, d3)**
- Blue dot = **observed** y (real, from the data).
- Point on the red line = **predicted** ŷ.
- Dashed vertical gap = **residual d = observed − predicted = y − ŷ**. It can be **positive** (dot above the line) or **negative** (dot below).

**Tiny example** with the line ŷ = 1.5x + 0.5:
| House | x | real y | predicted ŷ | residual y − ŷ |
|---|---|---|---|---|
| A | 1 | 2 | 2 | 0 (on the line) |
| B | 2 | 4 | 3.5 | **+0.5** (dot above the line) |
| C | 3 | 5 | 5 | 0 |

🎯 **Exam:** meaning of w and b; simple vs multiple; compute residuals from a table; what "best fit" means (smallest sum of squared residuals).

---

## Part 3: Slides 14–26, the cost function J (measuring how bad a line is)

**Slides 14–16:** we want ŷ close to the **actual** y (the slide says "predicted value", which is a typo).
- **Mean error** (just average the errors) **fails**: +3 and −3 cancel, so a bad line can show "0 error".
- **MSE / the course's cost:** `J(w,b) = 1/(2m) · Σ (ŷ − y)²`. Squaring makes every error positive. The ½ only simplifies the derivative later.

**Slide 15:** the best line always passes through the **average point (x̄, ȳ)**.

**Slide 17 (picture: training table):** size in feet² = **feature x**, price in $1000's = **target y**. Model f(x) = wx + b, where **w, b = parameters**.

**Slides 18–21: b = 0, so J becomes a simple curve.** Data (1,1), (2,2), (3,3), model ŷ = wx:
| w | errors ŷ − y | J(w) = 1/6·Σ(error²) |
|---|---|---|
| −0.5 | −1.5, −3, −4.5 | **5.25** |
| 0 | −1, −2, −3 | **2.33** |
| 0.5 | −0.5, −1, −1.5 | **0.58** |
| 1 | 0, 0, 0 | **0** ← best |
Plot these and you get the **U-shaped curve** on slide 21, with its bottom at w = 1. **Each w is a different line, and the lowest J is the best line.**

**Slides 23–26: b ≠ 0, so J is a 3D bowl.** With w and b both free, J(w,b) is a **bowl**. The bottom is the best (w, b).
- **Mount Fuji photos:** contour lines = rings of **equal height**. The bowl seen from above becomes **ellipses** (a contour plot).
- **Slide 25:** a bad line (w ≈ −0.15, b ≈ 500) slopes down while the data goes up, so its × is **far** from the centre of the ellipses.
- **Slide 26:** the good line **f(x) = 0.13x + 71** has small error arrows, and its × is **at the centre**.
- **One point on the contour plot = one line on the data graph.**

🎯 **Exam:** compute J for a few values of w by hand (table above); why we square; what a contour plot means.

---

## Part 4: Slides 27–37, gradient descent (fixing the line step by step)

- **Slide 28:** J *measures* how bad the line is. Gradient descent *improves* it by giving the direction to change w and b.
- **Slide 29:** start from some w, b → keep changing them to reduce J → stop near the minimum.
- **Slide 30 (bumpy picture):** some cost surfaces have **several valleys** (local minima), so gradient descent can get stuck in one that isn't the lowest. **(extra)** For linear regression with MSE, J is always one single bowl, so this doesn't happen.
- **Slide 31:** the algorithm (repeat until convergence) is below. Update w and b **simultaneously**: compute both new values from the old ones, *then* assign.
  ```
  w = w − α · ∂J/∂w        ∂J/∂w = 1/m · Σ (ŷ − y) · x
  b = b − α · ∂J/∂b        ∂J/∂b = 1/m · Σ (ŷ − y)
  ```
- **Slides 32–33:** these derivatives come from the chain rule. The 2 from the square cancels the ½. The only difference between them: ∂J/∂w has **· x**, ∂J/∂b doesn't.
- **Slide 34 (two pictures):** slope **> 0** (right side of the U) → w **decreases**. Slope **< 0** (left side) → w **increases**. Either way you move toward the bottom.
- **Slides 35–37 (worked example):** data (1,2), (2,4), (3,5), (4,8), w = b = 0, α = 0.1.
  J = 13.625 → ∂J/∂w = −14.25, ∂J/∂b = −4.75 → w = 1.425, b = 0.475 → J = **0.4823**.
  Iteration 2 (blank on the slide) = practise it yourself; the answer is in `ML_revision_guide.md`.

🎯 **Exam:** 1–2 iterations by hand; both derivative formulas; correct vs incorrect update; what happens to w when the slope is positive or negative.

---

## Part 5: Slides 38–40, the learning rate α and the other error measures

### Slide 38: how to choose the learning rate α

`w = w − α · ∂J/∂w`, so **α = the size of each step.**

**The two pictures:**
- **Top (good α):** orange dots walk **down** the U in small steps until they reach the minimum.
- **Bottom (α too large, "over-aggressive"):** the pink arrows **jump from one side of the U to the other** and climb higher each time. That's overshooting.

| α | What happens |
|---|---|
| too small | ✓ it works, but **slowly**: many iterations needed |
| too large | ✗ **overshoots** the minimum, ✗ may **oscillate**, ✗ may **diverge** (J explodes) |
| good | fast **and** stable convergence |

**Tiny example** (the professor's data, starting from w = b = 0). J over the first 4 iterations:
| α | iter 0 | iter 1 | iter 2 | iter 3 | Verdict |
|---|---|---|---|---|---|
| 0.01 | 13.6 | 11.5 | 9.6 | 8.1 | too slow 🐢 |
| 0.1 | 13.6 | 0.48 | 0.12 | 0.11 | good ✅ |
| 0.3 | 13.6 | 30.7 | 69.4 | 157 | diverges 💥 |

Try this in the **ML Study Lab** with the α slider.

🎯 **Exam:** "What happens if α is too large / too small?" with a sketch of the U and the zig-zag arrows. Also: "J increases after each iteration, why?" → α is too large.

### Slide 39: MAE (mean absolute error)

`MAE = 1/m · Σ |ŷ − y|`, the average **distance** between the prediction and the real value, with no squaring.
⚠ **Slide error:** it says "MAE is a variation of MAE that squares the difference instead of taking the absolute value". That's wrong. **MAE uses the absolute value |…|; MSE uses the square.** The formula on the slide (with |…|) is correct; only the sentence is wrong. Use the formula in the exam.

### Slide 40: RMSE (root mean squared error)

`RMSE = √( Σ (predicted − actual)² / N )` = **√MSE**. Taking the root brings the error back to the **same unit as y** (e.g. k$ instead of k$²). It's one of the two main performance measures for regression.

### All three on the same example (the error measures compared)

Real y = 10, 20, 30, 40, predicted ŷ = 12, 18, 31, 30. Errors: +2, −2, +1, **−10** (one big mistake).

| Measure | Calculation | Result |
|---|---|---|
| MAE | (2 + 2 + 1 + 10) / 4 | **3.75** |
| MSE | (4 + 4 + 1 + 100) / 4 | **27.25** |
| RMSE | √27.25 | **5.22** |

The single big error (−10) dominates MSE (100 out of 109) because squaring punishes big errors hard. **MSE and RMSE are sensitive to outliers; MAE is more robust.**
Note: the course's cost J = 1/(2m)·Σ(…)² is MSE ÷ 2. Same idea, the ½ is only for the derivative.

🎯 **Exam:** compute MAE, MSE and RMSE on 3–4 points; which one is most sensitive to outliers (MSE); why RMSE is easier to interpret (same unit as y).

**Slide 41:** "LAB datamining" means your **Lab 1** goes here: load data, clean it, scale it, 70/30 split, train, compute MSE/RMSE.

---

## Part 6: Slides 42–53, multiple linear regression (several inputs)

### Slide 42: the equation (picture with arrows)

`Y = β0 + β1·X1 + β2·X2 + … + ε`
- **Y** = dependent variable (response).
- **X1, X2, …** = independent variables (predictors).
- **β0** = y-intercept (base value).
- **β1, β2, …** = slope coefficients: one per input.
- **ε** = error term.

### Slide 43 (picture: table with 4 features)

| Size (feet²) x1 | Bedrooms x2 | Floors x3 | Age (years) x4 | Price ($1000's) y |
|---|---|---|---|---|
| 2104 | 5 | 1 | 45 | 460 |
| 1416 | 3 | 2 | 40 | 232 |
| 1534 | 3 | 2 | 30 | 315 |
| 852 | 2 | 1 | 36 | 178 |

Now each house has **4 inputs** instead of 1.

### Slide 44: the model with an example

Before: `f(x) = wx + b`. Now: `f(x) = w1x1 + w2x2 + w3x3 + w4x4 + b`.
The slide's example: **f(x) = 0.1·x1 + 4·x2 + 10·x3 − 2·x4 + 80**

**How to read it:**
- +0.1 per extra feet²
- +4 (k$) per extra bedroom
- +10 per extra floor
- **−2** per year of age: older house, cheaper (a negative coefficient)
- 80 = base price
- Each one applies **while the other inputs stay the same**.

**Tiny example:** prediction for house 1 (2104, 5, 1, 45):
0.1·2104 + 4·5 + 10·1 − 2·45 + 80 = 210.4 + 20 + 10 − 90 + 80 = **230.4 k$**
Its real price is 460, so this example model under-predicts. It's just an illustration; training would adjust the w's.

### Slide 45: vector notation (just a shorter way to write the same thing)

- **w⃗ = [w1 w2 … wn]**, the parameters, and **x⃗ = [x1 x2 … xn]**, the inputs. b is still a single number.
- `f(x⃗) = w⃗ · x⃗ + b` where **w⃗ · x⃗ = w1x1 + w2x2 + … + wnxn** (the **dot product**: multiply pair by pair, then add).
- Link to Advanced Python: in NumPy this is `np.dot(w, x) + b`.

### Slide 46: way 1 to find the β's, gradient descent

`βj := βj − α · ∂J/∂βj` for **every** j, repeated until J is minimal. It's the same idea as Part 4, with one update per coefficient.
✓ works on big datasets ✓ used everywhere in ML.

### Slide 47: way 2, the analytical solution (normal equation)

`β = (XᵀX)⁻¹ Xᵀ Y`: a formula that gives the best β's **directly**, with no steps and no α.
✓ exact solution ✗ slow for very large datasets (inverting a big matrix is expensive).

| | Gradient descent | Normal equation |
|---|---|---|
| How | step by step | one formula |
| Needs α? | yes | no |
| Big data | ✓ fast | ✗ slow |
| Result | approximate (close to the best) | exact |

### Slides 48–50: the worked example (weekly sales)

Weekly sales Y depend on Product 1 (x1) and Product 2 (x2): **Y = β0 + β1x1 + β2x2**.

| x1 | x2 | Y |
|---|---|---|
| 1 | 4 | 1 |
| 2 | 5 | 6 |
| 3 | 8 | 8 |
| 4 | 2 | 12 |

**Step 0, build X:** add a **column of 1s** in front (it multiplies β0):
```
X = [1 1 4]      Y = [ 1]
    [1 2 5]          [ 6]
    [1 3 8]          [ 8]
    [1 4 2]          [12]
```
(The slide prints the rows as "114, 125, 138, 142". Those are the rows [1 1 4], [1 2 5], … without spaces.)

**Step 1, XᵀX** (3×4 times 4×3 gives 3×3):
```
XᵀX = [ 4  10  19]     4 = number of rows,  10 = Σx1,  19 = Σx2
      [10  30  46]    30 = Σx1²,  46 = Σx1·x2
      [19  46 109]   109 = Σx2²
```
A shortcut: every entry is just a sum. Check: Σx1·x2 = 1·4 + 2·5 + 3·8 + 4·2 = 46 ✅

**Step 2, invert it:**
```
(XᵀX)⁻¹ ≈ [ 3.15  −0.59  −0.30]
          [−0.59   0.20   0.016]
          [−0.30   0.016  0.054]
```
**Step 3, multiply by Xᵀ:**
```
(XᵀX)⁻¹Xᵀ ≈ [ 1.36   0.47  −1.02   0.19]
            [−0.32  −0.098  0.155  0.26]
            [−0.065  0.005  0.185 −0.125]
```
⚠ **Slide error:** the first number is printed as **0.05**. It's really **1.36**. With 0.05, β0 would come out as −3.0, not −1.69. The slide's final answer is correct, so only this one number is a typo.

**Step 4, multiply by Y:**
β0 = 1.36·1 + 0.47·6 − 1.02·8 + 0.19·12 ≈ **−1.69** (same pattern for the other two rows)
→ **β0 = −1.69, β1 = 3.48, β2 = −0.05**

**Result: Y = −1.69 + 3.48·x1 − 0.05·x2.** The slide writes "x4" at the end; that's a typo for **x2**.
- Meaning: each extra unit of Product 1 adds about **3.48** to weekly sales. Product 2 barely matters (−0.05 ≈ 0).
- Check row 1: −1.69 + 3.48·1 − 0.05·4 = **1.57** vs real 1, close.

**In the exam:** a 3×3 inverse by hand is long. The professor may give you (XᵀX)⁻¹ and ask you to finish, or ask you to build X with the column of 1s and compute XᵀX. Know every step's *purpose*.

### Slide 51 (picture: a 3D plane)

With 2 inputs, the "line" becomes a **flat plane** in 3D (x1, x2 on the floor, Y as the height). The red dots are the data, and the black sticks are the **residuals** (vertical distance from each dot to the plane). Same idea as before, one dimension up.

**Slide 52:** "Lab Multiple Linear Regression" is your **Lab 2**, Task 3.3.

🎯 **Exam:** interpret coefficients ("all else constant", sign = direction); build X with the 1s column; compute XᵀX; GD vs normal equation; the plane picture.

---

## Part 7: Slides 53–63, polynomial regression (when the data curves)

### Slides 54–55: the idea

Sometimes the points **curve**: plant growth, temperature over a year, prices that rise then fall. A straight line can't follow them. Polynomial regression fits a **curve** by using **powers of x**. It doesn't need the relationship to be linear.
(Slide 54's sentence "a simple polynomial regression algorithm only works when the relationship is linear" should say *simple **linear** regression*.)

### Slide 56 (picture: two graphs)

- **Left: "Simple linear model" y = b0 + b1x.** The straight red line misses the dots at the top, which bend upward.
- **Right: "Polynomial model" y = b0 + b1x + b2x².** The red **curve** bends with the dots and fits them.

### Slides 57–58: the formula

`y = β0 + β1·x + β2·x² + β3·x³ + … + βd·xᵈ + ε`
- d = **degree** (1 = linear, 2 = quadratic, 3 = cubic). The β's are learned, ε is the error.

**The key trick (very important):** the curve isn't linear in **x**, but it **is linear in the β's**. So you create new columns x², x³, … and run **ordinary multiple linear regression** on them. That's why it's still called "linear" and why the same methods (GD, normal equation) work.

**Tiny example: plant growth**
| Day t | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Height h | 1 | 2 | 5 | 10 | 17 |

- **Straight line (degree 1):** best fit h = 4t − 1, which predicts −1, 3, 7, 11, 15. It's wrong at both ends, and MSE = **2.8**.
- **Degree 2:** add a column t² (0, 1, 4, 9, 16). Best fit h = **1 + t²**, which predicts 1, 2, 5, 10, 17. **Perfect**, MSE = 0.

### Slides 59–60: degree and types

| Degree | Shape | Equation |
|---|---|---|
| 1 | straight line | y = β0 + β1x |
| 2 | parabola, **1 bend** | y = β0 + β1x + β2x² |
| 3 | **2 bends** | + β3x³ |
| 4+ | more bends | quartic, … |

Higher degree = more complex curve.

### Slide 61 (picture: degrees 1 to 4 on the same wavy data)

The orange dots go up, down, up, down (a wave).
- **Green, degree 1:** a straight line through the middle. It misses everything (underfitting).
- **Blue, degree 2:** one gentle bend, still poor.
- **Red, degree 3:** follows part of the wave.
- **Yellow, degree 4:** follows the ups and downs best.
**Lesson:** more degree means more flexibility. **(extra, but Lab 2 asks it)** Too high a degree (e.g. 10) makes the curve wiggle through every point, so it memorizes the noise and predicts new data badly. That's **overfitting**, the opposite of generalization (Chapter 1). Choose the degree by checking the error on the **test** set, not the training set.

### Slide 62: when to use polynomial regression

1. **Curved trends:** plant growth, population growth that speeds up or slows down.
2. **Seasonal / cyclical patterns:** temperature over the year, sales or stock cycles.
3. **Turning points:** y goes up then down (or the reverse) within your data.

**Slide 63:** "Lab Polynomial Regression" is your **Lab 2**, Task 3.4.

🎯 **Exam:** why polynomial regression is still "linear" (linear in β); recognize which degree fits a picture; the overfitting risk of a high degree; give the 3 situations where you'd use it.

---

## ⚠ All slide errors found in Chapter 2

| Slide | Says | Correct |
|---|---|---|
| 9 | error rate = errors / total (for regression) | that's a classification measure; regression uses MSE / MAE / RMSE |
| 12 | "slope **m**" | slope **w** |
| 14 | "close to the **predicted** value" | close to the **actual** value |
| 39 | "MAE … squares the difference" | MAE takes the **absolute value**; MSE squares |
| 49 | (XᵀX)⁻¹Xᵀ first entry **0.05** | **1.36** |
| 50 | Y = −1.69 + 3.48x1 − 0.05**x4** | … − 0.05**x2** |
| 54 | "simple **polynomial** regression only works when … linear" | simple **linear** regression |

## The whole chapter in one chain

**Labelled data** → **model ŷ = wx + b** → **residuals y − ŷ** → **cost J (MSE)** → **gradient descent with a good α** → **more inputs: multiple LR (GD or normal equation)** → **curves: polynomial LR (watch out for overfitting)** → **measure on test data with MAE / MSE / RMSE**
