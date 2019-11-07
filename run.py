"""
Usage: run.py [--in=FILE] [--out=FILE]

Options:
  -h --help
  -i FILE --in=FILE               input data
  -o FILE --out=FILE              output
"""

from docopt import docopt

from data_tree import BizDataTree
from mylogger import mylog
from excel import read_excel

from make_html import render_method


def main():
    arg = docopt(__doc__)

    file_in = arg['--in']
    file_out = arg['--out']

    df, error = read_excel(file_in, replace_nan='')

    if error:
        mylog.error(error)
        return

    bdt = BizDataTree(df, 'POS FY')

    while True:
        bdt.print_console()
        html = bdt.render_html(render_method)

        with open(file_out, "w") as text_file:
            print(html, file=text_file)

        node_id = input("Click on id:")

        expanded, error = bdt.is_expanded(node_id)

        if error:
            mylog.error(error)
            continue

        if expanded:
            bdt.collapse(node_id)
        else:
            drill_by = input("Drill by:")
            error = bdt.expand(node_id, drill_by)
            if error:
                mylog.error(error)
                continue


if __name__ == '__main__':
    main()
