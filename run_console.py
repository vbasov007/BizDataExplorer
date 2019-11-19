"""
Usage: run_console.py [--in=FILE] [--out=FILE]

Options:
  -h --help
  -i FILE --in=FILE               input data
  -o FILE --out=FILE              output
"""

from docopt import docopt

from data_tree import BizDataTree
from mylogger import mylog
from excel import read_excel

from make_html import render_method_basic

import dt


def main():
    arg = docopt(__doc__)

    file_in = arg['--in']
    file_out = arg['--out']

    df, error = read_excel(file_in, replace_nan='')

    if error:
        mylog.error(error)
        return

    dt.data_tree = BizDataTree(df, 'POS FY')

    while True:
        dt.data_tree.print_console()
        html = dt.data_tree.render_html(render_method_basic)

        with open(file_out, "w") as text_file:
            print(html, file=text_file)

        node_id = input("Click on id:")

        expanded, error = dt.data_tree.is_expanded(node_id)

        if error:
            mylog.error(error)
            continue

        if expanded:
            dt.data_tree.collapse(node_id)
        else:
            drill_by = input("Drill by:")
            error = dt.data_tree.expand_id(node_id, drill_by)
            if error:
                mylog.error(error)
                continue


if __name__ == '__main__':
    main()
