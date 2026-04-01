
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Data entry from image
scale1_raw = [68.37, 70.81, 64.84, 67.57, 60.68, 67.11, 68.57, 65, 63.42, 64.1, 72.37, 67.55, 65.13, 66.11, 69.33, 65.05, 69.94, 62.23, 69.35]
scale2_raw = [59, 64, 61, 64, 67, 63, 62, 69, 60, 61, 62, 66, 63, 64, 64, 66, 66, 63, 63, 64, 64, 62, 64, 69, 59, 64, 63, 66, 61]
scale3_raw = [63.97, 63.49, 62.98, 62.89, 62.03, 63.85, 59.5, 63.28, 60.77, 64.97, 63.3, 62.12, 62.39, 61.57, 62.26, 61.21, 64.14, 64.26, 62.62, 62.11, 62.58, 62.59, 63.71, 64.28]
scale4_raw = [62.78, 63.56, 67.38, 55.34, 65.33, 59.28, 58.75, 59.72, 59.8, 63.3, 58.97, 62.65, 62.39, 62.9, 56, 64.43, 64.81, 64.34, 56.01, 64.8]

# Constants
WRAPPER_WEIGHT = 1.05
NET_WEIGHT_LABEL = 61.5

# Subtract wrapper weight
scale1 = np.array(scale1_raw) - WRAPPER_WEIGHT
scale2 = np.array(scale2_raw) - WRAPPER_WEIGHT
scale3 = np.array(scale3_raw) - WRAPPER_WEIGHT
scale4 = np.array(scale4_raw) - WRAPPER_WEIGHT

# Combine all data
all_data = np.concatenate([scale1, scale2, scale3, scale4])

print("=== QUESTION 2: Descriptive Statistics on Combined Data ===")
mean_val = np.mean(all_data)
std_dev = np.std(all_data, ddof=1) # Sample standard deviation
n = len(all_data)
sem = std_dev / np.sqrt(n)
# 95% Confidence Interval
ci = stats.t.interval(0.95, df=n-1, loc=mean_val, scale=sem)
print(f"Mean: {mean_val:.4f} g")
print(f"Standard Deviation: {std_dev:.4f} g")
print(f"95% Confidence Interval: {ci}")

print("\n=== QUESTION 2b: Outlier Test ===")
# Find smallest value
min_val = np.min(all_data)
print(f"Smallest Value: {min_val:.4f} g")

# IQR Method
q1 = np.percentile(all_data, 25)
q3 = np.percentile(all_data, 75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
print(f"Q1: {q1:.4f}, Q3: {q3:.4f}, IQR: {iqr:.4f}")
print(f"Lower Bound (Q1 - 1.5*IQR): {lower_bound:.4f}")
print(f"Is {min_val:.4f} < {lower_bound:.4f}? {'Yes, it is an outlier' if min_val < lower_bound else 'No, it is not an outlier'}")

# Grubb's Test (alternative, simplified check using Z-score for extreme outlier)
z_score = (min_val - mean_val) / std_dev
print(f"Z-score of smallest value: {z_score:.4f}")


print("\n=== QUESTION 2c & 2d: Plots ===")
# Histogram
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.hist(all_data, bins=10, edgecolor='black', alpha=0.7)
plt.title('Histogram of Candy Net Weights')
plt.xlabel('Net Weight (g)')
plt.ylabel('Frequency')

# Cumulative Percentage Plot (Probability Plot)
plt.subplot(1, 2, 2)
# Sort data for cumulative plot manually or use probplot
sorted_data = np.sort(all_data)
# Calculate cumulative percentage
y_axis = np.arange(1, n + 1) / n * 100
plt.plot(sorted_data, y_axis, marker='.', linestyle='none')
plt.title('Cumulative Percentage Plot')
plt.xlabel('Net Weight (g)')
plt.ylabel('Cumulative Percentage (%)')
plt.grid(True)
plt.tight_layout()
plt.savefig('candy_plots.png')
print("Plots saved to candy_plots.png")

print("\n=== QUESTION 2e: Normality Check ===")
shapiro_test = stats.shapiro(all_data)
print(f"Shapiro-Wilk Test: Statistic={shapiro_test.statistic:.4f}, p-value={shapiro_test.pvalue:.4f}")
if shapiro_test.pvalue > 0.05:
    print("Data appears to be normally distributed (p > 0.05)")
else:
    print("Data does NOT appear to be normally distributed (p < 0.05)")

print("\n=== QUESTION 3: Two-tailed t-test (Scale 1 vs Scale 2) ===")
# Comparing Scale 1 and Scale 2
t_stat, p_val = stats.ttest_ind(scale1, scale2)
print(f"Comparing Scale 1 (mean={np.mean(scale1):.2f}) and Scale 2 (mean={np.mean(scale2):.2f})")
print(f"t-statistic: {t_stat:.4f}, p-value: {p_val:.4e}")
if p_val < 0.05:
    print("There IS a statistically significant difference (p < 0.05).")
else:
    print("There IS NOT a statistically significant difference (p > 0.05).")

print("\n=== QUESTION 4: Chi-squared Goodness of Fit ===")
# Testing if data fits a normal distribution
# Bin the data
num_bins = 6 # Using a small number of bins for chi-square validity
observed_freq, bin_edges = np.histogram(all_data, bins=num_bins)
# Calculate expected frequencies for normal distribution
expected_freq = []
for i in range(num_bins):
    lower = bin_edges[i]
    upper = bin_edges[i+1]
    # CDF of upper - CDF of lower * total count
    prob = stats.norm.cdf(upper, loc=mean_val, scale=std_dev) - stats.norm.cdf(lower, loc=mean_val, scale=std_dev)
    expected_freq.append(prob * n)

# Adjust expected frequencies to sum to exactly n
expected_freq = np.array(expected_freq)
expected_freq = expected_freq * (np.sum(observed_freq) / np.sum(expected_freq))

# Simple Chi-Square calculation
chi2_stat, chi2_p = stats.chisquare(f_obs=observed_freq, f_exp=expected_freq)

# Display Table
print(f"{'Bin Range':<20} {'Observed':<10} {'Expected':<10}")
for i in range(num_bins):
    range_str = f"{bin_edges[i]:.2f} - {bin_edges[i+1]:.2f}"
    print(f"{range_str:<20} {observed_freq[i]:<10} {expected_freq[i]:<10.4f}")
print(f"Chi-Squared Statistic: {chi2_stat:.4f}, p-value: {chi2_p:.4f}")


print("\n=== QUESTION 5: Scale 3 Analysis ===")
scale3_mean = np.mean(scale3)
print(f"Scale 3 Mean (Net): {scale3_mean:.4f} g")
# One-sample t-test
# H0: mean = 61.5
# Ha: mean != 61.5 (two-tailed check first)
t_stat_3, p_val_3_two_tailed = stats.ttest_1samp(scale3, NET_WEIGHT_LABEL)
# For one-tailed: p_val / 2 if t_stat is in the direction of the alternative hypothesis.
# Question asks "statistically greater than or less than".
print(f"Target Net Weight: {NET_WEIGHT_LABEL} g")
print(f"t-statistic: {t_stat_3:.4f}, p-value (two-tailed): {p_val_3_two_tailed:.4e}")

if p_val_3_two_tailed < 0.05:
    print("The mean is statistically significantly different from 61.5g.")
    if t_stat_3 > 0:
        print("The mean is statistically GREATER than 61.5g.")
    else:
        print("The mean is statistically LESS than 61.5g.")
else:
    print("The mean is NOT statistically significantly different from 61.5g.")


print("\n=== QUESTION 6: ANOVA Analysis ===")
f_stat, anova_p = stats.f_oneway(scale1, scale2, scale3, scale4)
print(f"F-statistic: {f_stat:.4f}, p-value: {anova_p:.4e}")
if anova_p < 0.05:
    print("There IS a statistically significant difference between the four scales (p < 0.05).")
else:
    print("There IS NOT a statistically significant difference between the four scales.")
