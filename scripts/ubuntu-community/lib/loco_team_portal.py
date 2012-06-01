# Wrapper around the LTP services API
import urllib
try:
    import json
except ImportError:
    import simplejson as json

DEFAULT_SERVICE_ROOT = 'http://loco.ubuntu.com/services'

class LocoTeamPortal(object):

    def __init__(self, service_root=None):
        self.service_root = service_root or DEFAULT_SERVICE_ROOT
        self.cache = {}
        
    def clearCache(self, resource=None):
        if resource is None:
            self.cache = {}
        elif self.cache.has_key(resource):
            self.cache[resource] = {}
        
    # Generic, caching Collection
    def getCollection(self, resource, id_field='id', **kargs):
        if not self.cache.has_key(resource):
            self.cache[resource] = {}
        url = '/'.join([self.service_root, resource, ''])
        if len(kargs) > 0:
            url = '?'.join([url, urllib.urlencode(kargs)])
        s = urllib.urlopen(url)
        col = dict([(o[id_field], o) for o in json.load(s)])
        self.cache[resource].update(col)
        return col

    # Generic, cacheable Entity
    def getEntity(self, resource, entity_id):
        if not self.cache.has_key(resource):
            self.cache[resource] = {}
        if not self.cache[resource].has_key(entity_id):
            url = '/'.join([self.service_root, resource, str(entity_id)])
            s = urllib.urlopen(url)
            self.cache[resource][entity_id] = json.load(s)
        return self.cache[resource][entity_id]

