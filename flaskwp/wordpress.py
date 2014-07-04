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
                '_yoast_wpseo_authorship'
        ]
    }

    def __init__(self, api_root):
        self.api_root = api_root

    def add_custom_attributes_to_response(self, response):
        """
        TODO: Convert to Python from PHP:

        if (array_key_exists('custom_fields', $this->page) && is_array($this->page['custom_fields'])) {
                $this->custom_fields = $this->page['custom_fields'];

                foreach ($this->custom_attributes as $custom_attribute) {
                    if ($this->hasCustomAttribute($custom_attribute)) {
                        $keyName = str_replace('_yoast_wpseo_', '', $custom_attribute);
                        $this->page[$keyName] = $this->custom_fields[$custom_attribute][0];
                    }
                }
            }

        """
        return response

    def get_response(self, url, success_key):
        response = requests.get(url)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if (json_response['status'] == 'ok'):
                return self.add_custom_attributes_to_response(json_response[success_key])
        return False

    def get_recent_posts(self, count = 30, page = 1, post_type = 'post'):
        return self.get_response("%s/get_recent_posts/?count=%s&page=%s&post_type=%s" % (self.api_root, count, page, post_type), 'posts')

    def get_posts(self, count = 30, page = 1, post_type = 'post'):
        return self.get_response("%s/get_posts/?post_type=%s&count=%s&page=%s" % (self.api_root, post_type, count, page), 'posts')

    def get_pages(self, post_type = 'page'):
        return self.get_response("%s/get_page_index/?post_type=%s" % (self.api_root, post_type), 'pages')

    def get_page(self, slug, post_type = "page"):
        api_call = "%s/get_page/?slug=%s&custom_fields=%s&post_type=%s" % (self.api_root, slug, ",".join(self.defaults['custom_attributes']), post_type)
        return self.get_response(api_call, 'page')

    def get_post(self, slug, post_type = "post"):
        api_call = "%s/get_post/?slug=%s&custom_fields=%s&post_type=%s" % (self.api_root, slug, ",".join(self.defaults['custom_attributes']), post_type)
        return self.get_response(api_call, 'post')

    def get_category_posts(self, category_slug, count = 30, page = 1, post_type = 'post'):
        api_call = "%s/get_category_posts/?slug=%s&post_type=%s&count=%s&page=%s" % (self.api_root, category_slug, post_type, count, page)
        return self.get_response(api_call, 'posts')

    def get_tag_posts(self, tag_slug, count = 30, page = 1, post_type = 'post'):
        api_call = "%s/get_tag_posts/?slug=%s&post_type=%s&count=%s&page=%s" % (self.api_root, tag_slug, post_type, count, page)
        return self.get_response(api_call, 'posts')

    def get_author_posts(self, author_slug, count = 30, page = 1, post_type = 'post'):
        api_call = "%s/get_author_posts/?slug=%s&post_type=%s&count=%s&page=%s" % (self.api_root, author_slug, post_type, count, page)
        return self.get_response(api_call, 'posts')

    def get_search_results(self, query, count = 30, page = 1, post_type='post'):
        return []

    def get_nonce(self, controller, method):
        return {}

    def create_post(self, post, nonce):
        return {}

    def update_post(self, slug, post, nonce):
        return {}

    def delete_post(self, slug, nonce):
        return {}

    def submit_comment(self, post_id, name, email, content):
        """
        Optional arguments
            redirect - redirect instead of returning a JSON object
            redirect_ok - redirect to a specific URL when the status value is ok
            redirect_error - redirect to a specific URL when the status value is error
            redirect_pending - redirect to a specific URL when the status value is pending

        """
        return {}