"""
Usage: run_flask.py CONFIG

Options:
  -h --help
  CONFIG     config yaml
"""
from docopt import docopt
from flask import Flask, request, render_template
import yaml
# import timeit

from data_tree import BizDataTree
from mylogger import mylog
from excel import read_excel
import os
import glb
import data_preparation
# from render_tree import render_tree_by_template

from render_number_tree import render_bizdatanode_html

from data_cropping import crop_data


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

    if 'aliases' in glb.cfg.keys():
        data_preparation.alias_replacement_in_place(df, glb.cfg['aliases'], glb.cfg['folder'])

    if 'merge' in glb.cfg.keys():
        data_preparation.merge_in_place(df, glb.cfg['merge'], glb.cfg['folder'])

    for item in glb.cfg['crop_data']:
        crop_data(df, item['col_name'], item['sum_by'], item['less_then'], item['replace_with'])

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

    html = render_bizdatanode_html(glb.data_tree.root,
                                   sort_param=glb.cfg['sort_param'],
                                   number_format=glb.cfg['number_format'])

    return render_template('templ.html', content=html, drill_down_by=glb.cfg['drill_down_by'])


if __name__ == '__main__':
    run_flask()
