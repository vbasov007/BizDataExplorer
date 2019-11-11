"""
Usage: run_flask.py [--in=FILE]

Options:
  -h --help
  -i FILE --in=FILE               input data
"""
from docopt import docopt
from flask import Flask, request, render_template
from data_tree import BizDataTree
from mylogger import mylog
from excel import read_excel
import cfg

from make_html import render_method

app = Flask(__name__)


def run_flask():
    arg = docopt(__doc__)

    file_in = arg['--in']

    df, error = read_excel(file_in, replace_nan='')

    if error:
        mylog.error(error)
        return

    cfg.data_tree = BizDataTree(df, 'POS FY')

    cfg.data_tree.expand_by_name('root', 'DISTRIBUTOR')

    app.run(debug=True)


@app.route('/', methods=['GET', 'POST'])
def test():

    drill_down_by = ['DISTRIBUTOR', 'FINAL MC', 'COUNTRY FC', 'DIV', 'PL', 'HFG', 'SALES PRODUCT']
    mylog.debug(request)

    if cfg.data_tree is None:
        return render_template('templ.html', content="data not defined", drill_down_by=drill_down_by)

    mylog.debug(request.args)

    command = request.args.get('command')
    node_id = request.args.get('id')

    if node_id:
        if command == 'collapse':
            expanded, _ = cfg.data_tree.is_expanded(node_id)
            if expanded:
                cfg.data_tree.collapse(node_id)

        if command == 'expand':

            expanded, _ = cfg.data_tree.is_expanded(node_id)
            if expanded:
                cfg.data_tree.collapse(node_id)

            expand_by = request.args.get('by')
            error = cfg.data_tree.expand_id(node_id, expand_by)
            mylog.debug(error)

    html = cfg.data_tree.render_html(render_method,
                                     sort_param={
                                         'top_n': 50,
                                         'min': 10000.0,
                                     },
                                     number_format={
                                         'divider': 1000.0,
                                         'format': '{:1.0f}',
                                         'ending': ' K',
                                     })
    return render_template('templ.html', content=html, drill_down_by=drill_down_by)


if __name__ == '__main__':
    run_flask()
