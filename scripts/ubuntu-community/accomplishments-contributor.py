#!/usr/bin/python
import traceback, sys

from accomplishments.daemon import dbusapi
from launchpadlib.launchpad import Launchpad

try:
    api = dbusapi.Accomplishments()
    print "AAAAAAAAAAAAA"
    f = api.get_extra_information("ubuntu-community", "launchpad-email")
    if bool(f[0]["launchpad-email"]) == False:
        sys.exit(4)
    else:
        email = f[0]["launchpad-email"]

    l = Launchpad.login_anonymously(
        'ubuntu-community accomplishments', 'production')
    me = l.people.getByEmail(email=email)
    if me == None:
        sys.exit(1)
    else:
        # Get user's launchpadID
        name = me.name
        print name
        if name == "jonobacon":
            # A special case for someone who wrote lots of accomplishments, but
            # never have requested a MP :-) Such anomalies will never happen
            # anymore, so this condition actually can be hard-coded. 
            sys.exit(0)
        
        # Get ubuntu-community-accomplishments project
        uca = l.projects['ubuntu-community-accomplishments']
        # Access it's trunk series
        ucatrunk = uca.getSeries(name='trunk')
        # Get trunk branch
        ucab = ucatrunk.branch
        # Look for all MP's that have been merged
        mps = ucab.getMergeProposals(status='Merged')
        
        for mp in mps:
            # If it was me who requested this merge...
            if mp.registrant.name == name:
                # Successful!
                sys.exit(0)
                
        # Merged MP's for this user were not found.
        sys.exit(1)
        
except SystemExit, e:
    sys.exit(e.code)
except:
    traceback.print_exc()
    sys.exit(2)
