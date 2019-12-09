import pandas as pd

from data_tree import BizDataTree
import flask
from render_number_tree import render_bizdatanode_html
from mylogger import mylog


class NumberTreeWebPage:

    def __init__(self, data_df: pd.DataFrame, config: dict):
        self.biz_data_tree = BizDataTree(data_df, config['sum_by'])
        self.config = config

    def process_request(self, request_args) -> None:

        command = request_args.get('command')
        node_id = request_args.get('id')

        if node_id:
            if command == 'collapse':
                expanded, _ = self.biz_data_tree.is_expanded(node_id)
                if expanded:
                    self.biz_data_tree.collapse(node_id)

            if command == 'expand':
                expanded, _ = self.biz_data_tree.is_expanded(node_id)
                if expanded:
                    self.biz_data_tree.collapse(node_id)

                expand_by = request_args.get('by')
                error = self.biz_data_tree.expand_id(node_id, expand_by)
                mylog.debug(error)

    def html(self) -> str:
        content = render_bizdatanode_html(self.biz_data_tree.root,
                                          sort_param=self.config['sort_param'],
                                          number_format=self.config['number_format'])

        return flask.render_template('templ.html', content=content, drill_down_by=self.config['drill_down_by'])


class TableTreeWebPage(NumberTreeWebPage):
    pass
