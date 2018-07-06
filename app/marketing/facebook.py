from os import getenv
from os.path import dirname, abspath, join

import facebook
from clint.textui import colored


def api():
    cfg = { 'page_id' : getenv('FACEBOOK_PAGE_ID'), 'access_token' : getenv('FACEBOOK_PAGE_ACCESS_TOKEN') }
    return facebook.GraphAPI(cfg['access_token'])

def post(api, content, attachment):
    try:
        api.put_wall_post(message=content, attachment=attachment)
    except Exception as err:
        print(colored.red(err))
