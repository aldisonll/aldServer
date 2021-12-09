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

@route.create_route('/profile', CONTENT_TYPE.TEXT_HTML, RESPONSE.OK, CHARSET.UTF8)
def template_test():
    return route.render_template('/profile.html', numbers=[1, 2, 3, 4, 5, 6])


# create the server
server = createServer(hostname="localhost", port=3333)
# run the creted server
server.run()