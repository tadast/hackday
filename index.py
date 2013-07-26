import json
import sys
import urllib2

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

    solrReq = urllib2.Request(SOLR_URL, json.dumps([doc]))
    solrReq.add_header("Content-Type", "application/json")
    solrPoster = urllib2.urlopen(solrReq)
    response = solrPoster.read()
    solrPoster.close()
