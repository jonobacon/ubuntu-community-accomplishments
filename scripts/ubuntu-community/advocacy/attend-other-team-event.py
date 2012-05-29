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
    # Get group membership
    member_groups = ltp.getCollection('groups', user__username=me.name)
    member_teams = [member_groups[group_id]['name'] for group_id in member_groups]

    # Get all attended events
    attended_teams = ltp.getCollection('teams', teamevent__attendee__attendee_profile__user__username=me.name, teamevent__attendee__promise="sure", teamevent__date_begin__lt=datetime.datetime.now())

    for team in attended_teams.values():
        # If the user attended an event for a team that they are not a member of, return true
        if team['lp_name'] not in member_teams:
            sys.exit(0)

    sys.exit(1)
    
except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
