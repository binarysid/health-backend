from rest_framework.response import Response
class Response(Response):

    def __init__(self, data=None, message=None, code=None, status=None,
                template_name=None, headers=None,
                exception=False, content_type=None):

        data_content = {
            'code': code,
            'message': message,
            'data': data,
        }
        super(Response, self).__init__(
            data=data_content,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )
