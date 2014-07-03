import json, requests


class WordpressAPI(object):

    defaults = {
        'custom_attributes': [
                '_yoast_wpseo_metadesc',
                '_yoast_wpseo_title',
                '_yoast_wpseo_focuskw',
                '_yoast_wpseo_meta-robots-noindex',
                '_yoast_wpseo_meta-robots-nofollow',
                '_yoast_wpseo_redirect',
                '_yoast_wpseo_canonical',
                '_yoast_wpseo_google-plus-description',
                '_yoast_wpseo_opengraph-image',
                '_yoast_wpseo_opengraph-description',
                '_yoast_wpseo_sitemap-html-include',
                '_yoast_wpseo_sitemap-prio',
                '_yoast_wpseo_sitemap-include',
                '_yoast_wpseo_meta-robots-adv',
                '_yoast_wpseo_authorship',
                '_tieroom'
        ]
    }

    def __init__(self, api_root):
        self.api_root = api_root

    def get_recent_posts(self):
        api_call = "%s/get_recent_posts/" % self.api_root
        response = requests.get(api_call)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if (json_response['status'] == 'ok'):
                return json_response['posts']
        return []

    def get_pages(self):
        api_call = "%s/get_page_index/" % self.api_root
        response = requests.get(api_call)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if (json_response['status'] == 'ok'):
                return json_response['pages']
        return []

    def get_page(self, slug):
        api_call = "%s/get_page/?slug=%s&custom_fields=%s" % (self.api_root, slug, ",".join(self.defaults['custom_attributes']))
        response = requests.get(api_call)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if (json_response['status'] == 'ok'):
                return json_response['page']
        return False


    def get_post(self, slug):
        api_call = "%s/get_post/?slug=%s&custom_fields=%s" % (self.api_root, slug, ",".join(self.defaults['custom_attributes']))
        response = requests.get(api_call)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if (json_response['status'] == 'ok'):
                return json_response['post']
        return False