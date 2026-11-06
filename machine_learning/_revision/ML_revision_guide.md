# Machine Learning: revision guide

Course: Dr. Ameni Youssfi Nouira, PRISTINI 2026/2027.
Full slide-by-slide explanation: `Chap2_explained_simply.md`.
Sources read: `Chap1_Introduction_to_ML.pdf` (38 slides), `Chap2_Supervised_Learning_Regression.pdf` (63 slides),
`Lab1_datamining-1.pdf`, `Lab2_LinearRegression_HousePrice.pdf`, `feature_scaling.pdf`.
Slide numbers are approximate (taken from extracted text). Some slides are images only:
their diagrams and formulas weren't in the text, so check them in the PDF.

---

## Chapter map: what you must know

### Chapter 1: Introduction to ML
1. **Definition (Mitchell):** a program learns from experience **E** on tasks **T** with
   performance measure **P** if P on T improves with E. *Exam favourite: be able to name E, T and P for an example.*
   - Spam filter: T = classify emails, E = emails labelled spam/not spam, P = % correctly classified.
2. **Why ML:** too much data, explicit rules impossible (images, speech), hidden correlations.
3. **Generalization** = performing well on **new, unseen** data, not just on the training data.
4. **4 types of learning**

   | Type | Data | Goal | Example |
   |---|---|---|---|
   | Supervised | labelled | predict output | price prediction, spam |
   | Unsupervised | unlabelled | find structure (clustering, association) | customer segments |
   | Semi-supervised | few labelled + many unlabelled | as supervised, cheaper labelling | photo tagging |
   | Reinforcement | rewards/penalties from environment | maximize reward | game agent, robot |

   Prof's analogy: supervised = teacher at home *and* school; unsupervised = figure it out
   yourself; semi-supervised = a few concepts in class, then homework on similar ones.
5. **Data → Information → Knowledge** (raw facts → interpreted → combined with experience/insight).
6. **Data split:** Training (the model learns from it) / Validation (tuning while training) /
   Test (final **unbiased** evaluation, never seen during training).
7. **Variable types** (very likely exam question):
   - Numeric/quantitative → **continuous** (GPA, height, temperature) / **discrete** (number of courses, calls).
   - Categorical/qualitative → **ordinal** (Beginner < Intermediate < Advanced; Poor < Average < Good) /
     **nominal** (gender, phone colour: no order).
8. **Labelled / unlabelled / semi-labelled / weakly labelled / noisy data.**
9. **The 5 V's:** Volume, Variety, Velocity, Value, Veracity.

### Chapter 2: Supervised learning: regression
1. **Classification** (category) vs **Regression** (continuous number).
2. **Simple linear regression:** `ŷ = w·x + b` (w = slope, b = intercept).
   The best-fit line minimizes the **sum of squared residuals**; it passes through **(x̄, ȳ)**.
   Residual = `y − ŷ` (observed − predicted).
3. **Cost functions**
   - Mean error: useless alone, positive and negative errors cancel out.
   - **MSE / course cost:** `J(w,b) = 1/(2m) · Σ (ŷᵢ − yᵢ)²` (the ½ makes the derivative cleaner).
   - **MAE** = `1/m · Σ |ŷᵢ − yᵢ|`
   - **RMSE** = `√MSE`, same unit as y.
4. **Gradient descent:** the cost function *measures* how good the model is; GD *improves* it.
   ```
   repeat until convergence (SIMULTANEOUS update):
     w := w − α · ∂J/∂w      ∂J/∂w = 1/m · Σ (ŷᵢ − yᵢ)·xᵢ
     b := b − α · ∂J/∂b      ∂J/∂b = 1/m · Σ (ŷᵢ − yᵢ)
   ```
   - Derivative > 0 → w decreases; derivative < 0 → w increases.
   - **Simultaneous update:** compute both temp values with the *old* w,b, then assign.
     Updating w first and using the new w to compute b is the "incorrect" version on the slide.
   - **Learning rate α:** too small → slow; too large → overshoots, oscillates, diverges.
5. **Multiple linear regression:** `Y = β0 + β1·x1 + … + βn·xn`.
   - Solve by gradient descent (big datasets) **or** the **normal equation**
     `β = (XᵀX)⁻¹ XᵀY` (exact, slow when there are many features). X gets a first column of 1s for β0.
6. **Polynomial regression:** `y = β0 + β1x + β2x² + … + βd·xᵈ`.
   Non-linear in x but **linear in the coefficients**, so linear-regression techniques still work.
   Degree 1 = linear, 2 = quadratic, 3 = cubic. Use it for curves, cycles, turning points.
   Very high degree → **overfitting** (Lab 2, Task 3.4).

### Feature scaling (handout + Lab 1)
- Why: features with very different ranges (size 300–2000 vs bedrooms 0–5) need very
  different weights, and gradient descent zigzags and converges slowly. Scaling fixes both.
- Min-Max: `(x − min)/(max − min)` → [0,1], sensitive to outliers.
- Mean normalization: `(x − μ)/(max − min)` → about [−1,1], centred.
- Z-score: `(x − μ)/σ`, with `σ = √(1/n · Σ(xᵢ−μ)²)` → mean 0, std 1.
- Lab 1 also covers: Robust (median & IQR, good with outliers), Max-Abs (`x/max|x|` → [−1,1], sparse data), L2 unit norm.

---

## Worked examples, re-checked with Python ✅

**Gradient descent (Chap2 slides ~40–42):** data (1,2),(2,4),(3,5),(4,8), w=b=0, α=0.1, m=4
- Errors ŷ−y = −2, −4, −5, −8 → J(0,0) = 1/8·(4+16+25+64) = **13.625**
- ∂J/∂w = 1/4·(−2·1 −4·2 −5·3 −8·4) = −57/4 = **−14.25** → w = 0 − 0.1·(−14.25) = **1.425**
- ∂J/∂b = 1/4·(−19) = **−4.75** → b = **0.475**
- J(1.425, 0.475) = **0.4823** ✅
- The slide leaves iteration 2 blank. Answer: **w = 1.6625, b = 0.54625, J ≈ 0.1239** (try it by hand!).

**Normal equation (Chap2 ~slide 50):** rows of X `[1,1,4] [1,2,5] [1,3,8] [1,4,2]`, Y = `[1,6,8,12]`
→ β0 = −1.699, β1 = 3.484, β2 = −0.055 ✅ (matches the slide's −1.69 / 3.48 / −0.05).

**Feature scaling handout:** w1=0.1, w2=50, b=50 on (2000 ft², 5 bed) → 200+250+50 = $500k ✅.

---

## ⚠ Errata: mistakes or typos in the material (don't copy them into the exam)

1. **Chap2, MAE slide:** says "MAE is a variation of MAE that square difference instead of
   absolute value". That's backwards. **MAE uses the absolute value |ŷ−y|**, MSE uses the square.
2. **Chap2, multiple-LR result:** written `Y = −1.69 + 3.48x1 + (−0.05)x4`. It should be **x2**.
3. **Chap2, regression-line slide:** mentions "the slope **m**" while the formula uses **w**. Same thing.
4. **Chap2, "Regression steps" slide:** talks about "classes" and an "error rate" (number
   wrong / total). That's a *classification* metric; for regression use MSE/MAE/RMSE.
5. **Chap2, cost-function slide:** "as close as possible to the predicted value" should read
   "to the **actual** value".
6. **Lab 1, normalization code:** `df['x'] / df['x'].max()` is labelled "Min-Max", but it's
   really **Max-Abs/simple-feature scaling**. It equals min-max only when min = 0.
   True min-max: `(x − x.min()) / (x.max() − x.min())`.
7. **Chap2 slide 49:** (XᵀX)⁻¹Xᵀ first entry printed 0.05, really **1.36** (the final β's on the slide are still right).
8. **Chap2 slide 54:** "simple *polynomial* regression only works when linear" should say simple **linear** regression.
9. **Chap1:** "continuous variables… their values will remain in that finite interval" is
   loosely worded. Continuous means *any real value in a range*.

---

## Likely exam questions (practise these)
1. Define ML with E/T/P and apply it to a new example.
2. Classify variables in a table (nominal / ordinal / discrete / continuous).
3. Supervised vs unsupervised vs semi-supervised vs reinforcement, with one example each.
4. Why do we need a test set? What is generalization?
5. Do 1–2 iterations of gradient descent by hand and compute J before/after.
6. Effect of α too small / too large; what "simultaneous update" means.
7. MSE vs MAE vs RMSE: compute them on 3–4 points and say which is most sensitive to outliers (MSE).
8. Write and use the normal equation; when would you prefer gradient descent?
9. Why polynomial regression is still "linear"; the risk of a high degree.
10. Apply min-max and z-score to a small column of numbers; when to use each.

## Labs checklist
- **Lab 1** (home-value dataset): pandas load/inspect → missing values → standardize labels →
  `price_per_sqft` → normalization → dummy variables → EDA (`corr()`) → 70/30 split → multiple LR
  → MSE/RMSE/R² interpretation.
- **Lab 2** (house price): regplots → simple LR (interpret β0, β1) → multiple LR (interpret
  "all else constant") → polynomial degree 2 (feature count: with n features, degree 2 gives
  `C(n+2,2)` columns including the bias, e.g. 4 features → 15) → compare metrics → residual analysis.
