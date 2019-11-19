"""
Usage: run_flask.py CONFIG

Options:
  -h --help
  CONFIG     config yaml
"""
from docopt import docopt
from flask import Flask, request, render_template
import yaml
from data_tree import BizDataTree
from mylogger import mylog
from excel import read_excel
import os
import glb
from alias import add_aliases, alias_dict_by_df
from lookup import lookup_and_add, lookup_dict_by_df

from make_html import render_method


def new_flask():
    return Flask(__name__)


app = new_flask()


def run_flask():
    arg = docopt(__doc__)

    with open(arg['CONFIG']) as f:
        glb.cfg = yaml.load(f, Loader=yaml.FullLoader)
        mylog.debug(glb.cfg)

    pos_file_path = os.path.join(glb.cfg['folder'], glb.cfg['pos_files'][0])
    df, error = read_excel(pos_file_path, replace_nan='')

    if error:
        mylog.error(error)
        return

    if 'aliases' in glb.cfg:
        for alias_cfg in glb.cfg['aliases']:
            alias_file_path = os.path.join(glb.cfg['folder'], alias_cfg['file'])
            alias_df, error = read_excel(alias_file_path, replace_nan='')

            if error:
                mylog.error("Can't use alias file: {0}".format(alias_file_path))
                continue

            add_aliases(df,
                        alias_cfg['key_col'],
                        alias_cfg['new_col'],
                        alias_dict_by_df(alias_df)
                        )

    if 'merge' in glb.cfg:
        for merge_cfg in glb.cfg['merge']:
            merge_file_path = os.path.join(glb.cfg['folder'], merge_cfg['file'])
            merge_df, error = read_excel(merge_file_path, replace_nan='')
            if error:
                mylog.error("Can't use merge file: {0}".format(merge_file_path))
                continue

            lookup_and_add(df,
                           key_col=merge_cfg['pos_file_key'],
                           new_col=merge_cfg['new_col'],
                           lookup_dict=lookup_dict_by_df(merge_df, merge_cfg['merge_file_key'], merge_cfg['merge_res_key']))

    glb.data_tree = BizDataTree(df, glb.cfg['sum_by'])

    app.run(debug=True)


@app.route('/', methods=['GET', 'POST'])
def test():
    mylog.debug(request)

    if glb.data_tree is None:
        return render_template('templ.html', content="data not defined", drill_down_by=glb.cfg['drill_down_by'])

    mylog.debug(request.args)

    command = request.args.get('command')
    node_id = request.args.get('id')

    if node_id:
        if command == 'collapse':
            expanded, _ = glb.data_tree.is_expanded(node_id)
            if expanded:
                glb.data_tree.collapse(node_id)

        if command == 'expand':

            expanded, _ = glb.data_tree.is_expanded(node_id)
            if expanded:
                glb.data_tree.collapse(node_id)

            expand_by = request.args.get('by')
            error = glb.data_tree.expand_id(node_id, expand_by)
            mylog.debug(error)

    html = glb.data_tree.render_html(render_method,
                                     sort_param=glb.cfg['sort_param'],
                                     number_format=glb.cfg['number_format'])

    return render_template('templ.html', content=html, drill_down_by=glb.cfg['drill_down_by'])


if __name__ == '__main__':
    run_flask()
