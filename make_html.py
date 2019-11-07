from data_tree import BizDataNode


def tagged(tag: str, content: str, *attr) -> str:
    res = '<' + tag
    for item in attr:
        res += ' ' + item
    res += '>'
    res += content
    res += r'</' + tag + '>'

    return res


def render_method(node: BizDataNode) -> str:
    content = tagged('span', node.name + ': ', 'class="customer_name"') + \
              tagged('span', node.value, 'class="number"')
    next_level = ''

    if len(node.children) > 0:
        for child_node in node.children:
            next_level += render_method(child_node)
        next_level = tagged('ul', next_level)

    return tagged('li', content + next_level, 'id="{0}"'.format(node.id))
