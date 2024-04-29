
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask import jsonify
from apps.home.sdr_fm_scanner import scan 
from apps.home.funciones import fm_audio
import json
import time





@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
    

@blueprint.route('/start_ppm', methods=['POST'])
@login_required
def start_bot():
    if request.method == "POST":
        for arg in request.json:
            if arg !="city" and arg != "threshold":
                request.json[arg] = int(request.json[arg])
            elif arg == "threshold":
                request.json[arg] = float(request.json[arg])
#-------------------DEMODULACION EN FM DE LAS SEÑALES ENCONTRADAS-----------------------#
        lista_frecuencias_encontradas=scan(request.json,plot_waterfall=True)
        for signal in lista_frecuencias_encontradas:
            samples = fm_audio(fc=int(signal["freq"]), plot=True)

    response_message = f"mensaje enviado."
    return jsonify({'message': response_message})



@blueprint.route('/test_cpu', methods=['GET'])
def test_cpu():
    start=time.time()
    for i in range(1200):
        a=i**2
        time.sleep(0.05)
        print(a)
    print(f"el tiempo que se demora el codigo en correr es {time.time()-start}")
    response_message = f"mensaje enviado."
    return jsonify({'time': time.time()-start})