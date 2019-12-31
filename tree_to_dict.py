from collections import OrderedDict
from bizdatanode import BizDataNode

from anytree.exporter import DictExporter
import copy


def tree_to_dict(root_node: BizDataNode, sort_param: dict, number_format: dict) -> OrderedDict:
    dct = bizdatatree_to_dict(root_node,
                              reverse=sort_param.get('reverse', True),
                              top_n=sort_param.get('top_n', 0),
                              min_threshold=sort_param.get('min', 0))

    dct = format_numbers(dct,
                         divider=number_format.get('divider', 1.0),
                         format_str=number_format.get('format', '{:}'),
                         ending=number_format.get('ending', ''))

    return dct


def bizdatatree_to_dict(root_node: BizDataNode, reverse=True, top_n=0, min_threshold=0) -> OrderedDict:
    def _sorted(children):
        res = sorted(children, key=lambda child: float(child.value), reverse=reverse)
        if min_threshold > 0:
            res = [item for item in res if float(item.value) > min_threshold]
        if top_n > 0:
            res = res[:top_n]
        return res

    exporter = DictExporter(dictcls=OrderedDict, childiter=_sorted)

    return exporter.export(root_node)


def format_numbers(source_dict: OrderedDict, divider: float = 1.0, format_str: str = '{:}', ending: str = ''):
    res = copy.deepcopy(source_dict)

    def _fn(dct):
        for k, v in dct.items():
            if k == 'children':
                for child in dct['children']:
                    _fn(child)
            elif k == 'value':
                dct[k] = (format_str + ending).format(float(v) / divider)

    _fn(res)

    return res
