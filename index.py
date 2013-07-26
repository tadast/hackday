import json
import sys

SOLR_URL = "http://localhost:8983/solr/update/json"


with open("config/schema_mapper.json") as f:
    map = json.loads(f.read())


def tweets():
    with open(sys.argv[1]) as f:
        return json.loads(f.read())


def value_for_path(path, tweet):
    value = tweet
    for f in path.split("/"):
        if isinstance(value, list):
            return [v[f] for v in value]
        if value is None:
            return None
        try:
            value = value[f]
        except TypeError, e:
            print f
            print path
            raise SystemExit

    return value



for tweet in tweets():
    doc = {}
    for path, field in map.iteritems():
        value = value_for_path(path, tweet)
        doc[field] = value
    print doc



