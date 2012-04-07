import glob
import os
from random import randint
import ConfigParser
import subprocess

files = glob.glob("accomplishments/*/en/*")

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
        NOTE: Put each URL on a new line\n" },
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

print "Processing files:"

for f in files:
    print "..." + str(f)
    accomplishmentname = os.path.split(f)[1].split(".")[0]
    tempfile = open(os.path.join(generatedaccomplishmentsdir, accomplishmentname + ".c"), "w")
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

                output = output + ("// ENGLISH TRANSLATION:\n")
                output = output + (origitem + "\n")
                output = output + "// .\n"
                output = output + "// ----- TRANSLATION INSTRUCTIONS ----- \n"
                for c in sec.values()[0].split("\n"):
                    output = output + ("// " + c + "\n")
                output = output + ("_(\"" + accomplishmentname + "_" + i[0] + "\")\n")
                tempfile.write(output)
    tempfile.close()

    # write POTFILES.in
    potfilesin.write(os.path.join("accomplishments", accomplishmentname + ".c\n"))

potfilesin.close()

os.chdir(podir)
print "Generating POT file"
subprocess.call(["intltool-update", "-pot", "--gettext-package=template"])
print "...done."
