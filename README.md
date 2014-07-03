Flask + Wordpress via WP JSON API
======================================================

You will need a Wordpress running somewhere with [JSON API](http://wordpress.org/plugins/json-api/) installed.

```
$ git clone git@github.com:hising/flask-wp.git
$ cd flask-wp
$ virtualenv env
$ source env/bin/activate
$ pip install -U -r requirements.txt
```

Open up app.py and edit the path to your WP JSON API:

```
  'cms': {
    'base': "http://cms.yourwpinstall.com/api"
  }
```

```
$ python app.py
```


Then go to [0.0.0.0:3001](http://0.0.0.0:3001)

