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
        # Appeler l'API GitHub pour récupérer les commits
        url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
        response = requests.get(url)
        
        if response.status_code != 200:
            return f"Erreur lors de l'accès à l'API GitHub : {response.status_code}", 500
        
        data = response.json()

        # Extraire les dates des commits
        commit_dates = [commit['commit']['author']['date'] for commit in data]
        commit_minutes = [datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').minute for date in commit_dates]

        # Comptabiliser les commits par minute
        commit_count = Counter(commit_minutes)

        # Créer un graphique
        plt.figure(figsize=(10, 6))
        plt.bar(commit_count.keys(), commit_count.values())
        plt.xlabel('Minutes')
        plt.ylabel('Nombre de Commits')
        plt.title('Nombre de Commits par Minute')

        # Sauvegarder le graphique en mémoire
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()
        img.close()
        plt.close() # Fermer le graphique pour éviter les conflits

        # Retourner le graphique sous forme d'image
        return f'<img src="data:image/png;base64,{img_base64}" />'

    except Exception as e:
        return f"Erreur : {str(e)}", 500


@app.route('/')
def hello_world():
    return render_template('hello.html') #comm


if __name__ == "__main__":
  app.run(debug=True)
