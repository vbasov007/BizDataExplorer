# from jinja2 import Template
from flask import render_template
from dict_to_nested_list_html import dict_to_nested_list_html


class Render:

    def __init__(self, template_file, **kwargs):
        # self.template = Template(template_file)
        self.template_file = template_file
        self.template_vars = kwargs

    def render(self, data: dict, content_only=True) -> str:

        content = dict_to_nested_list_html(data)

        if content_only:
            return content
        else:
            # return self.template.render(content=content)
            return render_template(self.template_file, content=content, **self.template_vars)
