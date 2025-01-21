import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from scipy.optimize import curve_fit
from scipy.stats import stats
from scipy.stats import chisquare

# Use with "counts"
def function1(x, a):
    y = a/(x)**2
    return y

# Use with "integrals"
def function2(x, a, b):
    y = a/(x + b)**2
    return y

files = []
if (len(sys.argv) != 1):
    for i in range(1, len(sys.argv)):
        if (sys.argv[i].endswith(".txt")):
            if (i == 1):
                background = sys.argv[i]
            else:
                files.append(sys.argv[i])
        else:
            print("Incorrect format.")
            sys.exit(1)
else:
    print("Incorrect format.")
    sys.exit(1)

live_times = [43574, 240.46, 240.54, 240.64, 240.49, 240.58, 180, 180, 180, 181, 180]
distances = [0.0, 1.4, 2.4, 3.4, 4.5, 15.65, 16.2, 16.7, 17.2, 17.9]
counts = [19287, 18602, 17501, 16833, 15401]
integrals = []
summation = 0
lower_channel = 1060
upper_channel = 1390
indexer = 1

df_back = pd.read_csv(background, sep = "\r\n", header = None, engine = "python")
df_back[0] = df_back[0].apply(lambda x: x.replace("\t", " "))
df_back[["Channel", "Energy", "Count"]] = df_back[0].str.split(" ", n = 2, expand = True)
df_back.drop([0], axis = 1, inplace = True)
df_back.set_index("Channel", inplace = True)

for f in files:
    try:
        df = pd.read_csv(f, sep = "\r\n", header = None, engine = "python")
        df[0] = df[0].apply(lambda x: x.replace("\t", " "))
        df[["Channel", "Energy", "Count"]] = df[0].str.split(" ", n = 2, expand = True)
        df.drop([0], axis = 1, inplace = True)
        df.set_index("Channel", inplace = True)
        # df_back["Count"] = df_back["Count"].astype("float") / float(live_times[indexer])
        df_back["Count"] = df_back["Count"].astype("float") * (float(live_times[indexer]) / float(live_times[0]))
        for i in range(len(df.index)):
            if ((float(df.iloc[i, 1]) - float(df_back.iloc[i, 1])) < 0):
                df.iloc[i, 1] = 0
            else:
                df.iloc[i, 1] = float(df.iloc[i, 1]) - float(df_back.iloc[i, 1])
        for i in range(lower_channel, upper_channel + 1):
            summation += float(df.iloc[i, 1])
        integrals.append(int(summation))
        indexer += 1
        summation = 0
    except FileNotFoundError:
        print("Couldn't find file.")
        sys.exit(1)

def cs(n, y):
    return chisquare(n, np.sum(n)/np.sum(y) * y)
        
parameters, covariance = curve_fit(function2, distances, integrals, p0 = [900000, 1])
print(parameters)
fit_x = np.arange(min(distances), max(distances) + 1.9889, 1.9889)
fit_y = function2(fit_x, *parameters)
# print(integrals, fit_y)
print(cs(integrals, fit_y))
# chi_square_test_statistic, p_value = stats.chisquare(integrals, fit_y)
# print("chi_square_test_statistic is : " + str(chi_square_test_statistic))
# print("p_value : " + str(p_value))
'''
residuals = integrals - fit_y
ss_res = np.sum(residuals**2)
ss_tot = np.sum((integrals - np.mean(integrals))**2)
r_squared = 1 - (ss_res / ss_tot)
print(r_squared)
'''
plt.scatter(distances, integrals, color = "b", label = "Data")
plt.plot(fit_x, fit_y, color = "y", label = "Fit")
# plt.plot(distances, integrals, fit_x, fit_y);
plt.xlabel("Distance [cm]")
plt.ylabel("Integrated Count")
plt.title("Integrated Count vs. Distance for Cs-137 Gamma Spectrum")
plt.legend()
plt.show()
'''
# Chi-Square Goodness of Fit Testa)

# chi square test statistic and p value

# find Chi-Square critical value
# print(stats.chi2.ppf(1-0.05, df=6))

parameters, covariance = curve_fit(function1, distances, counts)
fit_x = np.arange(min(distances), max(distances) + 0.5625, 0.5625)
fit_y = function1(fit_x, *parameters)
'''
'''
residuals = counts - fit_y
ss_res = np.sum(residuals**2)
ss_tot = np.sum((counts - np.mean(counts))**2)
r_squared = 1 - (ss_res / ss_tot)
print(r_squared)
'''
'''
plt.plot(distances, counts, fit_x, fit_y);
plt.xlabel("Distance [cm]")
plt.ylabel("Integrated Count")
plt.title("Integrated Count vs. Distance for Cs-137 Gamma Spectrum")
plt.show()
'''
