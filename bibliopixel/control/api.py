from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import getpass, platform, sys, threading
from .. util import log
from . control import ExtractedControl

class Api(ExtractedControl):
    EXTRACTOR = {
        'keys_by_type': {
            'direct_command': ['action'],
            'value_command': ['action', 'value']
        }
    }

    def make_value_commands(self, value_command_list):
        return [{'action': com, 'value': val, 'type': 'value_command'} for (com, val) in value_command_list]

    def make_direct_commands(self, direct_command_list):
        if direct_command_list == None:
            return []
        else:
            return [{'action': com, 'type': 'direct_command'} for (com) in direct_command_list]

    def make_messages(self, params):
        parsed = (urllib.parse.parse_qs(params[2:]))
        vcs = parsed.get('value_command')
        vals = parsed.get('value')
        if (vcs != None and vals != None):
            vcl = list(zip(parsed.get('value_command'), parsed.get('value')))
            value_commands = self.make_value_commands(vcl)
        else:
            value_commands = []
        direct_commands = self.make_direct_commands(parsed.get('direct_command'))
        messages = value_commands + direct_commands
        for msg in messages:
            self.receive(msg)

    def _make_thread(self):
        server_address = ('', 8080)
        httpd = ApiServer(server_address, MsgRequestHandler)
        api = self
        thread = threading.Thread(target = httpd.serve_forever, args = (api, ))
        return thread

class ApiServer(HTTPServer):
    def serve_forever(self, api):
        self.RequestHandlerClass.api = api
        HTTPServer.serve_forever(self)

class MsgRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request_path = self.path
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.api.make_messages(request_path)
