import pandas as pd
import numpy as np


def crop_data(source_df: pd.DataFrame, col_name: str, sum_by: str, less_then: float, replace_with: str):
    source_df[sum_by] = pd.to_numeric(source_df[sum_by], errors='coerce')
    source_df.replace(np.nan, 0, regex=True, inplace=True)

    unique_values = list(set(source_df[col_name].tolist()))

    for val in unique_values:
        s = source_df.loc[np.isin(source_df[col_name], val), sum_by].sum()
        if s < float(less_then):
            source_df.loc[source_df[col_name] == val, col_name] = replace_with
