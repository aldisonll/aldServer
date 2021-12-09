import sys
sys.path.append('../')
from aldServer.server import createServer
from aldServer.server import Route
from aldServer.server import RESPONSE, CONTENT_TYPE, CHARSET

# crete route obj
route = Route()

# create static folder 
route.static_folder('/static')


@route.create_route('/api/v2/test', CONTENT_TYPE.TEXT_HTML, RESPONSE.OK, CHARSET.UTF8)
def test():
    return "/api/v2/test"

@route.create_route('/api/v2/json', CONTENT_TYPE.JSON, RESPONSE.OK, CHARSET.UTF8)
def json_test():
    return "{'json': 'is the best'}"


# create the server
server = createServer(hostname="localhost", port=3333)
# run the creted server
server.run()