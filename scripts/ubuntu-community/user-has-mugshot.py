#!/usr/bin/python

import traceback, sys
from accomplishments.daemon import dbusapi
from launchpadlib.launchpad import Launchpad

try:
  api = dbusapi.Accomplishments()
  f = api.get_extra_information("ubuntu-community", "launchpad-email")
  
  if bool(f[0]["launchpad-email"]) == False:
    sys.exit(4)
  else:
    email = f[0]["launchpad-email"]
    
  l=Launchpad.login_anonymously('ubuntu-community accomplishments',
                                'production')
  
  me=l.people.getByEmail(email=email)
  
  if me == None:
    sys.exit(1)
  
  try:
    mugshot = me.mugshot
    mugshot_handle = mugshot.open()
  except:
    sys.exit(1)
    
  sys.exit(0)

except SystemExit, e:
	sys.exit(e.code)
except:
	traceback.print_exc()
	sys.exit(2)

