import pandas as pd
import statsmodels.api as sm
from scipy.stats import pearsonr

# Dataset

X = [
45, 42, 44, 63, 63, 51, 59, 60, 50, 65,
65, 43, 72, 67, 66, 61, 55, 45, 31, 58,
42, 59, 60, 47, 54, 61, 62, 66, 57, 51,
55, 74, 63, 63, 46, 59, 47, 67, 57, 45,
57, 65, 45, 58, 51, 52, 70, 45, 47, 53,
57, 58, 65, 43, 45, 62, 48, 66, 63, 66,
71, 66, 60, 63, 61, 50, 55, 46, 67
]

Y = [
40, 39, 44, 58, 58, 48, 47, 49, 52,
58, 44, 61, 58, 56, 55, 42, 42, 27, 49,
28, 56, 60, 51, 47, 56, 46, 51, 63, 44,
56, 70, 54, 49, 48, 61, 41, 61, 48, 42,
52, 55, 42, 56, 54, 45, 64, 45, 55,
45, 54, 55, 42, 42, 41, 44, 55, 48, 70,
42, 59, 56, 52, 67, 47, 48, 33, 53
]

# Validate Data

print("Number of X data:", len(X))
print("Number of Y data:", len(Y))

if len(X) != len(Y):
raise ValueError("The number of X and Y observations must be equal!")

# Create DataFrame

df = pd.DataFrame({
"X": X,
"Y": Y
})

print("\nData successfully created.")
print("Number of respondents:", len(df))

# Pearson Correlation

r, p_corr = pearsonr(df["X"], df["Y"])

print("\nPearson Correlation")
print(f"r       = {r:.3f}")
print(f"Sig.    = {p_corr:.3f}")

# Simple Linear Regression

X_reg = sm.add_constant(df["X"])
model = sm.OLS(df["Y"], X_reg).fit()

# R-Square

r_squared = model.rsquared

print("\nR-Square")
print(f"R²       = {r_squared:.3f}")
print(f"R² (%)   = {r_squared * 100:.2f}%")
print(f"Other variation = {(1 - r_squared) * 100:.2f}%")

# t-Test

t_hitung = model.tvalues["X"]
sig_t = model.pvalues["X"]

print("\nt-Test")
print(f"t statistic = {t_hitung:.3f}")
print(f"Sig.        = {sig_t:.3f}")

# F-Test

f_hitung = model.fvalue
sig_f = model.f_pvalue

print("\nF-Test")
print(f"F statistic = {f_hitung:.3f}")
print(f"Sig.        = {sig_f:.3f}")

# Conclusion

print("\nConclusion")

if sig_t < 0.05:
print("t-Test: Significant (Sig. < 0.05)")
else:
print("t-Test: Not significant (Sig. >= 0.05)")

if sig_f < 0.05:
print("F-Test: Model is significant (Sig. < 0.05)")
else:
print("F-Test: Model is not significant (Sig. >= 0.05)")
