import os
import glob
import polib
import ConfigParser

accoms = glob.glob("accomplishments/*/en/*")
files = glob.glob("generated/po/*.po")

accomset = accoms[0].split("/")[1]

for f in files:
    langcode = os.path.split(f)[1].split(".")[0]
    langdir = os.path.join(os.path.join("accomplishments/", accomset), langcode)
    print "Opening: " + langcode
    #print langcode
    po = polib.pofile('generated/po/en_GB.po')

    if not os.path.exists(langdir):
        os.makedirs(langdir)

    for a in accoms:
        accomname = os.path.split(a)[1].split(".")[0]
        print "...processing: " + accomname
        masterconfig = ConfigParser.ConfigParser()
        masterconfig.read(a)
        title = masterconfig.get("accomplishment", "title")
        outputconfig = ConfigParser.ConfigParser()
        outputconfig.add_section("accomplishment")

        try:
            description = po.find(accomname + "title").msgstr
            outputconfig.set("accomplishment", "title", title)
        except:
            pass
                   
        try:
            description = po.find(accomname + "_description").msgstr
            outputconfig.set("accomplishment", "description", description)
        except:
            pass
        
        outputconfig.set("accomplishment", "application", masterconfig.get("accomplishment", "application"))
        outputconfig.set("accomplishment", "category", masterconfig.get("accomplishment", "category"))
        outputconfig.set("accomplishment", "icon", masterconfig.get("accomplishment", "icon"))

        try:
            summary = po.find(accomname + "_summary").msgstr
            outputconfig.set("accomplishment", "summary", summary)
        except:
            pass
            
        try:
            tips = po.find(accomname + "_tips").msgstr
            outputconfig.set("accomplishment", "tips", tips)
        except:
            pass
        
        try:    
            pitfalls = po.find(accomname + "_pitfalls").msgstr
            outputconfig.set("accomplishment", "pitfalls", pitfalls)
        except:
            pass
        
        try:
            links = po.find(accomname + "_links").msgstr
            outputconfig.set("accomplishment", "links", links)
        except:
            pass
        
        try:
            help = po.find(accomname + "_help").msgstr
            outputconfig.set("accomplishment", "help", help)
        except:
            pass

        
        if masterconfig.has_option("accomplishment", "depends"):
            outputconfig.set("accomplishment", "depends", masterconfig.get("accomplishment", "depends"))
        
        outputconfig.set("accomplishment", "needs-signing", masterconfig.get("accomplishment", "needs-signing"))
        outputconfig.set("accomplishment", "needs-information", masterconfig.get("accomplishment", "needs-information"))
        #print accomname

        path = os.path.join(os.path.join(os.path.join("accomplishments", accomset), langcode), accomname + ".accomplishment")

        outfile = open(path, "w")
        outputconfig.write(outfile)
        #outfile.write(outputconfig)
        outfile.close()

