import copy
from urllib.parse import urlencode

import time


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print(f'BEFORE processing {request.path} {request.method}')

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        print('AFTER')
        with open('logger.txt', 'a') as f:
            f.write(f'processing request: {request.path} {request.method}\n')

        return response

    return middleware


class TimingLog:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        t1 = time.time()
        response = self.get_response(request)
        t2 = time.time()
        print(f"TOTAL TIME:{t2 - t1}")
        return response


class QueryParamsInjectorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        query_params = copy.deepcopy(request.GET)
        if 'page' in query_params:
            del query_params['page']
        request.query_params = urlencode(query_params)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
