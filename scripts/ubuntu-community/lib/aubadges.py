from launchpadlib.launchpad import Launchpad

from cacheddata import CachedData
    
import traceback
import json
import gzip
import simplejson
import urllib2
import StringIO

class AUBadges(CachedData):
    # If you add any fields to the AUBadges object, increment this number to
    # ensure the cache is invalidated on update
    VERSION = 1

    def __init__(self):
        super(AUBadges, self).__init__()
        self.badges = {}

    @classmethod
    def populate(cls, userid):
        """Return a new AUBadges object populated from the key, which is the
        user's ID.
        """
        data = AUBadges()
        data.key = userid
        
        try:
            badges_req = urllib2.urlopen('http://api.stackexchange.com/2.0/users/%d/badges?pagesize=100&order=asc&sort=name&site=askubuntu&key=zUuJiog6hjENJovHBpM11Q((' % userid)
        except:
            traceback.print_exc()
            return data #Returnning empty values
        
        badges_raw = badges_req.read()

        badges_raw = StringIO.StringIO(badges_raw)
        gzipr = gzip.GzipFile(fileobj=badges_raw)

        badges_raw = gzipr.read()
        badges_data = json.loads(badges_raw)
        
        if len(badges_data['items']) == 0:
            return data
            
        for badge in badges_data['items']:
            if badge['badge_type'] == "named":
                data.badges[badge['badge_id']] = badge['name']
            
        return data
