import json, requests


class WordpressAPI(object):

    def __init__(self, api_root):
        self.api_root = api_root

    def get_page(self, slug):
        api_call = "%s/get_page/?slug=%s" % (self.api_root, slug)
        response = requests.get(api_call)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if (json_response['status'] == 'ok'):
                return json_response['page']
        return False
