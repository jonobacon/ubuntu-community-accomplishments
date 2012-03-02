#!/usr/bin/python

import traceback, sys
import libaccomplishments

try:
	import json, sys, os, pwd, subprocess
	from ubuntuone.couch import auth
	from launchpadlib.launchpad import Launchpad

	libaccom = libaccomplishments.Accomplishments()

	f = libaccom.getExtraInformation("ubuntu-community", "launchpad-email")

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
			print "Mugshot found"
			sys.exit(0)
		except:
			"Mugshot not found"
			sys.exit(1)

except SystemExit, e:
	sys.exit(e.code)
except:
	traceback.print_exc()
	sys.exit(2)

