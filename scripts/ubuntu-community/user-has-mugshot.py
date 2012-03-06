#!/usr/bin/python

import traceback, sys
from accomplishments.daemon import dbusapi

try:
	import json, sys, os, pwd, subprocess
	from ubuntuone.couch import auth
	from launchpadlib.launchpad import Launchpad

	api = dbusapi.Accomplishments()
	f = api.getExtraInformation("ubuntu-community", "launchpad-email")

	if bool(f[0]["launchpad-email"]) == False:
		sys.exit(4)
	else:
		email = f[0]["launchpad-email"]

	l=Launchpad.login_anonymously('ubuntu-community accomplishments','production')
	me=l.people.getByEmail(email=email)

	if me == None:
		sys.exit(1)
	else:
		try:
			mugshot = me.mugshot
			mugshot_handle = mugshot.open()
			sys.exit(0)
		except:
			sys.exit(1)

except SystemExit, e:
	sys.exit(e.code)
except:
	traceback.print_exc()
	sys.exit(2)

