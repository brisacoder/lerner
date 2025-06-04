# Lesson Plan: Odds and Log Odds (Logits)

## 1. Overview

**Goal:** Equip students with a solid understanding of *odds*, how they differ from *probabilities*, and why the *log of the odds* (logit) is so useful—especially as a bridge to logistic regression.

**Outcomes:** Learners will be able to

* Convert between probabilities and odds.
* Explain the conceptual difference between odds and probabilities.
* Compute log‑odds and interpret their symmetry.
* Recognize the logit as the core transformation used in logistic regression.

---

## 2. Warm‑Up Discussion (5 min)

Ask: “When sports commentators say *‘the odds are 3‑to‑1 our team wins,’* what do they mean? Is that the same as a 75 % chance?”  Use responses to surface misconceptions.

---

## 3. Core Content
  
### 3.1 Odds vs Probability (always true for *one* group)

* **Odds:**
  $\displaystyle\text{odds} = \frac{\text{number of ways the event happens}}{\text{number of ways the event does *not* happen}}$
  
* **Probability:**
  $\displaystyle P(\text{event}) = \frac{\text{number of ways the event happens}}{\text{total number of possible outcomes}}$

#### Example A – *Underdog Team*

> Odds of winning are **1 to 4**.
>
> $\text{odds}=\tfrac14 = 0.25$  (looks small!)
>
> Probability:
> $P=\frac{1}{1+4}=0.20$

#### Example B – *Favored Team*

> Odds of winning are **5 to 3**.
>
> $\text{odds}=\tfrac53\approx1.67$
>
> Probability:
> $P=\frac{5}{5+3}=0.625$

**Take‑away:** *Odds* compare success to failure; *probability* compares success to everything.

##### Quick Formula Link

If $P = P(\text{win})$ then
$\boxed{\text{odds}=\frac{P}{1-P}}\quad\Longleftrightarrow\quad P = \frac{\text{odds}}{1+\text{odds}}$

---

### 3.2 Computing Odds from Probabilities (10 min)

Use the last example: $P=0.625\Rightarrow\text{odds}=\frac{0.625}{0.375}=1.67$.  Show that identical result comes directly from counts because common denominators cancel.

---

### 3.3 Why **Log Odds**? (20 min)

* **Logit function:** $\operatorname{logit}(P)=\log\Big(\tfrac{P}{1-P}\Big)$
* Resolves *asymmetry* of odds scale:

  * Odds against range 0–1.
  * Odds for range 1–∞.
  * Logit maps (0,1) → (−∞, ∞) **symmetrically**.

#### Example C – Symmetry Demo

| Scenario        | Odds  | Log Odds (natural log) |
| --------------- | ----- | ---------------------- |
| Against 1 to 6  | 0.167 | −1.79                  |
| In favor 6 to 1 | 6.000 | +1.79                  |

Same distance from zero ⇒ easier to compare.

* **Normal‑ish distribution:** Simulating many random win/loss splits (that sum to a constant) yields log‑odds roughly normal → handy for inference.

* **Connection to Logistic Regression:** Logistic model sets
  $\operatorname{logit}(P(Y=1\mid X)) = \beta_0 + \beta_1 X_1 + \dots + \beta_k X_k$
  making log‑odds linear in predictors.

---

## 4. Guided Practice (in class)

1. **Convert & Compare**
   A survey finds 30 % of customers click a link.
   a) Compute the odds of clicking.
   b) Compute the log‑odds.
   c) Explain, in one sentence, why log‑odds are preferred for linear modeling.

2. **From Odds to Probability**
   Betting site quotes odds 9:2 a horse wins. What is the implied probability?

3. **Symmetry Check**
   Show that odds 1:9 and 9:1 yield log‑odds that are negatives of each other. Verify numerically.

---

## 5. Independent Exercises (Homework)

1. *Clinician’s Test*
   A diagnostic test detects a disease with 80 % sensitivity and 90 % specificity on a population where disease prevalence is 10 %. Compute:
   a) The odds that a randomly selected person has the disease.
   b) Posterior odds of disease given a **positive** test (use Bayes: likelihood ratios).
   c) Comment on how log‑odds might simplify additive reasoning here.

2. *Marketing Split‑Run*
   Variant A of an email has 400 opens and 1000 non‑opens. Variant B has 480 opens and 920 non‑opens.
   a) Compute odds of open for each variant.
   b) Compute log‑odds and the *odds ratio*.
   c) Interpret which variant performs better and by how much on the odds scale.

3. *Probability Ladder*
   Fill in the table (round to 3 dp):

| P    | odds | log odds |
| ---- | ---- | -------- |
| 0.05 | ?    | ?        |
| 0.25 | ?    | ?        |
| 0.50 | ?    | ?        |
| 0.75 | ?    | ?        |
| 0.95 | ?    | ?        |

4. *Reverse Engineering*
   Logistic model gives $\operatorname{logit}(P)=2.2$ for a certain customer profile.
   a) Convert to odds.
   b) Convert to probability.
   c) Explain what it means if another profile has logit = −2.2.

---

## 6. Key Takeaways

* **Odds**: ratio success : failure.
* **Probabilities** and odds are linked but *not* interchangeable.
* **Log‑odds** symmetrize the scale, yield (−∞, ∞) range, and appear naturally in logistic regression.
* Understanding odds/log‑odds is foundational for interpreting coefficients, likelihood ratios, and many applied statistics problems.

---

## 7. Instructor Notes / Solutions (for reference)

### Practice Answers (abbreviated)

1. a) $\text{odds}=0.30/0.70=0.429$;  b) log‑odds = −0.85;  c) Linear in predictors ⇒ easier coefficient interpretation.
2. Probability = $\frac{9}{9+2}≈0.818$.
3. Numeric confirmation: log‑odds ≈ ±2.20.

### Homework Hints

* Use odds × likelihood ratio = posterior odds.
* Odds ratio = e^{Δ(log‑odds)}.
* For table: odds = P/(1−P); log‑odds = ln(odds).


