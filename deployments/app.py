from flask import Flask
from flask import request
from datetime import datetime
app = Flask(__name__)

@app.route("/",methods=['GET'])
def webPage():
    html = """
<h1>CSC 8567</h1>
<p>Site assez simpliste !</p>
<p>v1</p>
<p>"""
    html += "L'URL utilisé pour accéder au site : " + request.base_url
    html += "</p><p>"
    html += "L'heure : "+datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    html += "</p>"
    return html