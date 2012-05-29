#!/usr/bin/python
import traceback, sys

import datetime
import urllib
try:
    import json
except ImportError:
    import simplejson as json

from accomplishments.daemon import dbusapi
from launchpadlib.launchpad import Launchpad

SERVICE_ROOT = 'http://loco.ubuntu.com/services'

class LocoTeamPortal(object):

    def __init__(self, service_root=None):
        self.service_root = service_root or SERVICE_ROOT
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

try:

    api = dbusapi.Accomplishments()
    f = api.get_extra_information("ubuntu-community", "launchpad-email")
    if bool(f[0]["launchpad-email"]) == False:
        sys.exit(2)
    else:
        email = f[0]["launchpad-email"]

    lp = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = lp.people.getByEmail(email=email)
    if me is None:
        sys.exit(1)

    ltp = LocoTeamPortal()
    attending = ltp.getCollection('events', contact__user__username=me.name, date_begin__lt=datetime.datetime.now())
    if len(attending) > 0:
        sys.exit(0)
    else:
        sys.exit(1)
    
except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
