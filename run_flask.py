"""
Usage: run_flask.py CONFIG

Options:
  -h --help
  CONFIG     config yaml
"""
from docopt import docopt
from flask import Flask, request
# import yaml
# import timeit

from config_manager import YamlConfigManager

from mylogger import mylog
from excel import read_excel
import os
import glb
import data_preparation
import web_page_controller as wpc
# from render_tree import render_tree_by_template
from render import Render

from data_cropping import crop_data

from data_tree import BizDataTree


def new_flask():
    return Flask(__name__)


app = new_flask()


def run_flask():
    arg = docopt(__doc__)

    config = YamlConfigManager(arg['CONFIG'])

    common_cfg: dict = config.get_common_config()
    mylog.debug(common_cfg)

    pos_file_path = os.path.join(common_cfg['folder'], common_cfg['pos_files'][0])
    df, error = read_excel(pos_file_path, replace_nan='')

    if error:
        mylog.error(error)
        return

    if 'aliases' in common_cfg.keys():
        data_preparation.alias_replacement_in_place(df, common_cfg['aliases'], common_cfg['folder'])

    if 'merge' in common_cfg.keys():
        data_preparation.merge_in_place(df, common_cfg['merge'], common_cfg['folder'])

    for item in common_cfg['crop_data']:
        crop_data(df, item['col_name'], item['sum_by'], item['less_then'], item['replace_with'])

    view_cfg = config.get_view_config('number tree')
    render_obj = Render(view_cfg['template'], drill_down_by=view_cfg['drill_down_by'])
    data = BizDataTree(source_df=df, sum_by=view_cfg['sum_by'])

    glb.number_tree_page = wpc.WebPageController(data, render_obj, view_cfg)

    app.run(debug=True)


@app.route('/', methods=['GET', 'POST'])
def number_tree_page():
    mylog.debug(request)

    return glb.number_tree_page.process_request(request)


if __name__ == '__main__':
    run_flask()
