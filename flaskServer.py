#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, url_for
from bs4 import BeautifulSoup
import json
import requests
import os

app = Flask(__name__, static_url_path='/static')

def updateJson(filename, dict_data):
	with open(filename, 'r') as json_data: 
		data = json.load(json_data)

	data.extend(dict_data)

	with open(filename, 'w') as json_data: 
		json.dump(data, json_data)

@app.route('/json')
def send_static():
	return "<a href={}>URLs Privadas</a><br>".format(url_for('static', filename='privateUrls.json'))

@app.route('/')
def formulario():
	return render_template('index.html')

@app.route('/', methods=['post'])
def index():

	idStart = int(request.form['id'])
	tipo = int(request.form['tipo'])

@app.route('/sala/<tipo>/<qualId>')
def sala(tipo, qualId):
	# script para cavar

	qualId = int(qualId)

	if tipo == 'after':
		tip = range(qualId, 400000000)
	else:
		tip = range(qualId, 0, -1)

	for i in tip:
		
		#inicio = time.time()
	
		url = 'http://player.vimeo.com/video/{}'.format(i)
	
		acessar = requests.get(url, stream=True).content
		getCode = BeautifulSoup(acessar, 'lxml')

		p = getCode.find('p')
		p = str(p).replace('p', '').replace('<', '').replace('>', '').replace('/', '')

		#print(p)
	
		titulo = getCode.find('title')
		titulo = str(titulo).replace('title', '').replace('<', '').replace('>', '').replace('/', '')

		if titulo == 'Sorry' or titulo == 'Desculpe':

			if p == 'This video does not exist.' or p == 'Este vídeo não existe.':
				updateJson('static/urls.json', [{'id':i, 'tipo':'inexistente'}])

			else:
				r = requests.get(url, headers={'referer':'https://saladosaber.com.br'})
				status = r.status_code
				updateJson('static/privateUrls.json', [{'id':i, 'tipo':'privado', 'status':status}])

		else:
			updateJson('static/urls.json', [{'id':i, 'tipo':'publico'}])
	return 'Fazendo os requests... Acompanhe através /json/urls.json'

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
