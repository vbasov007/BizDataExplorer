"""
Usage: run_flask.py CONFIG

Options:
  -h --help
  CONFIG     config yaml
"""
from docopt import docopt
from flask import Flask, request
import yaml
# import timeit


from mylogger import mylog
from excel import read_excel
import os
import glb
import data_preparation
import web_page_controller as wpc
# from render_tree import render_tree_by_template


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

    glb.number_tree_page = wpc.NumberTreeWebPage(df, glb.cfg)

    app.run(debug=True)


@app.route('/', methods=['GET', 'POST'])
def number_tree_page():
    mylog.debug(request)

    glb.number_tree_page.process_request(request_args=request.args)

    return glb.number_tree_page.html()


if __name__ == '__main__':
    run_flask()
