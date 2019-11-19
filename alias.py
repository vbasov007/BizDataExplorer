import pandas as pd


def alias_dict_by_df(alias_df):
    res = dict()
    for _, row in alias_df.iterrows():
        r = list(row)
        r = [i for i in r if len(i)>0]
        for val in r[1:]:
            res.update({val: r[0]})

    return res


def add_aliases(working_df: pd.DataFrame, key_col: str, new_col: str, alias_dict: dict):
    for index, row in working_df.iterrows():
        working_df.at[index, new_col] = alias_dict.get(row[key_col], row[key_col])
