from wit import Wit

access_token = "HUWGMDDDJZWMK4FF3AUCRB2VETR5AIXO"

client=Wit(access_token=access_token)
def wit_response(mssg):
    resp = client.message(mssg)
    entity = None
    value = None
    try:
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
    except:
        pass
    return entity, value

