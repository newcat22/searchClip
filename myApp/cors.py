# cors.py
"""解决跨域问题的中间件，作用全局"""


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class CORSMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # 添加响应头
        # 限制哪些域名可以访问，用逗号分隔，如果全部可使用'*'
        response['Access-Control-Allow-Origin'] = '*'
        # 限制携带的请求头，用逗号分隔
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        # 允许发送的请求方式
        response['Access-Control-Allow-Methods'] = 'DELETE, PUT'
        return response
