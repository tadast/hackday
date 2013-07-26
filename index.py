import json
import sys
import urllib2

SOLR_URL = "http://localhost:8983/solr/update/json"
NER_SERVER = "http://localhost:8080/"

def tweets():
    with open(sys.argv[1]) as f:
        return json.loads(f.read())


def value_for_path(path, tweet):
    value = tweet
    for f in path.split("/"):
        if isinstance(value, list):
            return [v[f] for v in value]
        if f == 'coordinates' and value[f] is not None:
            clist = value[f]['coordinates']
            coordinate = "%s,%s" % (clist[1], clist[0])
            return coordinate
        if value is None:
            return None
        try:
            value = value[f]
        except TypeError, e:
            print f
            print path
            raise SystemExit

    return value


def index(doc):
    solrReq = urllib2.Request(SOLR_URL, json.dumps([doc]))
    solrReq.add_header("Content-Type", "application/json")
    solrPoster = urllib2.urlopen(solrReq)
    response = solrPoster.read()
    solrPoster.close()


def extract(text):
    response = urllib2.urlopen(NER_SERVER, text.encode("UTF-8", "ignore"))
    return json.loads(response.read())


with open("config/schema_mapper.json") as f:
    map = json.loads(f.read())

count = 0
for tweet in tweets():
    doc = {}
    count += 1
    for path, field in map.iteritems():
        value = value_for_path(path, tweet)
        doc[field] = value
    for k, v in extract(doc['text']).iteritems():
        doc["ner_%s" % k.lower()] = v
    if count % 1000 == 0:
        print count
    index(doc)
