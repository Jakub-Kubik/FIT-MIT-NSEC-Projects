# ###################################################
# xkubik32 (Jan Jakub Kubik) Projekt do MSP 2021/2022
# ###################################################

from scipy.stats import shapiro, mannwhitneyu

import statsmodels.api as sm
from statsmodels.formula.api import ols

import numpy as np
import pandas as pd

from copy import copy

import matplotlib.pyplot as plt



def shapiro_test(data):
    """Perform the Shapiro-Wilk test for normality.

    The Shapiro-Wilk test tests the null hypothesis that the data was drawn from a normal distribution."""
    pvalue_x = shapiro(data['X_ms']).pvalue  # result -> 0.0219634510576725
    pvalue_y = shapiro(data['Y_ms']).pvalue  # result -> 0.03673752769827843
    print(f'pvalue of X_ms: {pvalue_x}\npvalue of Y_ms: {pvalue_y}')

    print('\n\n')

    return pvalue_x, pvalue_y

def plot_data(data):
    # line 1 points
    x1 = [x for x in range(1, 51)]
    y1 = data['X_ms']
    # plotting the line 1 points
    plt.plot(x1, y1, label = "Poskytovatel X")
    
    # line 2 points
    x2 = [x for x in range(1, 51)]
    y2 = data['Y_ms']
    # plotting the line 2 points
    plt.plot(x2, y2, label = "Poskytovatel Y")
    
    # naming the x axis
    plt.xlabel('Cislo merania')
    # naming the y axis
    plt.ylabel('Ping [ms]')
    # giving a title to my graph
    
    # show a legend on the plot
    plt.legend()
    
    # function to show the plot
    plt.show()


# shapio test + student test
def task_1():
    print('================' * 3)
    print('TASK_1')
    print('================' * 3)
    # xkubik32 - assignment number: 17
    data = {
        'X_ms': [25.75, 23.85, 25.31, 22.33, 25.06, 20.94, 24.05, 20.64, 25.87, 17.54, 25.32, 22.19, 26.69, 19.13, 24.5, 20.62, 26.24, 22.12, 27.65, 21.43, 24.53, 21.32, 24.46, 20.3, 24.91, 20.11, 24.9, 20.75, 24.2, 22.02, 25.66, 20.2, 24.9, 21.18, 25.36, 20.51, 24.58, 19.99, 28.22, 19.86, 25.97, 21.01, 25.77, 21.54, 25.67, 19.18, 24.21, 20.11, 25.69, 21.75],
        'Y_ms': [24.42, 23.08, 23.7, 23.3, 23.57, 26.79, 25.51, 25.75, 25.37, 23.68, 22.52, 24.87, 19.9, 26.77, 24.48, 25.42, 24.96, 23.28, 21.04, 25.21, 21.26, 22.77, 24.3, 23.78, 23.89, 27.14, 23.32, 25.75, 24.67, 25.74, 24.19, 21.98, 23.33, 24.62, 23.7, 23.34, 18.96, 25.28, 23.34, 24.89, 24.83, 24.71, 26.02, 25.85, 25.37, 20.47, 22.83, 25.47, 24.6, 22.77],
    }

    pvalue_x, pvalue_y = shapiro_test(data=data)

    # min 1 of 2 don't have normal distribution ->  
    if pvalue_x or pvalue_y:
        mw = mannwhitneyu(data['X_ms'], data['Y_ms'], method="asymptotic", alternative='two-sided')
        print(f'H0, HA1: pvalue={mw.pvalue}')
        mw = mannwhitneyu(data['X_ms'], data['Y_ms'], method="asymptotic", alternative='greater')
        print(f'H0, HA2: pvalue={mw.pvalue}')
        mw = mannwhitneyu(data['X_ms'], data['Y_ms'], method="asymptotic", alternative='less')
        print(f'H0, HA3: pvalue={mw.pvalue}')
        print('\n\n')
    
    plot_data(data)

# 2 factor ANOVA
def task_2():
    print('================' * 3)
    print('TASK_2')
    print('================' * 3)
    #create data
    df = pd.DataFrame({
        'faktor_1': [
            'rano', 'rano', 'rano', 'rano', 'obed', 'obed', 'obed', 'vecr', 'vecr', 'vecr',
            'rano', 'rano', 'rano', 'rano', 'obed', 'obed', 'obed', 'vecr', 'vecr', 'vecr', 'vecr',
            'rano', 'rano', 'rano', 'obed', 'obed', 'obed', 'obed', 'vecr', 'vecr', 'vecr',
            'rano', 'rano', 'obed', 'obed', 'vecr', 'vecr', 'vecr', 'vecr', 'vecr',
        ], 
        'faktor_2': [
            'ticho', 'ticho', 'ticho', 'ticho', 'ticho', 'ticho', 'ticho', 'ticho', 'ticho', 'ticho',               
            'hudba', 'hudba', 'hudba', 'hudba', 'hudba', 'hudba', 'hudba', 'hudba', 'hudba', 'hudba', 'hudba',
            'hluk_', 'hluk_', 'hluk_', 'hluk_', 'hluk_', 'hluk_', 'hluk_', 'hluk_', 'hluk_', 'hluk_',
            'krik_', 'krik_', 'krik_', 'krik_', 'krik_', 'krik_', 'krik_', 'krik_', 'krik_',                     
        ],
        'riesenie_min': [
            6, 8, 11, 7, 8, 13, 7, 7, 8, 6,           # added on pos `4` number 7
            7, 8, 12, 10, 5, 11, 7, 6, 8, 16, 15,
            8, 7, 20, 10, 17, 11, 13, 12, 17, 30,     # added on pos `10` number 30
            13, 21, 14, 45, 13, 17, 15, 22, 18,           # added on pos `4` number 45
        ]
    })
    # view all data
    print(df)

    model = ols('riesenie_min ~ C(faktor_1) + C(faktor_2) + C(faktor_1):C(faktor_2)', data=df).fit()    
    result_table = sm.stats.anova_lm(model, typ=3)

    print(result_table)
    print('\n\n')


def task_3():
    print('================' * 3)
    print('TASK_3')
    print('================' * 3)
    aktivita = {
        'žiadna': 0,
        '1x': 0,
        '2x': 0,
        '3x': 0, 
        '>3x': 0, 
    }

    data = {
        '<18': copy(aktivita),
        '<20': copy(aktivita),
        '<23': copy(aktivita),
        '<25': copy(aktivita),
        '<35': copy(aktivita),
        '<45': copy(aktivita),
        '>45': copy(aktivita),
    }

    df = pd.read_csv('task_3.csv')
    for x, y in df.iterrows():
        age = ''.join(y[1].split()[:2])
        sport_times = ''.join(y[2].split()[:1])
        data[age][sport_times] += 1
    

    for k, v in data.items():
        print(k, v)

def main():
    task_1()

    task_2()

    task_3()


if __name__ == "__main__":
    main()
