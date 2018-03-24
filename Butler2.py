#2nd code prototype..

import os,sys
import requests
from flask import Flask, request
import json
from random import random, choice
from utils import wit_response
from pymessenger import Bot

page_access_token="EAACwuoYn284BADWs7CsFWPZBpYUx7xMNFZCh4j9FVmzWRIM5n3IVTIB9UD5eacVwFYXVeaBZCUoSZCy72Befg9CZADZAhem8bQusHZBSUBPj6yhBqL9BcZCZBsIfiZBGsjVMxcR5lVyT0OfJ5xxGV0ksGFkWLcqxnwj9lCbXbusDu1avFDQN7IABms"

chatbot=Flask(__name__)                                              #Flask object
bot= Bot(page_access_token)

@chatbot.route('/', methods=['GET'])                                 #This route works for the verification of user..
def verify():
    print("Handling verification...")
    if request.args.get('hub.verify_token', '')=='Butler':
        print("Verified!!")
        return request.args.get("hub.challenge", '')
    else:
        print("Wrong request!!")
        return "error!!"


@chatbot.route('/', methods=['POST'])
def webhook():
    data=request.get_json()
    log(data)                                                       #To print all message that has been received..
    if data["object"]=="page":                                      #Contains all the dictionaries and lists..
        for entry in data["entry"]:
            for things in entry["messaging"]:

                if things.get("message"):
                    s_id= things["sender"]["id"]                    #Sender id
                    r_id= things["recipient"]["id"]                 #recepient id
                    log("Sender id:"+ s_id)
                    log("Receiver id: "+ r_id)
                    try:
                        messaging_text= things["message"]["text"]          #message
                        entity, value=wit_response(str(messaging_text))
                        response = None
                        if entity == 'foodcourt':
                            response = "I got ya.. Will be right there at {} ".format(str(value))
                            #send_message(s_id, "I got ya.. Will be right there at {} ".format(str(value)))
                        elif entity == 'food_item':
                            response ="You want to have {0}... I'll get you".format(str(value))
                            #send_message(s_id, "You want to have {0}... I'll get you".format(str(value)))
                    except:
                        response="Sorry!! Couldn't understand that.."
                        #send_message(s_id, "Sorry!! Couldn't understand that..")
                    bot.send_text_message(s_id, response)
    else:
        log("->Check your code... no POST handle functioned.")
    return 'ok', 200                                    #ok 200 response for successful feedback..


'''def send_message(r_id, messaging_text):                      #These are the parameters required for communication with with messenger API..
    r_id=str(r_id)
    log("sending message to {recipient}: {text}".format(recipient=r_id, text=messaging_text))

    params = {
        "access_token": page_access_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": r_id
        },
        "message": {
            "text": messaging_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.12/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
'''

def log(message):
    print(message)
    sys.stdout.flush()

if __name__=="__main__":
    chatbot.run(debug=True, port=5000)