import sys
sys.path.append('../')
from aldServer.server import createServer
from aldServer.server import Route
from aldServer.server import RESPONSE, CONTENT_TYPE, CHARSET

# crete route obj
route = Route()


@route.create_route('/me', CONTENT_TYPE.TEXT_HTML, RESPONSE.OK, CHARSET.UTF8)
def template_test():
    return route.render_template('/me.html')

# create the server
server = createServer(hostname="localhost", port=3333)
# run the creted server
server.run()