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
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})


        @app.route('/commits/')
def commits_chart():
    try:
        # Appel de l'API GitHub avec urllib
        url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
        with urllib.request.urlopen(url) as response:
            raw_data = response.read()
            data = json.loads(raw_data.decode('utf-8'))

        # Extraire les dates des commits
        commit_dates = [commit['commit']['author']['date'] for commit in data]
        commit_minutes = [datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').minute for date in commit_dates]

        # Comptabiliser les commits par minute
        commit_count = Counter(commit_minutes)

        # Générer un tableau HTML simple
        table_html = "<table border='1'><tr><th>Minute</th><th>Nombre de Commits</th></tr>"
        for minute, count in sorted(commit_count.items()):
            table_html += f"<tr><td>{minute}</td><td>{count}</td></tr>"
        table_html += "</table>"

        # Retourner le tableau HTML
        return f"<h1>Commits par minute</h1>{table_html}"

    except Exception as e:
        return f"Erreur : {str(e)}", 500


@app.route('/')
def hello_world():
    return render_template('hello.html') #comm


if __name__ == "__main__":
  app.run(debug=True)
