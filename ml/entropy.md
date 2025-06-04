# Entropy – Measuring Expected Surprise

## 1. Overview

**Goal:** Give learners an intuitive and practical grasp of entropy as “expected surprise,” starting from probability → surprise → entropy. We reuse the coin‑flip and chicken‑pen examples from StatQuest and add hands‑on Python exercises (pandas + matplotlib + SciPy/Statsmodels).

**Learning Objectives**

* Define *surprise* for an event and compute it with log‑inverse probability.
* Derive entropy as the expected value of surprise.
* Calculate entropy for biased coins and categorical distributions.
* Interpret entropy as a measure of class impurity (decision trees) or uncertainty.
* Code entropy, information gain, and a simple decision‑tree split in Python.

---

## 2. Warm‑Up Question (5 min)

> “If a coin comes up heads 100 % of the time, how *surprised* will you be on the next flip? How large do you expect its entropy to be compared with a fair coin?”

Expected answer: zero surprise, zero entropy vs 1 bit for fair coin.

---

## 3. From Probability to Surprise (10 min)

### 3.1 Intuition (Chicken Pens)

* **Area A**: 6 orange + 1 blue → picking orange unsurprising.
* **Area B**: 10 blue + 1 orange → picking blue unsurprising.
* **Area C**: 5 blue + 5 orange → either colour equally surprising.

### 3.2 Formula for Surprise

To capture “low probability ⇒ high surprise” and ensure 0 surprise when probability = 1, define
$\boxed{\text{surprise}(x) = -\log_2 p(x)}$
Equivalent to log of inverse probability.

> *Note:* Base‑2 gives “bits” of surprise; any base works with a scale factor.

---

## 4. Expected Surprise ⇒ Entropy (15 min)

For discrete outcomes $x \in \{x_1,\dots,x_k\}$ with probabilities $p(x)$:

$\boxed{H(X)=\mathbb E[\text{surprise}] = -\sum_{i=1}^k p(x_i)\,\log_2 p(x_i)}$

Interpretation: average bits needed to encode/outcome, impurity measure, “information content.”

### 4.1 Biased Coin Example (90 % heads, 10 % tails)

| Outcome     | $p$ | surprise (bits)    | contribution $p·\text{surprise}$ |
| ----------- | --- | ------------------ | -------------------------------- |
| Heads       | 0.9 | $-\log_2 0.9≈0.15$ | 0.135                            |
| Tails       | 0.1 | $-\log_2 0.1≈3.32$ | 0.332                            |
| **Entropy** |     |                    | **0.467 bits**                   |

### 4.2 Chicken Pens Entropy

Compute $H_A≈0.59$, $H_B≈0.44$, $H_C=1.0$. Highest when classes equal → maximum uncertainty.

---

## 5. Coding Section (live demo)

### 5.1 Utility Function

```python
import numpy as np
def entropy(p):
    """p: 1‑D array‑like of probabilities (will be normalized). Returns H in bits."""
    p = np.asarray(p, dtype=float)
    p = p[p > 0]           # drop zeros to avoid log(0)
    return -(p * np.log2(p)).sum()
```

### 5.2 Quick Checks

```python
print(entropy([0.5, 0.5]))      # 1.0 bit
print(entropy([0.9, 0.1]))      # ≈0.468 bit
```

### 5.3 Plot Entropy vs Bias (SciPy optional)

```python
import matplotlib.pyplot as plt
ps = np.linspace(0.001, 0.999, 300)
H = [entropy([p, 1-p]) for p in ps]
plt.figure(figsize=(6,4))
plt.plot(ps, H)
plt.title("Entropy of a Biased Coin")
plt.ylabel("H(bits)"); plt.xlabel("p(heads)")
plt.axvline(0.5, ls='--', color='gray');
plt.show()
```

### 5.4 Information Gain Exercise (Decision‑Tree Split)

```python
import pandas as pd
from statsmodels.stats import contingency_tables as ct

data = pd.DataFrame({
    "Colour": ["O","O","O","B","B","B","B","B","O","O"],
    "Label" :  [1,1,1,0,0,0,0,0,1,1]  # 1=Yes, 0=No
})
# Compute entropy before split
p_root = data['Label'].value_counts(normalize=True)
H_root = entropy(p_root)

# Split on colour
infos = {}
for colour, subset in data.groupby('Colour'):
    p = subset['Label'].value_counts(normalize=True)
    infos[colour] = entropy(p) * len(subset)/len(data)
H_after = sum(infos.values())
info_gain = H_root - H_after
print(f"Info gain by splitting on Colour: {info_gain:.3f} bits")
```

---

## 6. New Coding Exercises (Homework)

### Exercise 1 – **Entropy Table**

Create a DataFrame of three biased coins with p(heads)=0.2, 0.5, 0.8. Compute their entropy and plot a bar chart.

*Hints:* Use `pandas.DataFrame` plus `apply` to call your `entropy` function; use `matplotlib` bar plot.

### Exercise 2 – **Mutual Information**

Generate a 2 × 2 table of counts:

```python
import numpy as np
np.random.seed(0)
ctab = np.random.randint(20, 80, size=(2,2))
```

1. Compute row/col probabilities $p(x,y)$.
2. Compute $I(X;Y) = \sum p(x,y)\log_2 [p(x,y)/(p(x)p(y))].$
3. Verify result using `sklearn.metrics.mutual_info_score` (if available) or manual SciPy calculation.

### Exercise 3 – **Entropy‑Based Split for Numeric Threshold**

Given a 1‑D array `x` and binary labels `y`, write a function that scans possible split thresholds on `x` and returns the threshold with maximum information gain. Test on a synthetic Gaussian mixture and visualise `info_gain` vs threshold.

*Hints:* Sort unique `x`, loop, keep left/right subsets; use your `entropy` to compute info gain; plot curve with `matplotlib`.

---

## 7. Common Misconceptions

1. **Entropy = randomness:** It actually measures *expected* uncertainty, not randomness itself.
2. **Low probability means high entropy:** Only if the event probability is *spread out*. A sure rare event (prob≈0 or 1) has low entropy because outcome is certain.
3. **Log base matters:** Base only sets units (bits, nats); ordering and relative comparisons unchanged.

---

## 8. Key Takeaways

* *Surprise* $=-\log p$ quantifies how unexpected an outcome is.
* *Entropy* is the average surprise: $H(X)=-\sum p(x)\log p(x).$
* Maximum entropy occurs with uniform distribution; entropy drops as distribution becomes skewed.
* Entropy underpins decision‑tree splits, mutual information, KL divergence, cross‑entropy loss.
* In code, entropy is a one‑liner with numpy; combine with pandas for categorical data and matplotlib for visual insight.
