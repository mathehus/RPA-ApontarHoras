from flask import Flask,request,jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def homepage():
    # return render_template("index.html")
    return 'A API está no ara' 

@app.route('/webhooks', methods=['GET'])
def webhooks():
    mode = request.args.get('hub.mode')
    challenge = request.args.get('hub.challenge')
    verify_token = request.args.get('hub.verify_token')

    return challenge

@app.route('/webhooks', methods=['POST'])
def webhooksPost():
    _json = request.json
    try:
        menssagem = _json['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

        if menssagem == 'Apontar Horas':
            chamar = "robo"
            print("robo")
            #Validar campos
            return "200"
        else:
             
            url = "https://graph.facebook.com/v14.0/101101909440708/messages"
            
            headers = {"Content-Type": "application/json; charset=utf-8", "Authorization" : "Bearer EAALVmdug7uMBAPfV18nvkifWp3vpWQ8LfQ6rjdBFrOd0xTfDjaZArIrdzi97emmuX30q8ANr1SdCZAoKlqTLGRqNkZCKiNel7ZCofnfm1fR6TljzX7LmjFLpB6jgPMa4ZCC2HjWKr8nv4kES97y6HEAc4Atz4imUE5mV28nZCEJQ1IuxM2dnXR"}
            
            data = {
                "messaging_product": "whatsapp",
                "to": "5511962583347",
                "type": "template",
                "template": {
                    "name": "timesheet",
                    "language": {
                    "code": "pt_BR"
                    }
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            return "500"
    except:
        url = "https://graph.facebook.com/v14.0/101101909440708/messages"
            
        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization" : "Bearer EAALVmdug7uMBAPfV18nvkifWp3vpWQ8LfQ6rjdBFrOd0xTfDjaZArIrdzi97emmuX30q8ANr1SdCZAoKlqTLGRqNkZCKiNel7ZCofnfm1fR6TljzX7LmjFLpB6jgPMa4ZCC2HjWKr8nv4kES97y6HEAc4Atz4imUE5mV28nZCEJQ1IuxM2dnXR"}
            
        data = {
            "messaging_product": "whatsapp",
             "to": "5511962583347",
             "type": "template",
             "template": {
                "name": "timesheet",
                 "language": {
                "code": "pt_BR"
                }
            }
        }

        response = requests.post(url, headers=headers, json=data)
        return "500"
         #mandar erro pro wpp  




   

