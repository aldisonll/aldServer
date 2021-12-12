import sys
sys.path.append('../')
from aldServer.server import Debug, createServer
from aldServer.server import Route
from aldServer.server import RESPONSE, CONTENT_TYPE, CHARSET

# server debugging 
Debug.debug = False

# crete route obj
route = Route()

@route.create_route('/me', CONTENT_TYPE.TEXT_HTML, RESPONSE.OK, CHARSET.UTF8)
def template_test():
    return route.render_template('/me.html', name="aldison")

@route.create_route('/profile', CONTENT_TYPE.TEXT_HTML, RESPONSE.OK, CHARSET.UTF8)
def template_test():
    return route.render_template('/profile.html', numbers=[1, 2, 3, 4, 5, 6], to_dos=["one", "two", "three", "four"])

@route.create_route('/user', CONTENT_TYPE.TEXT_HTML, RESPONSE.OK, CHARSET.UTF8)
def template_test():
    return route.render_template('/user.html', name="aldison")

# create the server
server = createServer(hostname="localhost", port=3333)
# run the creted server
server.run()