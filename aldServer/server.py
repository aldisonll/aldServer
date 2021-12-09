from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from .templateEngine import AldTemplateEngine
import os

class CHARSET:
    UTF8: str = "utf-8"

class CONTENT_TYPE:
    TEXT_HTML: str = "text/html"
    JSON: str = "application/json"

class RESPONSE:
    OK: int = 200
    ACCEPTED: int = 202
    MOVED: int = 301
    FOUND: int = 302
    BAD_REQUEST: int = 400
    UNAUTHORIZED: int = 401
    FORBIDDEN: int = 403
    NOT_FOUND: int = 404
    INTERNAL_SERVER_ERROR: int = 500
    BAD_GATEWAY: int =502

class Route(AldTemplateEngine):
    routes = []
    
    def has_route_files_duplicate_conflict(self, routes, item):
        if item in routes:
            raise SystemExit(f'{list(item.keys())[0]} is duplicated route')
        return False

    def create(self, item):
        if not self.has_route_files_duplicate_conflict(self.routes, item):
            self.routes.append(item)
    
    def create_route(self, *args):
        def inner(func):
            try:
                path = args[0]
                content_type = args[1]
                response_code = args[2]
                charset = args[3]
            except IndexError:
                raise SystemExit("@route_create arguments are wrong or missing.\nExample: @route_create('/test', CONTENT_TYPE.TEXT_HTML, RESPONSE.OK, CHARSET.UTF8, route=route)")
            content = func()
            self.create({path: [content_type, response_code, content, charset]})
        return inner             
    
    def all_files_in_folder(self, folder_name):
        all_files = []
        for path, _, files in os.walk(folder_name):
            for name in files:
                all_files.append(os.path.join(path, name))
        return all_files
    
    def ignore_first_slash(self, static_folder):
        if not static_folder.startswith('/'):
            return static_folder
        return static_folder[1:]

    def get_file_content(self, file_name, isTemplate):
        if not isTemplate:
            with open(file_name, 'r') as file_content:
                return file_content.read()    
        else:
            try:
                with open('template' + file_name, 'r') as file_content:
                    return file_content.read()
            except FileNotFoundError:
                raise SystemExit("/template folder doesn\'t exist")      
                    
    def create_route_for_static_files(self, static_files):
        for file_path in static_files:
            FILE_CONTENT = self.get_file_content(file_path, isTemplate=False)
            self.create({'/' + file_path.replace('\\', '/'): [CONTENT_TYPE.TEXT_HTML, RESPONSE.OK, FILE_CONTENT, CHARSET.UTF8]})

    def static_folder(self, *args):
        try:
            static_folder = self.ignore_first_slash(args[0])
        except Exception as e:
            raise SystemExit("Add a folder path to the static_folder. Example: static_folder('/static')")
        try:
            all_static_files = self.all_files_in_folder(static_folder)
        except FileNotFoundError as e:
            raise SystemExit(e)
        else:
            return self.create_route_for_static_files(all_static_files)

    def render_template(self, file_name, isTemplate=True):
        unrendered_template =  self.get_file_content(file_name, isTemplate)
        return self.template_render(unrendered_template)

class Server(BaseHTTPRequestHandler, RESPONSE):
    
    @property
    def _params(self):
        return parse_qs(urlparse(self.path).query)
    
    @property
    def _route(self):
        for route in Route.routes:
            endpointPath = urlparse(self.path).path 
            if route.get(endpointPath):
                 return route.get(endpointPath)
        return False      
    
    def do_GET(self):
        serverParams = self._params
        if self._route: 
            content_type, response_code= self._route[0], self._route[1]
            content, charset_parameter = self._route[2], self._route[3]
            self.send_response(response_code)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(bytes(content, charset_parameter))
        elif self.path != '/favicon.ico':
            self.send_response(RESPONSE.NOT_FOUND)
            self.end_headers()
            print(f'AldServer - Page Not Found "GET {self.path}" - 404')

@dataclass
class createServer(Server, Route):
    hostname: str
    port: int

    def run(self):
        webServer = HTTPServer((self.hostname, self.port), Server, Route.routes)
        print("AldServer - Server started http://%s:%s" % (self.hostname, self.port))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")