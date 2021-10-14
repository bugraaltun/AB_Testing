#################################################################
##################### AB TESTING ################################
#################################################################


#####################################
# Importing required libraries
#####################################


import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel("Datasets/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("Datasets/ab_testing.xlsx", sheet_name="Test Group")
df_control.isnull().sum()
df_test.isnull().sum()

df_control.dtypes
df_test.dtypes

####################################################
# AB Testing (Independent Two Sample T Test)
####################################################

# It is used when it is desired to make a comparison between the mean of two groups.

#1. Assumption Check
# - 1. Normality Assumption
# - 2. Variance Homogeneity
# 2. Implementation of the Hypothesis
# - 1. Independent two-sample t-test if assumptions are met (parametric test)
# - 2. Mannwhitneyu test if assumptions are not met (non-parametric test)
# Note:
# - Number 2 directly if normality is not achieved. If variance homogeneity is not provided, an argument is entered for number 1.
# - It can be useful to perform outlier analysis and correction before normality analysis.


#################################
# Is there a statistically significant difference between maximumbidding and averagebidding in terms of yield?
##################################

df_control.describe().T
df_test.describe().T
#the mean and median of both are very close to each other

#ad views
df_control["Click"].mean() / df_control["Impression"].mean()
df_test["Click"].mean() / df_test["Impression"].mean()

#click-to-buy rates
df_control["Purchase"] / df_control["Click"]
df_test["Purchase"].mean() / df_test["Click"].mean()

#1. Assumption Check
# - 1. Normality Assumption
# - 2. Variance Homogeneity

############################
# Normality Assumption
############################

# H0: Assumption of normal distribution is provided.
# H1:..not provided.
################################################ ###############################
# If p-value < 0.05 to HO RED.
# 0.05 H0 CANNOT BE REJECTED unless p-value <.

test_stat, pvalue = shapiro(df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = 0.9589, p-value = 0.1541
#HO cannot be rejected

test_stat, pvalue = shapiro(df_control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
##HO cannot be rejected
#Test Stat = 0.9773, p-value = 0.5891

############################
# Variance Homogeneity
############################

# H0: Variances are Homogeneous
# H1: Variances Are Not Homogeneous


test_stat, pvalue = levene(df["Purchase"].dropna(), df["Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#H0 cannot be rejected, so variances are homogeneous

"""
We can say that the results are acceptable because when I describe it above, 
the mean and medians are very close so the results make sense.
"""
###################
# Application of the hypothesis: Independent two-sample t-test (parametric test)
###################

# H0: M1 = M2 => No difference between purchase averages
# H1: M1 != M2 => There is difference between purchase averages

test_stat, pvalue = ttest_ind(df_control["Purchase"], df_test["Purchase"], equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#Test Stat = -0.9416, p-value = 0.3493
#We can't reject #H0 so there is no statistical difference between purchasing averages.
"""

We can say that the results are acceptable because when I described above, the mean and medians are interconnected.
we can see how close it is, so the normality assumption and variance homogeneity assumption results are reasonable.
It can also be accepted that there is no statistically significant difference between the results, because the sales averages are also a little close to each other.
"""
"""
As a test, I first used the normality assumption test, then I used the variance homogeneity test since the assumptions were provided.
Since the variances were homogeneous, I used the independent two-sample t-test.
"""

# Is there any significant difference see ads and click through rates.
df_control["Click"].mean() / df_control["Impression"].mean()
df_test["Click"].mean() / df_test["Impression"].mean()

# H0: Assumption of normal distribution is provided.
# H1:..not provided.
######################################################################

test_stat, pvalue = shapiro(df_control["Click"] / df_control["Impression"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df_test["Click"] / df_test["Impression"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# H0 rejected

####################
# Mannwhitneyu Test
####################
# H0 = there is no statistically significant difference between seeing and clicking the ads
# H1 = ...has
test_stat, pvalue = mannwhitneyu(df_control["Click"] / df_control["Impression"], df_test["Click"] / df_test["Impression"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# there is difference between seeing and clicking the ads

df_control["Click"].mean() / df_control["Impression"].mean()
df_test["Click"].mean() / df_test["Impression"].mean()
# When we compare the conversion rates,
# we see that the average (click-through / ad view) rate of the old system is higher and there is a statistical difference between them.

##############################################
# Is there a statistically significant difference between the two systems in terms of clicking on ads and earning income?
##############################################

# H0: Assumption of normal distribution is provided.
# H1:..not provided.
#################################################################################


test_stat, pvalue = shapiro(df_control["Earning"] / df_control["Click"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df_test["Earning"] / df_test["Click"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#H0 rejected. Assumption of normal distribution is not provided.

##################
#Mannwhitneyu Test
##################

# H0 = There is no statistically significant difference between the two systems in terms of clicking ads and earning
# H1 = ...has

test_stat, pvalue = mannwhitneyu(df_control["Earning"] / df_control["Click"], df_test["Earning"] / df_test["Click"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#h0 is rejected.
# Click on the ads and choose between the return rates. there is a significant difference.
df_control["Earning"].mean() / df_control["Click"].mean()
df_test["Earning"].mean() / df_test["Click"].mean()


df_control.describe().T
df_test.describe().T

# When we compare the ratios, we can say that the result is correct.
# The rate of return on clicks of the new system is almost twice that of the old system.
#When we consider only the average of earnings, we can clearly say that the second system makes a difference.



"""
According to the results, we could not find a statistical difference between the purchases of the old system and the new system after the clicked ads, 
and the sales averages are close to each other. 
However, we have statistically observed that the old system works a little better than the new system in terms of conversion.
At the same time, the earnings per click statistics of the new system compared to the old system are almost twice that of the old system. 
When we consider not only earnings per click but also earnings rates, 
we can clearly say that the second system makes a difference. 
Considering all this, we can test and observe the purchases after the clicked ads for a while, 
but since the second system is clearly ahead of the earnings rate, 
I see the second system one step ahead because although the conversion rate is better in the first system, 
the earning is clearly in the second system it gave better results.
"""