from launchpadlib.launchpad import Launchpad

from cacheddata import CachedData


class LPData(CachedData):
    """Force launchpadlib to evaluate some of the lazy data it knows about a
       user and store it in member variables.
    """
    # If you add any fields to the LPData object, increment this number to
    # ensure the cache is invalidated on update
    VERSION = 1

    def __init__(self):
        super(LPData, self).__init__()
        # This is a list of all teams the user is a direct or indirect member
        self.super_teams = []
        # Store a list of teams user is a direct member of
        self.direct_teams = []
        self.name = None

    @classmethod
    def populate(cls, email):
        """Return a new LPData object populated from the key, which is the
        user's email address.
        """
        data = LPData()
        lp = Launchpad.login_anonymously('ubuntu-community accomplishments',
                                         'production')
        user = lp.people.getByEmail(email=email)
        if user is None:
            return data
        data.name = user.name
        data.key = str(email)
        data.super_teams = [i.name for i in user.super_teams]
        # Direct teams are temporarily disabled, since no script would make use of it.
        # If you are adding a new script that requires this bit of data, uncomment the
        # following line, and remember to increment VERSION
        ### data.direct_teams = [i.team.name for i in user.memberships_details]
        return data
