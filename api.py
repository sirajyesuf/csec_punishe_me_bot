import requests
import json

base_url = "http://127.0.0.1:8000/api/bot/12345"

headers = {

    'Accept':'application/json',
    'Content-Type':'application/json'
}


def get_user_info(telegram_user_id):
    url = base_url +"/users/{}".format(telegram_user_id)
    r = requests.get(url=url,headers=headers)
    if r.status_code == 200:
        for role in r.json()['data']['roles']:
            if role['short_title'] == "DC":
                return 1
    if r.status_code == 404:
        return 0



def search_user(key_word=None,url=None):
    _url=''
    if key_word:
        _url = base_url +"/users/search/user?key={}".format(key_word)
    if url:
        _url = url
    r = requests.get(url=_url,headers=headers)
    print("at search",r.json())

    if(len(r.json())):
        return r.json()
    else:
        return 0




def punishement_record(payload):
    url = base_url + "/users/punishe"
    r = requests.post(url=url,data=json.dumps(payload),headers=headers)
    print("punished",r.json())

