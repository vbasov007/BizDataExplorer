from data_tree import BizDataTree
from mylogger import mylog
from tree_to_dict import tree_to_dict
from render import Render


class WebPageController:

    def __init__(self, data: BizDataTree, render_obj: Render, config: dict):
        self.data = data
        self.render_obj = render_obj
        self.sort_param = config['sort_param']
        self.number_format = config['number_format']

    def process_request(self, request):

        if request.method == 'GET':
            return self.response(content_only=False)
        elif request.method == 'POST':
            self.command(request_args=request.form)
            return self.response(content_only=True)

    def command(self, request_args) -> None:

        command = request_args.get('command')
        node_id = request_args.get('id')

        if node_id:
            if command == 'collapse':
                expanded, _ = self.data.is_expanded(node_id)
                if expanded:
                    self.data.collapse(node_id)

            if command == 'expand':
                expanded, _ = self.data.is_expanded(node_id)
                if expanded:
                    self.data.collapse(node_id)

                expand_by = request_args.get('by')
                error = self.data.expand_id(node_id, expand_by)
                mylog.debug(error)

    def response(self, content_only=True):
        return self.render_obj.render(tree_to_dict(self.data.root,
                                                   sort_param=self.sort_param,
                                                   number_format=self.number_format),
                                      content_only=content_only)
