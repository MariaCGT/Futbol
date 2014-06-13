#coding:utf-8

import requests
import json
import os
from bottle import request, get, post, run, debug, route, template, error, TEMPLATE_PATH
import bottle


@route('/')
def buscar():
	return template('index')

@get('/bbva')
def bbva():
    return template('bbva')
    
@get('/segunda')
def segunda():
	return template('adelante')
    
@route('/clasificacion1')
def clasificacion1():
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','league':'1','req':'tables'}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	return template('clasificacion1',datos=datos)
	
@get('/pedir_jornada1')
def pedir_jornada1():
	return template('pedir_jornada1')
	
@post('/jornada1')
def jornadas1():
	ronda = request.forms.get("ronda")
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','league':'1','req':'matchs','round':ronda}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	return template('jornada',datos=datos,ronda=ronda)
	
@get('/pedir_fecha1')
def pedir_fecha1():
	return template('pedir_fecha1')
	
@post('/partidos1')
def partidos1():
	global fecha
	fecha = request.forms.get("fecha")
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','req':'matchsday','date':fecha}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	
	rango=int(len(datos['matches']))
	partidos = []
	comp = []

	for i in xrange(rango):
		comp = datos['matches'][i]['competition_name']
		if comp == "Liga BBVA":
			partidos.append([])
			partidos[i].append(datos['matches'][i]['id'])
			partidos[i].append(datos['matches'][i]['local'])
			partidos[i].append(datos['matches'][i]['visitor'])
			partidos[i].append(datos['matches'][i]['result'])
	return template('partidos',fecha=fecha,partidos=partidos)
	
@post('/detalle_partido')
def detalles():
	ident = request.forms.get("ident")
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','req':'match','id':ident}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	
	return template('detalles',datos=datos)
	
	

	
	
@route('/clasificacion2')
def clasificacion1():
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','league':'2','req':'tables'}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	return template('clasificacion2',datos=datos)
	
	
	
ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

if ON_OPENSHIFT:
    TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'],
                                      'app-root/repo/wsgi/views/'))
    
    application=default_app()
else:
    run(host='localhost', port=8080)
