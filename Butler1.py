#1st code prototype..


import os,sys
import requests
from flask import Flask, request
import json
from random import random, choice

page_access_token="EAAcRRBn2MAoBAAjPXMsfEQcmGavAmMdGIESnSJyxIiPTGSkY5EO9ZCRk38Cm71mjGFbiumO22tmx4yUWRi4LgANPPSuk6RerMFznmbCrsJhKYrjDCHyEI0QLng6lUZBxrKwR89ZBzpehtq4jxlgaAKZBDjZBSPOzRxzKUNQZAiMR7jrZAQ0hEAv"
chatbot=Flask(__name__)                                               #Flask object

@chatbot.route('/', methods=['GET'])                                 #This route works for the verification of user..
def verify():
    print("Handling verification...")
    if request.args.get('hub.verify_token', '')=='Butler':
        print("Verified!!")
        return request.args.get("hub.challenge",'')
    else:
        print("Wrong request!!")
        return "error!!"


@chatbot.route('/', methods=['POST'])                                #This works for message posting and request..
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
                        send_message(s_id, str(messaging_text))
                    except:
                        send_message(s_id, "Sorry!! Couldn't understand that..")

                    if things.get("delivery"):
                        log("message delivered..")
                    elif things.get("optin"):
                        pass
                    elif things.get("postback"):
                        pass
    return 'ok', 200                                    #ok 200 response for successful feedback..




def send_message(r_id, messaging_text):                      #These are the parameters required for communication with with messenger API..
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
            "text": str(messaging_text)
        }
    })
    r = requests.post("https://graph.facebook.com/v2.12/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):
    print(message)
    sys.stdout.flush()

if __name__=="__main__":
    chatbot.run(debug=True, port=5000)