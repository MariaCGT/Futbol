from bottle import route, default_app, run
from funciones import cuadrado

@route('/name/<name>')
def nameindex(name='Stranger'):
    return '<strong>Hola, %s!</strong>' % name
 
@route('/')
def index():
    return '<strong>Hello %d</strong>' % cuadrado(3)

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

if ON_OPENSHIFT:
    TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
                                      'runtime/repo/wsgi/views/'))
    
    application=default_app()
else:
    run(host='localhost', port=8080, debug=True)
