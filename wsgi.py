#!/usr/bin/python
import os
import jinja2

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
repodir = os.environ['OPENSHIFT_REPO_DIR']
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

def application(environ, start_response):

    templateLoader = jinja2.FileSystemLoader(searchpath=repodir + "/templates/")
    env = jinja2.Environment(loader=templateLoader)
    ctype = 'text/plain'
    if environ['PATH_INFO'] == '/health':
        response_body = "1"
    elif environ['PATH_INFO'] == '/env':
        response_body = ['%s: %s' % (key, value)
                    for key, value in sorted(environ.items())]
        response_body = '\n'.join(response_body)
    elif environ['PATH_INFO'] == '/api/':
        ctype = 'text/json'
        template = env.get_template('capabilities.json')
        response_body = str(template.render())
    elif environ['PATH_INFO'] == '/api/vtimeseries/':
        ctype = 'text/json'
        template = env.get_template('vtimeseries.json')
        response_body = str(template.render())
    elif environ['PATH_INFO'] == '/api/vtimeseries/pdf-profound/':
        ctype = 'text/json'
        template = env.get_template('locations.json')
        response_body = str(template.render())
    else:
        ctype = 'text/html'
        template = env.get_template('welcome.html')
        response_body = str(template.render({"title": "OpenShift Python Application", 
                                "header": "Welcome To An Example RESTFul API For ePD's"}))

    status = '200 OK'
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    #
    start_response(status, response_headers)
    return [response_body]

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
