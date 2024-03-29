from flask import Flask,request,jsonify
import requests
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os

app = Flask(__name__)

chaveApontamento = False

def robo(arrayMenssagem):
    try:
        email = arrayMenssagem[0]
        senha = arrayMenssagem[1]
      
        op = webdriver.ChromeOptions()
        op.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
        op.add_argument("--headless")
        op.add_argument("--no-sandbox")
        op.add_argument("--disable-dev-sh-usage")
        
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)
    
        print("chamou robo")
        #logando
        driver.get('https://app.onergy.com.br/')
        time.sleep(3)
        driver.find_element('name', 'login').send_keys(email)
        driver.find_element('name', 'password').send_keys(senha)
        driver.find_element('xpath', '//*[@id="signUpForm"]/div[2]/div[4]/button').click()
        time.sleep(2)
        #Time Sheet Grid
        driver.get('https://app.onergy.com.br/#/internal-feed/000b8d14-e7c1-4a3f-9c47-0674103fad08/Time-sheet/false/false/form-feed/000b8d14-e7c1-4a3f-9c47-0674103fad08/Time-sheet')
        time.sleep(3)

        #Time Sheet prenchendo campos
        data_apontar = arrayMenssagem[2]
        projeto_apontar = arrayMenssagem[3]
        atividade_desc = arrayMenssagem[6]
        horas_apontar = arrayMenssagem[4]
        horas_adicionais_apontar = arrayMenssagem[5]


        #data do apontamento
        elem = driver.find_element('id', 'data').click()
        #ActionChains para acionar keybrod 
        act = ActionChains(driver)
        act.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        elem = driver.find_element('id', 'data').send_keys(data_apontar)

        
        #tipo de Atividade REF
        tipoAtividade = driver.find_element('xpath', '/html/body/app-root/app-admin/div/div[2]/div/div/div/div/div/div/app-form-feed/div/div/app-card/div/div/div/form/div[5]/app-paged-dropdown/div/ng-select/div/div/div[2]/input').send_keys('Projeto')
        time.sleep(2)
        act.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        act.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

        #Área trabalhada(CCusto)
        tipoAtividade = driver.find_element('xpath', '/html/body/app-root/app-admin/div/div[2]/div/div/div/div/div/div/app-form-feed/div/div/app-card/div/div/div/form/div[7]/app-paged-dropdown/div/ng-select/div/div/div[2]/input').send_keys('PROJETOS')
        time.sleep(2)
        act.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        act.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

        #Projeto 
        tipoAtividade = driver.find_element('xpath', '/html/body/app-root/app-admin/div/div[2]/div/div/div/div/div/div/app-form-feed/div/div/app-card/div/div/div/form/div[11]/app-paged-dropdown/div/ng-select/div/div/div[2]/input').send_keys(projeto_apontar)
        time.sleep(3)
        act.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        act.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()


        #Campos - Horas, Atividade e Horas adicionais 
        driver.find_element('id', 'atividade').send_keys(atividade_desc)
        driver.find_element('id', 'horas').send_keys(horas_apontar)
        driver.find_element('id', 'horas_adicionais').send_keys(horas_adicionais_apontar)

        #Save do Registro
        driver.find_element('xpath', '/html/body/app-root/app-admin/div/div[2]/div/div/div/div/div/div/app-form-feed/div/div/app-card/div/div/div/form/div[17]/div/div/button[2]').click()
        time.sleep(2)
        print("apontou")
        chaveApontamento = False
        return "200"
        
    except: 
        print("robo except")
        return "500"

def introducaoRobo(menssagem):
    retorno = "500"
    try:
        arrayMenssagem = menssagem.split(";")
        if(len(arrayMenssagem) == 7):
          rpa = robo(arrayMenssagem)
          if(rpa == "200"):
            retorno = "200"
        return retorno
    except:
        print("introducaoRobo except")
        return retorno

   


@app.route('/')
def homepage():
    # return render_template("index.html")
    return 'A API está no Ar' 

@app.route('/webhooks', methods=['POST'])
def webhooksPost():
    _json = request.json
    print(_json)
    try:
        if(_json['entry'][0]['changes'][0]['value']['messages']):
            try:
                menssagem = _json['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                #teste
                # menssagem = "matheus.santos@keeptrue.com;Mq210976;01/09/2022;OXITENO;8;0;Desenvolvimento fluxo de NFSE e CTE"

                chaveApontamento = True
                if menssagem != None and menssagem != "Help" :
                    
                    retornoRobo = ""
                    if(chaveApontamento):
                       retornoRobo = introducaoRobo(menssagem)
                    
                    if(retornoRobo == "200"):
                        url = "https://graph.facebook.com/v14.0/101101909440708/messages"
                        
                        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization" : "Bearer EAALVmdug7uMBAPfV18nvkifWp3vpWQ8LfQ6rjdBFrOd0xTfDjaZArIrdzi97emmuX30q8ANr1SdCZAoKlqTLGRqNkZCKiNel7ZCofnfm1fR6TljzX7LmjFLpB6jgPMa4ZCC2HjWKr8nv4kES97y6HEAc4Atz4imUE5mV28nZCEJQ1IuxM2dnXR"}
                        
                        data = {
                            "messaging_product": "whatsapp",
                            "to": "5511962583347",
                            "type": "template",
                            "template": {
                                "name": "sucesso",
                                "language": {
                                "code": "pt_BR"
                                }
                            }
                        }
              
                        response = requests.post(url, headers=headers, json=data)
                        print("200")
                        return "200"
                    else:

                        url = "https://graph.facebook.com/v14.0/101101909440708/messages"
                        
                        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization" : "Bearer EAALVmdug7uMBAPfV18nvkifWp3vpWQ8LfQ6rjdBFrOd0xTfDjaZArIrdzi97emmuX30q8ANr1SdCZAoKlqTLGRqNkZCKiNel7ZCofnfm1fR6TljzX7LmjFLpB6jgPMa4ZCC2HjWKr8nv4kES97y6HEAc4Atz4imUE5mV28nZCEJQ1IuxM2dnXR"}
                        
                        data = {
                            "messaging_product": "whatsapp",
                            "to": "5511962583347",
                            "type": "template",
                            "template": {
                                "name": "error",
                                "language": {
                                "code": "pt_BR"
                                }
                            }
                        }
                        print("ELSE DO 200")
                        
                        response = requests.post(url, headers=headers, json=data)
                        
                        return "200"

                elif(menssagem == "Help" or menssagem == "help"):

                    url = "https://graph.facebook.com/v14.0/101101909440708/messages"
                    
                    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization" : "Bearer EAALVmdug7uMBAPfV18nvkifWp3vpWQ8LfQ6rjdBFrOd0xTfDjaZArIrdzi97emmuX30q8ANr1SdCZAoKlqTLGRqNkZCKiNel7ZCofnfm1fR6TljzX7LmjFLpB6jgPMa4ZCC2HjWKr8nv4kES97y6HEAc4Atz4imUE5mV28nZCEJQ1IuxM2dnXR"}
                    
                    data = {
                        "messaging_product": "whatsapp",
                        "to": "5511962583347",
                        "type": "template",
                        "template": {
                            "name": "help",
                            "language": {
                            "code": "pt_BR"
                            }
                        }
                    }
                    
                    response = requests.post(url, headers=headers, json=data)
                    return "500"
                    #mandar erro pro wpp    
                else:
                    url = "https://graph.facebook.com/v14.0/101101909440708/messages"
                    
                    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization" : "Bearer EAALVmdug7uMBAPfV18nvkifWp3vpWQ8LfQ6rjdBFrOd0xTfDjaZArIrdzi97emmuX30q8ANr1SdCZAoKlqTLGRqNkZCKiNel7ZCofnfm1fR6TljzX7LmjFLpB6jgPMa4ZCC2HjWKr8nv4kES97y6HEAc4Atz4imUE5mV28nZCEJQ1IuxM2dnXR"}
                    
                    data = {
                        "messaging_product": "whatsapp",
                        "to": "5511962583347",
                        "type": "template",
                        "template": {
                            "name": "error",
                            "language": {
                            "code": "pt_BR"
                            }
                        }
                    }
                    
                    response = requests.post(url, headers=headers, json=data)
                    return "500"
                    #mandar erro pro wpp  
                    
            except:
                url = "https://graph.facebook.com/v14.0/101101909440708/messages"
                    
                headers = {"Content-Type": "application/json; charset=utf-8", "Authorization" : "Bearer EAALVmdug7uMBAPfV18nvkifWp3vpWQ8LfQ6rjdBFrOd0xTfDjaZArIrdzi97emmuX30q8ANr1SdCZAoKlqTLGRqNkZCKiNel7ZCofnfm1fR6TljzX7LmjFLpB6jgPMa4ZCC2HjWKr8nv4kES97y6HEAc4Atz4imUE5mV28nZCEJQ1IuxM2dnXR"}
                    
                data = {
                    "messaging_product": "whatsapp",
                    "to": "5511962583347",
                    "type": "template",
                    "template": {
                        "name": "error",
                        "language": {
                        "code": "pt_BR"
                        }
                    }
                }
                print("excpet principal de não localizou caminho")
                return "500"
                #mandar erro pro wpp  
        else:
            return "500"
    except:
        return "500"
