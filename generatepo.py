import glob
import os
from random import randint
import ConfigParser
import subprocess

translatedsections = [
    { "title" :
        "A short description of the accomplishment.\n \
        NOTE: Describe this in the past tense as if it has been achieved (e.g. Registered On Launchpad). " },
    { "description" :
        "Add a descriptive single-line summary of the accomplishment." },
    { "summary" :
        "Introduce the accomplishment, explain what the different concepts are that are involved, and provide guidance on how to accomplish it.\n \
        NOTE: Break this into paragraphs by putting each paragraph on a new line. \n \
        FORMATTING ALLOWED: <i> <strong> <tt>" },
    { "steps" :
        "Add a series of step-by-step instructions for how to accomplish this trophy.\n \
        NOTE: Put each step on a new line\n \
        FORMATTING ALLOWED: <i> <strong> <tt>" },
    { "tips" :
        "Add tips and best practise for accomplishing this trophy.\n \
        NOTE: Put each tip on a new line\n \
        FORMATTING ALLOWED: <i> <strong> <tt>" },
    { "pitfalls" :
        "Add things the user should not do when working to accomplish this trophy.\n \
        NOTE: Put each pitfall on a new line\n \
        FORMATTING ALLOWED: <i> <strong> <tt>" },
    { "links" :
        "Add related web addresses (don't include a HTML link).\n \
        NOTE: Put each URL on a new line" },
    { "help" :
        "Add related help resources (e.g. IRC channel names).\n \
        NOTE: Put each help resource on a new line\n \
        FORMATTING ALLOWED: <i> <strong> <tt>" }]
    
generatedaccomplishmentsdir = "generated/accomplishments"
podir = "generated/po"

if not os.path.exists(generatedaccomplishmentsdir):
    os.makedirs(generatedaccomplishmentsdir)

if not os.path.exists(podir):
    os.makedirs(podir)
    
potfilesin = open(os.path.join(podir, "POTFILES.in"), "w")

print "Scanning for files:"

files = {}

collslist = os.listdir("accomplishments")
for collection in collslist:
    colldir = os.path.join("accomplishments",collection)
    cfg = ConfigParser.RawConfigParser()
    cfg.read(os.path.join(colldir,"ABOUT"))
    deflang = cfg.get("general","langdefault")
    deflangdir = os.path.join(colldir,deflang)
    deflangdirlist = os.listdir(deflangdir)
    for item in deflangdirlist:
        itempath = os.path.join(deflangdir,item)
        if os.path.isdir(itempath):
            dislist = os.listdir(itempath)
            for accom in dislist:
                accompath = os.path.join(itempath,accom)
                accID = collection + "/" + accom[:-15]
                print " " + accID
                files[accompath] = accID
        else:
            accID = collection + "/" + item[:-15]
            print " " + accID
            files[itempath] = accID

print "Processing files:"

for f in files:
    accomID = files[f]
    print " ..." + accomID + " (" + str(f) + ")"
    accomID_splitted = accomID.split("/")
    if len(accomID_splitted) == 2:
        # requires a directory
        if not os.path.exists(os.path.join(generatedaccomplishmentsdir,accomID_splitted[0])):
            os.makedirs(os.path.join(generatedaccomplishmentsdir,accomID_splitted[0]))
    tempfile = open(os.path.join(generatedaccomplishmentsdir,accomID + ".c"),"w")
    config = ConfigParser.RawConfigParser()
    config.read(f)
    title = config.get("accomplishment", "title")
    items = config.items("accomplishment")
    tempfile.write("[accomplishment]\n")
    for i in items:
        for sec in translatedsections:
            if i[0] in sec.keys():
                output = "// ACCOMPLISHMENT: " + title + " ('" + i[0] + "' field)\n"
                output = output + "// .\n"
                origitemlines = config.get("accomplishment", i[0]).split("\n")
                origitem = ""
                for l in origitemlines:
                    origitem = origitem + ("// " + l + "\n")

                output = output + ("// ORIGINAL TRANSLATION:\n")
                output = output + (origitem + "\n")
                output = output + "// .\n"
                output = output + "// ----- TRANSLATION INSTRUCTIONS ----- \n"
                for c in sec.values()[0].split("\n"):
                    output = output + ("// " + c + "\n")
                output = output + ("_(\"" + accomID + "_" + i[0] + "\")\n")
                tempfile.write(output)
    tempfile.close()

    # write POTFILES.in
    potfilesin.write(os.path.join("accomplishments", accomID + ".c\n"))

potfilesin.close()

os.chdir(podir)
print "Generating POT file"
subprocess.call(["intltool-update", "-pot", "--gettext-package=template"])
print "...done."
