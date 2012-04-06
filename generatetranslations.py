import glob
import os
from random import randint
import ConfigParser
import subprocess

print "starting up"

files = glob.glob("accomplishments/*/en/*")

translatedsections = [{"title" : "Enter a title for the accomplishment"},
    { "description" : "Add a single line description" },
    { "summary" : "Enter a summary" },
    { "steps" : "Add the steps" },
    { "links" : "Add the links" },
    { "help" : "Add the help" }]
    
print translatedsections

generatedaccomplishmentsdir = "generated/accomplishments"
podir = "generated/po"

if not os.path.exists(generatedaccomplishmentsdir):
    os.makedirs(generatedaccomplishmentsdir)

if not os.path.exists(podir):
    os.makedirs(podir)
    
potfilesin = open(os.path.join(podir, "POTFILES.in"), "w")

for f in files:
    accomplishmentname = os.path.split(f)[1].split(".")[0]
    tempfile = open(os.path.join(generatedaccomplishmentsdir, accomplishmentname + ".c"), "w")
    config = ConfigParser.RawConfigParser()
    config.read(f)
    items = config.items("accomplishment")
    print "[accomplishment]\n"
    tempfile.write("[accomplishment]\n")
    for i in items:
        for sec in translatedsections:
            if i[0] in sec.keys():
                comment = "/// " + sec.values()[0] + "\n"
                tempfile.write(comment)
                wr = "_(\"" + accomplishmentname + "_" + i[0] + "\")\n"
                tempfile.write(wr)
                print wr
    tempfile.close()

    # write POTFILES.in
    potfilesin.write(os.path.join("accomplishments", accomplishmentname + ".c\n"))

potfilesin.close()

os.chdir(podir)
print "generating POT file"
subprocess.call(["intltool-update", "-pot", "--gettext-package=template"])
