import pandas as pd


def lookup_dict_by_df(alias_df: pd.DataFrame, lookup_col, res_col):
    res = dict()
    for _, row in alias_df.iterrows():
        res.update({row[lookup_col]: row[res_col]})

    return res


def lookup_and_add(working_df: pd.DataFrame, key_col, new_col, lookup_dict):
    for index, row in working_df.iterrows():
        working_df.at[index, new_col] = lookup_dict.get(row[key_col], '')
