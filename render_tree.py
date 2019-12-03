from jinja2 import Template


def render_nested_dict(source: dict, template_str: str, nested_key='children') -> str:
    if not isinstance(source, dict):
        return ''

    nested_list = source.get(nested_key, [])

    nested_str = ''
    for item in nested_list:
        nested_str += render_nested_dict(item, template_str, nested_key)

    render_args = dict(source)
    render_args.update({nested_key: nested_str})

    return Template(template_str).render(**render_args)


def render_tree_by_template(src_tree_as_dict: dict, template_str: str, nested_key='children',
                            sort_param: dict = None) -> str:
    if sort_param is None:
        sort_param = {}

    reverse = sort_param.get('reverse', True)
    top_n = sort_param.get('top_n', 0)
    min_threshold = sort_param.get('min', 0)
    sort_by = sort_param.get('sort_by', None)

    nested_list = src_tree_as_dict.get(nested_key, [])

    if sort_by is not None:
        nested_list.sort(key=lambda x: float(x[sort_by]), reverse=reverse)
        if top_n > 0:
            nested_list = nested_list[:top_n]
        if min_threshold > 0:
            nested_list = [item for item in nested_list if float(item[sort_by]) > min_threshold]

    nested_str = ''
    for item in nested_list:
        nested_str += render_nested_dict(item, template_str, nested_key)

    render_args = dict(src_tree_as_dict)
    render_args.update({nested_key: nested_str})

    return Template(template_str).render(**render_args)
