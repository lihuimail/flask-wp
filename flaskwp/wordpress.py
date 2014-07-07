import json, requests
import urllib

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

    def get_response(self, endpoint, params = {}, method = 'GET', data = {}):

        url = "%s/%s/?%s" % (self.api_root, endpoint, urllib.urlencode(params))

        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            response = requests.post(url, data=data)

        if response.status_code == 200:
            json_response = json.loads(response.text)
            if (json_response['status'] == 'ok'):
                return self.add_custom_attributes_to_response(json_response)

        return False

    def get_recent_posts(self, count = 30, page = 1, post_type = 'post'):
        params = {
            'count': count,
            'page': page,
            'post_type': post_type
        }
        return self.get_response('get_recent_posts', params)

    def get_posts(self, count = 30, page = 1, post_type = 'post'):
        params = {
            'count': count,
            'page': page,
            'post_type': post_type
        }
        return self.get_response('get_posts', params)

    def get_date_posts(self, date, count=30, page=1, post_type='post'):
        params = {
            'date': date,
            'count': count,
            'page': page,
            'post_type': post_type
        }
        return self.get_response('get_date_posts', params)

    def get_page_index(self, count = 30, page = 1, post_type = 'page'):
        params = {
            'count': count,
            'page': page,
            'post_type': post_type
        }
        return self.get_response('get_page_index', params)

    def get_date_index(self):
        return self.get_response('get_date_index')

    def get_category_index(self, parent=-1):
        params = {}
        if parent > 0:
            params['parent'] = parent
        return self.get_response('get_category_index', params=params)

    def get_tag_index(self):
        return self.get_response('get_tag_index')

    def get_author_index(self):
        return self.get_response('get_author_index')

    def get_page(self, slug, post_type = "page"):
        params = {
            'slug': slug,
            'custom_fields': ",".join(self.defaults['custom_attributes']),
            'post_type': post_type
        }
        return self.get_response('get_page', params)

    def get_post(self, slug = "", post_type = "post", post_id = -1):

        params = {
            'custom_fields': ",".join(self.defaults['custom_attributes']),
            'post_type': post_type
        }

        if slug != "":
            params['slug'] = slug

        if post_id > -1:
            params['id'] = post_id

        return self.get_response('get_post', params)

    def get_category_posts(self, category_slug, count = 30, page = 1, post_type = 'post'):
        params = {
            'slug': category_slug,
            'count': count,
            'page': page,
            'post_type': post_type
        }
        return self.get_response('get_category_posts', params)

    def get_tag_posts(self, tag_slug, count = 30, page = 1, post_type = 'post'):
        params = {
            'slug': tag_slug,
            'count': count,
            'page': page,
            'post_type': post_type
        }
        return self.get_response('get_tag_posts', params)

    def get_author_posts(self, author_slug, count = 30, page = 1, post_type = 'post'):
        params = {
            'slug': author_slug,
            'count': count,
            'page': page,
            'post_type': post_type
        }
        return self.get_response('get_author_posts', params)

    def get_search_results(self, query, count = 30, page = 1, post_type='post'):
        params = {
            'search': query,
            'count': count,
            'page': page,
            'post_type': post_type
        }
        return self.get_response('get_search_results', params)


    def get_nonce(self, controller, method):
        params = {
            'controller': controller,
            'method': method
        }
        return self.get_response('get_nonce', params)

    def create_post(self, post):
        nonce = self.get_nonce(controller='posts', method='create_post')
        post['nonce'] = nonce['nonce']
        return self.get_response('posts/create_post', method='POST', data=post)

    def update_post(self, slug, post):
        nonce = self.get_nonce(controller='posts', method='update_post')
        post['nonce'] = nonce['nonce']

        params = {
            'slug': slug
        }

        return self.get_response('posts/update_post', method='POST', params=params, data=post)


    def delete_post(self, slug):
        nonce = self.get_nonce(controller='posts', method='delete_post')

        params = {
            'slug': slug
        }

        data = {
            'nonce': nonce['nonce']
        }

        return self.get_response('posts/delete_post', method='POST', params=params, data=data)

    def submit_comment(self, post_id, name, email, content, url = ""):
        data = {
            'name': name,
            'email': email,
            'content': content,
            'url': url
        }

        params = {
            'post_id': post_id
        }

        return self.get_response('respond/submit_comment', params=params, method='POST', data=data)
