from anytree import PostOrderIter, PreOrderIter, RenderTree
import pandas as pd
import numpy as np

from error import Error
from mylogger import mylog
from bizdatanode import BizDataNode


class BizDataTree:
    def __init__(self, df: pd.DataFrame, sum_by: str):

        df[sum_by] = pd.to_numeric(df[sum_by], errors='coerce')
        df = df.replace(np.nan, 0, regex=True)

        value = df[sum_by].sum()
        self.root = BizDataNode('root', str(value))
        self._df = df
        self._sum_by = sum_by

    def collapse(self, node_id) -> Error:
        current_node, error = self._node_by_id(node_id)

        if error:
            return error

        for node in PostOrderIter(current_node):
            if node is not current_node:
                node.parent = None

        return Error(None)

    def expand_id(self, node_id, by: str) -> Error:
        current_node, error = self._node_by_id(node_id)

        if error:
            return error

        return self.expand_node(current_node, by)

    def expand_node(self, current_node: BizDataNode, by: str) -> Error:

        subset_df = self._subset_df(current_node)
        dv_list, error = self._different_values(subset_df, by)

        if error:
            return error

        # df = self._subset_df(current_node)

        mylog.debug("{0} unique values".format(len(dv_list)))

        for v in dv_list:
            flt = {'column': by, 'value': v}
            s = self._sum(subset_df, flt)
            BizDataNode(v, str(s), parent=current_node, subset_filter=flt)

        return Error(None)

    def expand_by_name(self, name: str, by: str, parent_node=None) -> Error:
        node, error = self._node_by_name(name, parent_node)
        if error:
            return error
        return self.expand_node(node, by)

    def is_expanded(self, node_id) -> (bool, Error):
        current_node, error = self._node_by_id(node_id)

        if error:
            return False, error

        if len(current_node.children) > 0:
            return True, Error(None)
        else:
            return False, Error(None)

    def toggle(self, node_id, by: str):

        expanded, error = self.is_expanded(node_id)

        if error:
            return error

        if expanded:
            self.collapse(node_id)
        else:
            self.expand_id(node_id, by)

        return Error(None)

    def print_console(self):
        print(RenderTree(self.root))

    def _subset_df(self, current_node) -> pd.DataFrame:

        subset_df = self._df

        subset_filter_list = self._filter_list(current_node)

        for sf in subset_filter_list:
            if sf is not None:
                subset_df = subset_df[subset_df[sf['column']] == sf['value']]

        return subset_df

    def _node_by_id(self, node_id) -> (BizDataNode, Error):
        for node in PreOrderIter(self.root):
            if node.id == node_id:
                return node, Error(None)
        return None, Error("No such node:{0}".format(node_id))

    def _node_by_name(self, name, start_node=None) -> (BizDataNode, Error):
        if start_node is None:
            start_node = self.root
        node: BizDataNode
        for node in PreOrderIter(start_node):
            if node.name == name:
                return node, Error(None)
        return None, Error("No such node:{0}".format(name))

    def _sum(self, df: pd.DataFrame, subset_filter=None):

        #        if subset_filter is not None:
        #            df = df[df[subset_filter['column']] == subset_filter['value']]
        if subset_filter is not None:
            f_col = subset_filter['column']
            f_val = subset_filter['value']
            return df.loc[np.isin(df[f_col], f_val), self._sum_by].sum()

        return df[self._sum_by].sum()

    @staticmethod
    def _different_values(subset_df, col_name) -> (list, Error):
        if col_name in subset_df.columns:
            return list(set(subset_df[col_name].tolist())), Error(None)
        else:
            return list(), Error("No such column:'{0}'".format(col_name))

    @staticmethod
    def _filter_list(current_node):
        res = []
        while True:
            res.append(current_node.subset_filter)

            if current_node.parent is None:
                break
            else:
                current_node = current_node.parent

        res.reverse()
        return res

    def tree_to_dict(self):
        return self.root.tree_to_dict()
