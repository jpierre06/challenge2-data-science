from typing import Literal
import jupyterlab
import ipykernel

import pandas as pd
import numpy as np
from scipy import stats

from ydata_profiling import ProfileReport


def print_notebook_versions():
    print(f"JupyterLab: {jupyterlab.__version__}\n")
    print(f"ipykernel: {ipykernel.__version__}")


def count_zero(array:np.array):
    '''Counts the number of zeros in a numpy array.'''
    
    count = np.size(array) - np.count_nonzero(array)
    return count


def mode_limits(list_values: list, max_mode=True):
    '''Calculates the mode of a list of values, returning the maximum or minimum mode value.'''

    mode_values = mode_lists(pd.Series.mode(list_values))
    if max_mode:
        mode_values = np.max(mode_values)
    else:
        mode_values = np.min(mode_values)
    return mode_values


def mode_lists(list_values: list):
    mode_values = list(pd.Series.mode(list_values))
    return mode_values


def mode(list_values:list, count_mode=False):
    mode_value = stats.mode(list_values, keepdims=False)
    if count_mode:
        mode_value = mode_value[1]
    else:
        mode_value = mode_value[0]
    return mode_value


def mode_count(list_values:list):
    return mode(list_values, True)


def mean_abs_deviation(list_values: list):
    mean = np.mean(list_values)
    mean_ad = np.mean(abs(list_values - mean))
    return mean_ad


def median_abs_deviation_norm(list_values: list):
    mad = stats.median_abs_deviation(list_values)
    factor = 1 / stats.norm.ppf(0.75)
    mad_norm = mad * factor  # Factor for normal distribution
    return mad_norm


def outlier_values(list_values: list, dtype: Literal['lower', 'upper']):
    q1 = np.percentile(list_values, 25)
    q3 = np.percentile(list_values, 75)
    iqr = q3 - q1
    
    if dtype == 'lower':
        outlier = q1 - 1.5 * iqr
    elif dtype == 'upper':
        outlier = q3 + 1.5 * iqr
    else:
        outlier = None
        
    return outlier


def count_outlier_values(list_values: list, dtype: Literal['lower', 'upper']):
    if dtype == 'lower':
        outlier = outlier_values(list_values, dtype)
        lower_outliers = list_values[list_values < outlier]
        num = len(lower_outliers)
    elif dtype == 'upper':
        outlier = outlier_values(list_values, dtype)
        upper_outliers = list_values[list_values > outlier]
        num = len(upper_outliers)
    else:
        num = None
        
    return num


def describe_full_df(_df: pd.DataFrame):
    '''Generates a full description of a DataFrame, 
    including additional statistics for numeric columns.
    '''

    cols_number = _df.select_dtypes(include='number').columns
    df_describe = _df.describe()
    
    percentile_25 = lambda x: np.percentile(x, 25)
    percentile_75 = lambda x: np.percentile(x, 75)
    range_values = lambda x: np.max(x) - np.min(x)
    lower_outlier = lambda x: outlier_values(x, 'lower')
    upper_outlier = lambda x: outlier_values(x, 'upper')
    count_lower_outlier = lambda x: count_outlier_values(x, 'lower')
    count_upper_outlier = lambda x: count_outlier_values(x, 'upper')
    coefficient_variation = lambda x: pd.Series.std(x) / pd.Series.mean(x)
    shapiro_stat = lambda x: stats.shapiro(x)[0]
    shapiro_pvalue = lambda x: stats.shapiro(x)[1]
    
    
    if np.all(df_describe.columns == cols_number):

        dict_functions = {
            'count': pd.Series.count,
            'count_zero': count_zero,
            'count_nonzero': np.count_nonzero,
            'count_unique': pd.Series.nunique,
            'mean': pd.Series.mean,
            'median': pd.Series.median,
            'mode': mode,
            'mode_lists': mode_lists,
            'mode_count': mode_count,
            'min': np.min,
            '25%': percentile_25,
            '50%': pd.Series.median,
            '75%': percentile_75,
            'max': np.max,
            'range_values': range_values,
            'iqr': stats.iqr,
            'lower_outlier': lower_outlier,
            'count_lower_outlier': count_lower_outlier,
            'upper_outlier': upper_outlier,
            'count_upper_outlier': count_upper_outlier,
            'mean_abs_deviation': mean_abs_deviation,
            'std': pd.Series.std,
            'median_abs_deviation': stats.median_abs_deviation,
            'median_abs_deviation_norm': median_abs_deviation_norm,
            'coefficient_variation': coefficient_variation, 
            'variance': np.var,
            'kurt': pd.Series.kurt,
            'kurtosis': stats.kurtosis,
            'skew': pd.Series.skew,
            'shapiro_stat': shapiro_stat,
            'shapiro_pvalue': shapiro_pvalue,
            'autocorr': pd.Series.autocorr,
            'circvar': stats.circvar,
            'circmean': stats.circmean,
            'circstd': stats.circstd,
            'entropy': stats.entropy,
            'kstat': stats.kstat,
            'kstatvar': stats.kstatvar,
        }
        
        dict_data = {}
        for col_n in cols_number:
            
            list_metric = []
            for col, function in dict_functions.items():
                list_metric.append(function(_df[col_n]))
                    
            dict_data.update({col_n: list_metric})

        df_temp = pd.DataFrame(dict_data)
        df_temp.index = dict_functions.keys()

        return pd.concat([df_temp])
    
    
def save_profile_report(df: pd.DataFrame, filename: str, title: str = "Pandas Profiling Report"):
    '''Saves a profile report of a DataFrame to an HTML file.'''
    
    filename=f'{filename}.html'
    ProfileReport(df, title=title, explorative=True, progress_bar=False).to_file(filename)
    #profile = ProfileReport(df, title=title, explorative=True)
    #profile.to_file(filename)

    print(f"Profile report saved to {filename}")


def describe_df_category(df, col_category, col_metric):
    list_category = df[col_category].unique()
    list_describe_category = [df[col_metric].describe()]
    
    for cat in list_category:
        series_category = df[df[col_category] == cat][col_metric]
        series_category.name = cat
        list_describe_category.append(series_category.describe())
        
    df_describe = pd.concat(list_describe_category, axis=1)
    return df_describe


def apply_percent_category(list_values: list):
    count_list = len(list_values)
    sum_list = sum(list_values) 
    return sum_list / count_list *100    


def convert_types(df, list_columns: list, list_types: list):
    '''Converts the specified columns of a DataFrame to a given data type.'''
    
    for col, dtype in zip(list_columns, list_types):
        if col in df.columns:
            df[col] = df[col].astype(dtype)
        else:
            print(f"Column {col} not found in DataFrame.")
    
    return df