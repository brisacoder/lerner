# Lesson Plan: Understanding Expected Value

## 1. Overview

**Goal:** Teach learners how to compute and interpret the *expected value* (EV) of a discrete random variable using intuitive, real‑world betting examples.

**By the end of this lesson students will be able to:**

* Define expected value in their own words.
* Compute EV for simple discrete scenarios.
* Explain why EV represents a long‑run average gain or loss.
* Translate word problems into EV formulas (including σ‑notation).
* Critically evaluate whether a bet is favorable based on its EV.

---

## 2. Warm‑Up: The Statland Story

> *Set the scene:* “We arrive in **Statland**, where our friend **Statsquatch** wants to bet on whether the next person we meet has heard of the 1990 cult film ***Troll 2***.”

### Population Data

| Group                            | Count   | Probability            |
| -------------------------------- | ------- | ---------------------- |
| Heard of ***Troll 2***           | 37      | $\frac{37}{213}=0.17$  |
| **Never** heard of ***Troll 2*** | 176     | $\frac{176}{213}=0.83$ |
| **Total**                        | **213** | 1.00                   |

---

## 3. Example 1 – A Fair Dollar Bet

Statsquatch proposes:

> “I’ll wager **\$1** that the next person **has** heard of *Troll 2*. If I’m wrong, **you** win \$1.”

### 3.1 Outcomes Table (One Bet)

| Scenario                        | Probability | Payout to *You* ($x$) |
| ------------------------------- | ----------- | --------------------- |
| Person *has heard* of *Troll 2* | $0.17$      | $-1$ (you lose \$1)   |
| Person *has NOT heard*          | $0.83$      | $+1$ (you win \$1)    |

### 3.2 Calculating Expected Value

**Definition (discrete):**

$$
\operatorname{E}[X]=\sum_{i} p_i\,x_i
$$

where $x_i$ are outcomes and $p_i$ their probabilities.

Plugging in the values:

$$
\operatorname{E}[\text{Bet}] = (0.17)(-1) + (0.83)(+1) = -0.17 + 0.83 = \boxed{0.66}
$$

**Interpretation:** On average, you gain **\$0.66 per bet** over many repetitions, even though each *individual* bet wins or loses exactly \$1.

### 3.3 Long‑Run Perspective (100 Bets)

* **Expected wins:** $0.83\times100\approx83$ → **\$83**
* **Expected losses:** $0.17\times100\approx17$ → **–\$17**
* **Net:** \$83 – \$17 = **\$66**
* **Per‑bet average:** $$\frac{66}{100}=\$0.66$$ (matches EV above).

> **Key Point:** Multiplying and then dividing by the same number of trials (100) cancels out, reinforcing that EV is a *per‑trial* measure.

---

## 4. Example 2 – An Unbalanced Bet

Statsquatch ups the ante:

> “Because few people know the film, **I’ll pay you \$10** if they *have* heard of *Troll 2*. If they haven’t, **you pay me \$1**.”

### 4.1 Outcomes Table

| Scenario           | Probability | Payout to *You* ($x$) |
| ------------------ | ----------- | --------------------- |
| Heard of *Troll 2* | $0.17$      | **+10**               |
| Not heard          | $0.83$      | **–1**                |

### 4.2 Expected Value

$$
\operatorname{E}[X]= (0.17)(10) + (0.83)(-1)=1.70 - 0.83 = \boxed{0.87}
$$

**Interpretation:** Average profit is **\$0.87 per bet**. The larger upside when you win more than offsets the frequent \$1 losses.

> **Conclusion:** Statsquatch is a *very* poor gambler. You should gladly accept the wager if allowed many rounds.

---

## 5. General Formula & Notation Cheat‑Sheet

| Symbol                                                                | Meaning                                 |
| --------------------------------------------------------------------- | --------------------------------------- |
| $X$                                                                   | Random variable representing the payout |
| $x_i$                                                                 | A specific outcome of $X$               |
| $p_i$                                                                 | Probability of outcome $x_i$            |
| $\displaystyle\operatorname{E}[X]=\sum_{i} p_i x_i$                   | Discrete expected value                 |
| $\displaystyle\operatorname{E}[X]=\int_{-\infty}^{\infty} x f(x)\,dx$ | Continuous version (preview)            |

---

## 6. Common Misconceptions

1. **“EV tells me what will happen on the next trial.”**
   → **Reality:** EV is an average over *many* trials; single outcomes still vary.
2. **“Positive EV guarantees profit.”**
   → You need enough repetitions for the Law of Large Numbers to manifest.
3. **“If EV is positive, risk doesn’t matter.”**
   → Variance/standard deviation quantify risk; EV alone ignores volatility.

---

## 7. Guided Practice

1. **Reverse the stakes:** What payout from Statsquatch (instead of \$10) would make the second bet *fair* (EV = 0)?
2. **Alternative universe:** In a town where 60 % have seen *Troll 2*, redo Example 1. Is the bet still favorable?
3. **Three‑outcome game:** Suppose a die roll pays \$5 for a 6, \$1 for 3–5, and –\$2 for 1–2. Compute the EV.

*Solutions provided in the Teaching Notes section.*

---

## 8. Extension (for next lesson)

* Moving from discrete to **continuous** variables: EV via integrals.
* Applications to insurance premiums, stock pricing, and queueing theory.

---

## 9. Summary & Key Takeaways

* **Expected value** is the long‑run average outcome of a random process.
* Formula: $\operatorname{E}[X]=\sum p_i x_i$ (discrete).
* Positive EV bets are favorable *in the long run*.
* Always pair EV with variance to assess both reward and risk.

---

## 10. Teaching Notes (Instructor‑Only)

### Practice 1 Solution

Set EV to 0: $10p - 1(1-p)=0 \Rightarrow p=\tfrac{1}{11} \approx 0.09$.

### Practice 2 Solution

With $p=0.60$ for “heard”, EV = $0.60(-1)+0.40(+1)=-0.20$ → *Don’t* take the bet.

### Practice 3 Solution

$\operatorname{E}[X]=\tfrac16(5)+\tfrac36(1)+\tfrac26(-2)=0.83\,\text{dollars}.$
