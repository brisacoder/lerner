# Lesson Plan: Odds Ratio & Log Odds Ratio (Log OR)

## 1. Overview

**Goal:** Help students master the *odds ratio* (OR)—a comparison of two odds—and its symmetric companion, the *log odds ratio* (log OR). This bridges the earlier lesson on odds/log‑odds to real‑world association testing (e.g., disease vs. exposure) and prepares them for logistic‑regression output.

**Learner Outcomes**

* Construct 2 × 2 contingency tables and compute OR & log OR.
* Interpret OR > 1, OR < 1, and log OR symmetry.
* Perform and interpret Fisher’s Exact, Chi‑Square, and Wald tests.
* Simulate the sampling distribution of log OR and visualise it.
* Write Python code (pandas + matplotlib + SciPy) that automates the above.

---

## 2. Warm‑Up Prompt (5 min)

> *“A study reports an odds ratio of **3.2** that smokers develop cough compared with non‑smokers.*
> a) What does 3.2 mean in plain English?
> b) Is 3.2 a probability?”

Discuss to surface misconceptions that OR is *not* a probability and can exceed 1.

---

## 3. Core Content

### 3.1 Definitions & Formulae (15 min)

| Term               | Symbol          | Formula                    | Notes                |
| ------------------ | --------------- | -------------------------- | -------------------- |
| **Odds (group i)** | $\text{odds}_i$ | $\dfrac{a_i}{b_i}$         | successes / failures |
| **Odds Ratio**     | $\text{OR}$     | $\dfrac{a_1/b_1}{a_0/b_0}$ | ratio of two odds    |
| **Log OR**         | $\log\text{OR}$ | $\ln(\text{OR})$           | symmetric around 0   |

Where, for a 2 × 2 table…

|                  | **Outcome = 1** | **Outcome = 0** |
| ---------------- | --------------- | --------------- |
| **Exposure = 1** | $a_1$           | $b_1$           |
| **Exposure = 0** | $a_0$           | $b_0$           |

*Interpretation*

* **OR = 1** → No association.
* **OR > 1** → Outcome more likely with exposure.
* **OR < 1** → Outcome less likely with exposure.
* **log OR > 0 / < 0** mirror OR > 1 / < 1 but symmetric (−∞ ↔ ∞).

---

### 3.2 Worked Example – Mutated Gene × Cancer (20 min)

|            | **Cancer +** | **Cancer −** | **Total** |
| ---------- | ------------ | ------------ | --------- |
| **Gene +** | 23           | 117          | 140       |
| **Gene −** | 6            | 210          | 216       |
| **Total**  | 29           | 327          | 356       |

* $\text{odds}_{\text{Gene+}}=23/117=0.197$
* $\text{odds}_{\text{Gene−}}=6/210=0.029$
* **OR** = 0.197 / 0.029 ≈ **6.88**
* **log OR** = ln 6.88 ≈ **1.93**.

> **Interpretation:** Odds of cancer are \~6.9 × higher when the mutation is present.

---

### 3.3 Significance Tests (15 min)

1. **Fisher’s Exact** – exact p‑value for 2 × 2 tables; no large‑sample assumptions.
2. **Chi‑Square** – large‑sample approximation; optional Yates continuity correction.
3. **Wald z‑Test** – uses normality of log OR to test $H_0:\text{OR}=1$ and build confidence intervals.

*Wald formulae*

* $SE_{\log\text{OR}} = \sqrt{\tfrac1{a_1}+\tfrac1{b_1}+\tfrac1{a_0}+\tfrac1{b_0}}$
* $z = \dfrac{\log\text{OR}}{SE}$
* $\text{CI}_{95\%} = \exp\big(\log\text{OR} \pm 1.96\,SE\big)$

---

## 4. Guided Practice (10 min)

Using the table above, students should manually verify OR, log OR, z‑score, and CI. Then predict whether p < 0.05 before looking at code results.

---

## 5. Independent Exercises (Homework)

1. **Medication × Side‑Effect** – Dataset: 125/1000 medicated report nausea vs 60/1000 placebo. Compute OR, log OR, 95 % CI, and test significance with Chi‑Square and Wald.
2. **Marketing A/B** – Ad A: 75 clicks / 925 misses; Ad B: 90 / 910. Calculate OR, interpret, and decide which ad is better.
3. **Reverse Engineering** – A paper lists log OR = −0.69 (SE = 0.22).
   a) Recreate OR and CI.
   b) What does the sign imply?
   c) Compute the Wald p‑value.

---

## 6. Python Walk‑Through

> **Run this end‑to‑end script in a notebook or Python shell.**

```python
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import fisher_exact, chi2_contingency, norm

# ---------------------------
# Build table via pandas
# ---------------------------
obs_df = pd.DataFrame({"Cancer+": [23, 6], "Cancer-": [117, 210]},
                     index=["Gene+", "Gene-"])
print("Observed 2x2 table:\n", obs_df, "\n")

# Raw counts
a1, b1 = obs_df.loc["Gene+", ["Cancer+", "Cancer-"]]
a0, b0 = obs_df.loc["Gene-", ["Cancer+", "Cancer-"]]

# Odds & OR
odds_gene = a1 / b1
odds_nogene = a0 / b0
OR = odds_gene / odds_nogene
logOR = np.log(OR)
print(f"OR = {OR:.2f},  log(OR) = {logOR:.2f}\n")

# Significance tests
_, p_fisher = fisher_exact(obs_df.values)
chi2, p_chi2, _, _ = chi2_contingency(obs_df.values, correction=True)
SE = np.sqrt(1/a1 + 1/b1 + 1/a0 + 1/b0)
z = logOR / SE
p_wald = 2 * (1 - norm.cdf(abs(z)))
CI_low, CI_high = np.exp([logOR - 1.96*SE, logOR + 1.96*SE])
print(f"Fisher p-value : {p_fisher:.6f}")
print(f"Chi2  p-value  : {p_chi2:.6f}")
print(f"Wald  p-value  : {p_wald:.6f}")
print(f"95% CI (OR)   : [{CI_low:.2f}, {CI_high:.2f}]\n")

# ---------------------------
# Simulate null distribution of log OR
# ---------------------------
log_or_null = []
rng = np.random.default_rng(0)
for _ in range(10_000):
    n = rng.integers(300, 401)
    cancer = rng.random(n) < 0.08      # prevalence 8%
    gene   = rng.random(n) < 0.39      # mutation frequency 39%
    a = np.sum(gene & cancer)
    b = np.sum(gene & ~cancer)
    c = np.sum(~gene & cancer)
    d = np.sum(~gene & ~cancer)
    if min(a,b,c,d) == 0:
        continue  # skip degenerate
    log_or_null.append(np.log((a/b)/(c/d)))
log_or_null = np.array(log_or_null)

# Plot
plt.figure(figsize=(8,5))
plt.hist(log_or_null, bins=40, density=True, alpha=0.6, label="Null log(OR)")
xs = np.linspace(log_or_null.min(), log_or_null.max(), 400)
plt.plot(xs, norm.pdf(xs, 0, log_or_null.std()), 'r-', label="Normal PDF")
plt.axvline(logOR, color='k', ls='--', label=f"Observed log(OR) = {logOR:.2f}")
plt.title("Sampling Distribution of log(OR) Under H₀")
plt.xlabel("log(OR)")
plt.ylabel("Density")
plt.legend(); plt.tight_layout(); plt.show()
```

> **What students should notice**: the simulated distribution is roughly normal, centred at 0, validating the Wald z‑test; the observed log OR (≈ 1.93) lies far in the tail, consistent with tiny p‑values.

```python
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.contingency_tables import Table2x2

# Build DataFrame (same as SciPy block)
obs_df = pd.DataFrame({"Cancer+": [23, 6], "Cancer-": [117, 210]},
                     index=["Gene+", "Gene-"])
ct = Table2x2(obs_df.values)  # pass ndarray but keep pandas for display
print(ct.summary())           # automatic prettier summary

# OR, CI, logOR
print("OR        :", ct.oddsratio)
print("95% CI    :", ct.oddsratio_confint())
print("log(OR)   :", ct.log_oddsratio)

# p‑values (Fisher, Chi‑Square, Wald)
print("Fisher p  :", ct.fisher_exact(method="table")[1])
print("Chi2  p   :", ct.test_nominal_association().pvalue)
print("Wald  p   :", ct.log_oddsratio_pvalue())
```

---

## 7. Key Takeaways

* **Odds Ratio** quantifies comparative odds between two groups; **log OR** makes interpretation symmetric (& math nicer).
* OR = 1 ↔ no effect; log OR = 0 ↔ no effect.
* Fisher, Chi‑Square, and Wald all test $H_0: \text{OR}=1$. Field conventions decide which to report; it’s good practice to check more than one when results hover near p = 0.05.
* Simulation illustrates why log OR is (approximately) normally distributed for moderate cell counts.
