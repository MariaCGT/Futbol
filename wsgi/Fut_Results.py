#coding:utf-8

import requests
import json
import os
from bottle import request, get, post, run, debug, route, template,error, TEMPLATE_PATH
import bottle

#Pagina principal de la app, con las distintas opciones de búsqueda

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
	
@route('/jornadas1')
def jornadas1():
	ronda = request.forms.get("ronda")
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','league':'1','req':'matchs','round':ronda}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	return template('jornada',datos=datos)
	
@route('/partidos1')
def partidos1():
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','req':'matchsday','date':'2012-08-19','top':'1','limit':'1'}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	return template('partido',datos=datos)
	
@route('/clasificacion2')
def clasificacion1():
	dicc_parametros = {'key':'94c694751928db22f60b189594f8c5b6','format':'json','league':'2','req':'tables'}
	r = requests.get("http://www.resultados-futbol.com/scripts/api/api.php", params=dicc_parametros)
	datos = json.loads(r.text.encode("utf-8"))
	return template('clasificacion2',datos=datos)
	
	
	
	
debug='True'		
run(host='localhost', port=8080)
