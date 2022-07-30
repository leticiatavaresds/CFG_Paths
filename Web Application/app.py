# from urllib import response
# import pymysql.cursors
# import pandas as pd
# import scipy.spatial
# from base64 import b64encode

import ControlFlowPaths
import imghdr
import re
from pathlib import Path
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, Response




from flask import Flask, render_template, request


code_1 = ""
code = ""
filename = ""
tipo_script = ""
filename_download = ""


app = Flask(__name__,template_folder="templates")  
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   

app.config['MAX_CONTENT_LENGTH'] = 2048 * 2048
app.config['UPLOAD_EXTENSIONS'] = ['.py']
app.config['UPLOAD_PATH'] = 'uploads'

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@app.route("/")

def PlayTypes():

    IMG_FOLDER = os.path.join('static', 'IMG')
    app.config['UPLOAD_FOLDER'] = IMG_FOLDER

    graph_image = os.path.join(app.config['UPLOAD_FOLDER'], 'graph.png')
    script_image = os.path.join(app.config['UPLOAD_FOLDER'], 'script.png')
    code = ""            
    
    return render_template("people.html",  titulo = "Selecione o script python:", 
     graph_image = graph_image, script_image = script_image, code = code)


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route("/files", methods=['GET','POST'])

def files_response():

    global code_1, filename

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)

    if filename != '':
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)

        if not os.path.exists(file_path):
            return redirect(url_for('PlayTypes'))
            
        code_1 = ControlFlowPaths.graph_testing(file_path)
        code = code_1.script_nodes

    else:
        code = ""

    IMG_FOLDER = os.path.join('static', 'IMG')
    app.config['UPLOAD_FOLDER'] = IMG_FOLDER

    graph_image = os.path.join(app.config['UPLOAD_FOLDER'], 'graph.png')
    script_image = os.path.join(app.config['UPLOAD_FOLDER'], 'script.png')

    
    return render_template("files.html", titulo = "Arquivos",
    graph_image = graph_image, script_image = script_image, code = code)


@app.route("/code_graph", methods=['GET', 'POST'])

def code_nodes():

    global cidade, localidade, code, tipo_script, filename_download

    tipo_script = (request.args.get("action"))


    IMG_FOLDER = os.path.join('static', 'IMG')
    app.config['UPLOAD_FOLDER'] = IMG_FOLDER

    name_image = code_1.image_file
    graph_image = os.path.join(app.config['UPLOAD_FOLDER'], 'graph.png')
    script_image = os.path.join(app.config['UPLOAD_FOLDER'], 'script.png')
    
    cidade = "Arquivos"    

    if str(tipo_script) == "Script Cobertura de Nós":

        code = code_1.script_nodes
        filename_download = "Script_Cobertura_Nós.py"
    
        return render_template("code_graph.html", nome_arquivo = tipo_script,
        graph_image = graph_image, script_image = script_image, code = code)

    elif tipo_script == "Script Cobertura de Arcos":

        code = code_1.script_arcs
        filename_download = "Script_Cobertura_Arcos.py"
    
        return render_template("code_graph.html",  graph_image = graph_image, 
        script_image = script_image, code = code, nome_arquivo = tipo_script)

    elif tipo_script == "Script Cobertura de Pares de Arcos":

        code = code_1.script_pair_arcs
        filename_download = "Script_Cobertura_Pares_Arcos.py"
    
        return render_template("code_graph.html", graph_image = graph_image, 
        script_image = script_image, code = code, nome_arquivo = tipo_script)

    elif tipo_script == "Grafo CFG":        

        filename_download = "Grafo.png"

    
        return render_template("graph.html", titulo = "Arquivos",
        graph_image = graph_image, script_image = script_image, 
        code = code_1.script_pair_arcs, name_image = name_image)


@app.route("/getFile")
def getFile():
    global code, filename_download
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()

    return Response(
        code,
        mimetype="py",
        headers={"Content-disposition":
                 f"attachment; filename={filename_download}"})


if __name__ == "__main__":
    app.run()
