## aldServer - a template server

Inspired by Flask and Jinja. Super easy to use!

#### Installation
```bash
pip3 install aldSever
```

#### Simple Code Example
```python 
# imports
from aldServer.server import createServer, Route, Debug
from aldServer.server import RESPONSE, CONTENT_TYPE, CHARSET

# server debugging (false by default)
Debug.debug = True 

# crete route obj
route = Route()

# create static folder 
route.static_folder('/static')

# create simple route
@route.create_route('/api/v2/json', CONTENT_TYPE.JSON, RESPONSE.OK, CHARSET.UTF8)
def json_test():
    return "{'json': 'is the best'}"

# simple templating, passing arguments
@route.create_route('/me', CONTENT_TYPE.TEXT_HTML, RESPONSE.OK, CHARSET.UTF8)
def template_test():
    return route.render_template('/me.html', name="aldison")
    ''' - me.html file:
       <h3>Hello my name is {{%name%}},</h3>
       <h4>and this server is made with aldServer.</h4> 
    '''
    ''' - me.html file after rendering
       <h3>Hello my name is aldison,</h3>
       <h4>and this server is made with aldServer.</h4> 
    '''

# create the server
server = createServer(hostname="localhost", port=3333)
# run the created server
server.run()
```

#### Template Supports

- Different loops:

```python
#1 -  to_dos - is given as a parameter
{%for to_do in to_dos%}
    <li>{{to_do}}</li>
{%endloop%}

#2
{%for i in range(5)%}
    <li>{{i}}</li>
{%endloop%}

#3
{%for i, x in enumerate(range(5))%}
    <li>{{i}} - {{x}}</li>
{%endloop%}

#4
{%for i in range(5)%}
    {{ i }} x 7 = {{i * 7}} <br>
{%endloop%}

#5
{%for item in ["hello", "world"]}
    <li>{{item}}</li>
{%endloop%}
```

- Printing variables 
```python 
<h3>Hello my name is {{%name%}},</h3>
<h4>and this server is made with aldServer.</h4> 
```
