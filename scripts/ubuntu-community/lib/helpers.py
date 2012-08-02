try:
    import cPickle as pickle
except ImportError:
    import pickle
    
import os
import os.path
import time
import traceback
import gzip
import simplejson
import urllib2
import StringIO
try:
    import json
except ImportError:
    import simplejson as json
    
from launchpadlib.launchpad import Launchpad as LaunchpadLib


# Ten minutes, a bit smaller then default interval for running scripts
CACHE_LIFESPAN = 10*60


class CachedData(object):
    """CachedData is a parent object which allows inheriting objects to perform
       some costly fetch operation and cache the output.

       Child objects should create a populate(key) method. This method will
       perform the costly retrieval and store the data in member variables.
       Calling the fetch(key) classmethod will check the cache for this data
       and return it if the following conditions are met:

       1) The cache file exists
       2) The cache is not stale (see the CACHE_LIFESPAN module global)
       3) The key in the cache matches the requested key
       4) The version of data in the cache is equal to the defined class
          VERSION

       If a condition is not met, the populate(key) method is called to fetch
       the data and it is stored in the cache.
    """
    def __init__(self):
        self.key = None
        self.version = self.VERSION

    def __repr__(self):
        cls = self.__class__
        return '<%s.%s object - %r>' % (cls.__module__,
                                        cls.__name__,
                                        self.name)

    @classmethod
    def fetch(cls, key):
        """Fetch data from the cache or from a costly source.

           This will call the populate(key) method on derived classes. That
           method should return a populated object of the derived class.
           This method will then store the object in the cache for later
           retrieval.
        """
        # basedir spec says to check $XDG_CACHE_HOME for the location of
        # the user cache dir first. Failing that, it's just ~/.cache.
        try:
            cache_dir = os.environ['XDG_CACHE_HOME']
        except KeyError:
            cache_dir = '~/.cache'

        cache_dir = os.path.expanduser(cache_dir)
        cache_dir = os.path.join(cache_dir, 'accomplishments')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        cache_file = os.path.join(cache_dir, cls.__name__.lower())

        if os.path.exists(cache_file):
            mtime = os.path.getmtime(cache_file)
            if abs(time.time() - mtime) < CACHE_LIFESPAN:
                with open(cache_file, 'rb') as input:
                    try:
                        obj = pickle.load(input)
                        if cls.VERSION == obj.version:
                            if obj.key == key:
                                # Cache hit. All conditions met.
                                return obj
                    except:
                        print "Not using the current cache as it seems to be broken."
                        # broken cache
                        pass

        # Cache miss. Call populate()
        print "Creating %s cache for %s..." % (cls.__name__.lower(), str(key))
        obj = cls.populate(key)
        
        with open(cache_file, 'wb') as output:
            pickle.dump(obj, output)

        return obj


class Launchpad(CachedData):
    """
    This class provides an easy access to some data about a Launchpad user,
    which may be used in all accomplishment scripts. Currently it provides
    with a list of teams this user belongs to (including teams that belong
    to teams). This data is cached, to improve effectiveness.
    
    Example usage:
        >>> from helpers import Launchpad
        >>> me = Launchpad.fetch('rafalcieslak256@ubuntu.com')
        >>> me.super_teams
        ["locoteams","ubuntu-pl","ubuntu-accomplishment-contributors","ubuntu-users", ... ]
        
    """
    # If you add any fields to the Launchpad object, increment this number to
    # ensure the cache is invalidated on update
    VERSION = 1

    def __init__(self):
        super(Launchpad, self).__init__()
        # This is a list of all teams the user is a direct or indirect member
        self.super_teams = []
        # Store a list of teams user is a direct member of
        self.direct_teams = []
        self.name = None

    @classmethod
    def populate(cls, email):
        # Return a new LPData object populated from the key, which is the
        # user's email address.
        data = Launchpad()
        lp = LaunchpadLib.login_anonymously('ubuntu-community accomplishments',
                                         'production')
        user = lp.people.getByEmail(email=email)
        if user is None:
            return data
        data.name = user.name
        data.key = str(email)
        data.super_teams = [i.name for i in user.super_teams]
        # Direct teams are temporarily disabled, since no script would make use of it.
        # If you are adding a new script that requires this bit of data, uncomment the
        # following line, remove these four lines of comments, and remember to
        # increment VERSION
        ### data.direct_teams = [i.team.name for i in user.memberships_details]
        return data

class AskUbuntu(CachedData):
    """
    This class is meant to be used by accomplishment scripts, as it provides
    easy access to AskUbuntu data concerning given user. Currently it can
    list all badges this user got. This data is cached, to improve
    effectiveness.
    
    Example usage:
        >>> from helpers import AskUbuntu
        >>> me = AskUbuntu.fetch(1234) #userID
        >>> badgeid = 12
        >>> badgeid in me.badges
    """
    # If you add any fields to the AskUbuntu object, increment this number to
    # ensure the cache is invalidated on update
    VERSION = 1

    def __init__(self):
        super(AskUbuntu, self).__init__()
        self.badges = {}

    @classmethod
    def populate(cls, userid):
        # Return a new AskUbuntu object populated from the key, which is the
        # user's ID.
        data = AskUbuntu()
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
        

DEFAULT_SERVICE_ROOT = 'http://loco.ubuntu.com/services'

class LocoTeamPortal(object):
    # Wrapper around the LTP services API

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


