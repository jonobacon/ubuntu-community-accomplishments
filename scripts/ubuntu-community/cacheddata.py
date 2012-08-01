try:
    import cPickle as pickle
except ImportError:
    import pickle
import os
import os.path
import time

from launchpadlib.launchpad import Launchpad


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
                    obj = pickle.load(input)
                    if cls.VERSION == obj.version:
                        if obj.key == key:
                            # Cache hit. All conditions met.
                            return obj

        # Cache miss. Call populate()
        print "Creating %s cache for %s" % (cls.__name__.lower(), str(key))
        obj = cls.populate(key)

        with open(cache_file, 'wb') as output:
            pickle.dump(obj, output)

        return obj
