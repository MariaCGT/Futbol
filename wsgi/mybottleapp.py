#coding:utf-8

import requests
import json
import os
from bottle import request, get, post, run, debug, route, template, error, TEMPLATE_PATH, default_app
import bottle

@route('/')
def buscar():
	return template('index')

@get('/bbva')
def bbva():
    return template('bbva')
    
@get('/adelante')
def adelante():
	return template('adelante')
	
@route('/bbva/clasificacion')
def clasificacion1():
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','league':'1','req':'tables'}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	return template('clasificacion',datos=datos)
	
@route('/adelante/clasificacion')
def clasificacion1():
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','league':'2','req':'tables'}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	return template('clasificacion',datos=datos)

@get('/bbva/pedir_jornada')
def pedir_jornada1():
	return template('pedir_jornada1')
	
@get('/adelante/pedir_jornada')
def pedir_jornada2():
	return template('pedir_jornada2')
	
@post('/jornada')
def jornada():
	liga = request.forms.get("liga")
	ronda = request.forms.get("ronda")
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','league':liga,'req':'matchs','round':ronda}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	if datos['match'] == False:
		return template('error_jornada',ronda=ronda)
	else:
		return template('jornada',datos=datos,ronda=ronda)
	
@get('/bbva/pedir_fecha')
def pedir_fecha():
	return template('pedir_fecha1')
	
@get('/adelante/pedir_fecha')
def pedir_fecha():
	return template('pedir_fecha2')
	
@post('/bbva/partidos')
def partidos1():
	fecha = request.forms.get("fecha")
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','req':'matchsday','date':fecha}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	
	if datos['matches'] == False:
		return template('error_fecha',fecha=fecha)
	else:
		rango=int(len(datos['matches']))
		partidos = []
		comp = []
		j = 0
		for i in xrange(rango):
			comp = datos['matches'][i]['competition_name'].encode("UTF-8")
			if comp == "Liga BBVA":
				partidos.append([])
				partidos[j].append(datos['matches'][i]['id'])
				partidos[j].append(datos['matches'][i]['local'])
				partidos[j].append(datos['matches'][i]['visitor'])
				partidos[j].append(datos['matches'][i]['result'])
				j = j + 1
		if partidos == []:
			return template('error_fecha',fecha=fecha)
		else:
			return template('partidos',fecha=fecha,partidos=partidos)
	
@post('/adelante/partidos')
def partidos2():
	fecha = request.forms.get("fecha")
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','req':'matchsday','date':fecha}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text)
	if datos['matches'] == False:
		return template('error_fecha',fecha=fecha)
	else:
		rango=int(len(datos['matches']))
		partidos = []
		comp = []
		j = 0
		for i in xrange(rango):
			comp = datos['matches'][i]['competition_name'].encode("UTF-8")
			if comp == "Segunda División":
				partidos.append([])
				partidos[j].append(datos['matches'][i]['id'])
				partidos[j].append(datos['matches'][i]['local'])
				partidos[j].append(datos['matches'][i]['visitor'])
				partidos[j].append(datos['matches'][i]['result'])
				j = j + 1
		if partidos == []:
			return template('error_fecha',fecha=fecha)
		else:
			return template('partidos',fecha=fecha,partidos=partidos)
			
@post('/detalle_partido')
def detalles():
	ident = request.forms.get("ident")
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','req':'match','id':ident}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
		
	if datos['visitor'] == None:
		return template('error_detalles')
		
	if "goals" in datos['events']:
		rango=int(len(datos['events']['goals']))
		j = 0
		goles = []
		for i in xrange(rango):
			goles.append([])
			goles[j].append(datos['events']['goals'][i]['minute'])
			goles[j].append(datos['events']['goals'][i]['player'])
			goles[j].append(datos['events']['goals'][i]['team'])
			j = j + 1
	else:
		goles = "-"
		
	if "cards" in datos['events']:
		rango=int(len(datos['events']['cards']))
		j = 0
		tarjetas = []
		for i in xrange(rango):
			tarjetas.append([])
			tarjetas[j].append(datos['events']['cards'][i]['minute'])
			tarjetas[j].append(datos['events']['cards'][i]['action'])
			tarjetas[j].append(datos['events']['cards'][i]['player'])
			tarjetas[j].append(datos['events']['cards'][i]['team'])
			j = j + 1
	else:
		tarjetas = "-"
		
	if "changes" in datos['events']:
		rango=int(len(datos['events']['changes']))
		j = 0
		cambios = []
		for i in xrange(rango):
			cambios.append([])
			cambios[j].append(datos['events']['changes'][i]['minute'])
			cambios[j].append(datos['events']['changes'][i]['action'])
			cambios[j].append(datos['events']['changes'][i]['player'])
			cambios[j].append(datos['events']['changes'][i]['team'])
			j = j + 1
	else:
		cambios = "-"
		
	return template('detalles',goles=goles,tarjetas=tarjetas,cambios=cambios,datos=datos)
	
@get('/quiniela')
def quiniela():
	return template('quiniela')
		
@post('/quiniela_jornada')
def quin_jornada():
	ronda = request.forms.get("jornada")
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','req':'quiniela','round':ronda}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	return template('mostrar_quiniela', datos=datos, ronda=ronda)

@get('/mundial')
def segunda():
	return template('mundial')
	
@post('/grupos_mundial')
def grupos_mundial():
	grupo = request.forms.get("grupo")
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','league':'136','req':'tables','group':grupo}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	return template('clasificacion_grupo', datos=datos,grupo=grupo)

@error(404)
def error404(error):
	return template('errores')
	
@error(500)
def error500(error):
	return template('errores')
		
		
		
ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

if ON_OPENSHIFT:
    TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'],
                                      'app-root/repo/wsgi/views/'))
    
    application=default_app()
else:
    run(host='localhost', port=8080)
