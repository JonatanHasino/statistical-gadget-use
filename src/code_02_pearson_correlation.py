import pandas as pd
from scipy.stats import pearsonr

# Dataset

data = {
"X": [
45, 42, 44, 63, 63, 51, 59, 60, 50, 65,
65, 43, 72, 67, 66, 61, 55, 45, 31, 58,
42, 59, 60, 47, 54, 61, 62, 66, 57, 51,
55, 74, 63, 63, 46, 59, 47, 67, 57, 45,
57, 65, 45, 58, 51, 52, 70, 45, 47, 53,
57, 58, 65, 43, 45, 62, 48, 66, 63, 66,
71, 66, 60, 63, 61, 50, 55, 46, 67
],
"Y": [
40, 39, 44, 58, 58, 48, 47, 49, 47, 52,
58, 44, 61, 58, 56, 55, 42, 42, 27, 49,
28, 56, 60, 51, 47, 56, 46, 51, 63, 44,
56, 70, 54, 49, 48, 61, 41, 61, 48, 42,
52, 55, 42, 56, 54, 45, 64, 45, 55,
45, 54, 55, 42, 42, 41, 44, 55, 48, 70,
42, 59, 56, 52, 67, 47, 48, 33, 53
]
}

df = pd.DataFrame(data)

# Pearson Correlation

r, p = pearsonr(df["X"], df["Y"])

# Descriptive Statistics

print("Number of observations =", len(df))
print("Mean X =", df["X"].mean())
print("Mean Y =", df["Y"].mean())
print("SD X =", df["X"].std())
print("SD Y =", df["Y"].std())

# Correlation Results

print("Pearson r =", r)
print("p-value =", p)
