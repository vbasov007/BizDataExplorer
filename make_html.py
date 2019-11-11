from data_tree import BizDataNode
from html_escape import html_escape


def tagged(tag: str, content: str, *attr) -> str:
    res = r'<' + tag
    for item in attr:
        res += r' ' + item
    res += r'>'
    res += content
    res += r'</' + tag + r'>'

    return res


def render_method_basic(node: BizDataNode) -> str:
    id_str = 'id="{0}"'.format(node.id)
    content = tagged('span', html_escape(node.name) + ': ', 'class="customer_name btn"', id_str) + \
        tagged('span', node.value, 'class="number btn"', id_str)

    next_level = ''

    if len(node.children) > 0:
        for child_node in node.children:
            next_level += render_method_basic(child_node)
        next_level = tagged('ul', next_level)

    return tagged('li', content + next_level)


def render_method(node: BizDataNode, sort_param: dict = None, number_format: dict = None) -> str:
    if sort_param is None:
        sort_param = {}
    if number_format is None:
        number_format = {}

    divider = number_format.get('divider', 1.0)
    format_str = number_format.get('format', '{:}')
    ending = number_format.get('ending', '')

    value_str = (format_str + ending).format(float(node.value) / divider)

    reverse = sort_param.get('reverse', True)
    top_n = sort_param.get('top_n', 0)
    min_threshold = sort_param.get('min', 0)

    id_str = 'id="{0}"'.format(node.id)
    content = tagged('span', html_escape(node.name) + ': ', 'class="customer_name btn"', id_str) + \
        tagged('span', value_str, 'class="number btn"', id_str)

    next_level = []

    if len(node.children) > 0:

        for child_node in node.children:
            next_level.append({'text': render_method(child_node, sort_param, number_format),
                               'value': child_node.value,
                               })

    next_level = sorted(next_level, key=lambda l: float(l['value']), reverse=reverse)

    if min_threshold > 0:
        next_level = [item for item in next_level if float(item['value']) > min_threshold]

    if top_n > 0:
        next_level = next_level[:top_n]

    next_level_str = [item['text'] for item in next_level]

    next_level_html = tagged('ul', "".join(next_level_str))

    return tagged('li', content + next_level_html)
