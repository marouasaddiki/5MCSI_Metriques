from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)     
@app.route("/contact/")
def contact():
    return render_template("contact.html")
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  @app.route("/histogramme/")
def mongraphique():
    return render_template("graphique.html")
# Route pour extraire les minutes d'une information formatée
# Route pour extraire les minutes d'une information formatée
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})

# Route pour récupérer les commits minute par minute
@app.route('/commits/')
def commits():
    # URL de l'API GitHub pour les commits du repository
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'

    # Ouvrir l'URL et lire les données
    response = urlopen(url)
    data = json.loads(response.read().decode())

    # Initialisation d'un dictionnaire pour compter les commits par minute
    commits_per_minute = {}

    # Parcours des commits pour compter les occurrences par minute
    for commit in data:
        commit_date = commit['commit']['author']['date']
        minute = extract_minutes(commit_date)['minutes']
        if minute in commits_per_minute:
            commits_per_minute[minute] += 1
        else:
            commits_per_minute[minute] = 1

    # Création d'une liste de tuples (minute, nombre de commits)
    commits_data = [{'minute': minute, 'commits': commits_per_minute[minute]} for minute in sorted(commits_per_minute.keys())]

    # Retourner les données au format JSON
    return jsonify({'commits_data': commits_data})

   

@app.route('/')
def hello_world():
    return render_template('hello.html') #comm


if __name__ == "__main__":
  app.run(debug=True)
