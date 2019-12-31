from html_escape import html_escape


def tagged(tag: str, content: str, *attr) -> str:
    res = r'<' + tag
    for item in attr:
        res += r' ' + item
    res += r'>'
    res += content
    res += r'</' + tag + r'>'

    return res


def dict_to_nested_list_html(source_dict: dict):
    def _render(dct):
        id_str = 'id="{0}"'.format(dct['id'])
        content = tagged('span', html_escape(dct['name']) + ': ', 'class="customer_name btn"', id_str) + \
            tagged('span', dct['value'], 'class="number btn"', id_str)

        next_level = ''
        children_list = dct.get('children', [])
        if len(children_list) > 0:
            for child in children_list:
                next_level += _render(child)
            next_level = tagged('ul', next_level)
        return tagged('li', content + next_level)

    return _render(source_dict)
