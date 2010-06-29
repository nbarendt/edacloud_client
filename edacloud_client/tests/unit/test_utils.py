import BaseHTTPServer
from threading import Thread

class MockFunctionHelper(object):
    def __init__(self, func):
        self.func = func

    def will_return(self, value):
        setattr(self.func, 'return_value', value)

    def will_cause_side_effect(self, value):
        setattr(self.func, 'side_effect', value)

    def was_called_with(self, expected):
        actual = getattr(self.func, 'call_args_list')
        assert expected == actual, 'Expected %s but actual %s' % (expected, actual)


class HttpTestServer(object):
    def __init__(self):
        self.httpd_server = BaseHTTPServer.HTTPServer(('localhost', 0), BaseHTTPServer.BaseHTTPRequestHandler)
        self.server_thread = Thread(target=self.httpd_server.serve_forever)
        self.server_thread.daemon = True

    @property
    def hostname(self):
        return self.httpd_server.server_address[0]
    
    @property
    def port(self):
        return self.httpd_server.server_address[1]
        
    def start(self):
        self.server_thread.start()

    def stop(self):
        if self.server_thread.isAlive():
            self.httpd_server.shutdown()
            self.server_thread.join()
            self.server_thread = None

    def replace_request_handler_with(self, request_handler):
        self.httpd_server.RequestHandlerClass = request_handler

class QuietHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

class SimpleGETHTTPRequestHandler(QuietHTTPRequestHandler):
    resp = ''
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.resp)
        return
