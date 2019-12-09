import pandas as pd
from mylogger import mylog
from excel import read_excel
import os


def alias_replacement_in_place(working_df: pd.DataFrame, alias_cfg: dict, working_folder: str) -> None:
    for cfg in alias_cfg:
        alias_file_path = os.path.join(working_folder, cfg['file'])
        alias_df, error = read_excel(alias_file_path, replace_nan='')

        if not error:
            add_aliases(working_df,
                        cfg['key_col'],
                        cfg['new_col'],
                        alias_dict_by_df(alias_df)
                        )
        else:
            mylog.error("Can't use alias file: {0} {1}".format(alias_file_path, error))


def merge_in_place(working_df: pd.DataFrame, merge_cfg: dict, working_folder) -> None:
    for cfg in merge_cfg:
        merge_file_path = os.path.join(working_folder, cfg['file'])
        merge_df, error = read_excel(merge_file_path, replace_nan='')

        if not error:
            lookup_and_add(working_df,
                           key_col=cfg['pos_file_key'],
                           new_col=cfg['new_col'],
                           lookup_dict=lookup_dict_by_df(
                               merge_df,
                               cfg['merge_file_key'],
                               cfg['merge_res_key']))
        else:
            mylog.error("Can't use merge file: {0}".format(merge_file_path))


def lookup_dict_by_df(alias_df: pd.DataFrame, lookup_col, res_col):
    res = dict()
    for _, row in alias_df.iterrows():
        res.update({row[lookup_col]: row[res_col]})

    return res


def lookup_and_add(working_df: pd.DataFrame, key_col, new_col, lookup_dict):
    for index, row in working_df.iterrows():
        working_df.at[index, new_col] = lookup_dict.get(row[key_col], '')


def alias_dict_by_df(alias_df):
    res = dict()
    for _, row in alias_df.iterrows():
        r = list(row)
        r = [i for i in r if len(i) > 0]
        for val in r[1:]:
            res.update({val: r[0]})

    return res


def add_aliases(working_df: pd.DataFrame, key_col: str, new_col: str, alias_dict: dict):
    for index, row in working_df.iterrows():
        working_df.at[index, new_col] = alias_dict.get(row[key_col], row[key_col])
