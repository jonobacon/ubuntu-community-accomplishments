import os
import glob
import polib
import ConfigParser


class GenerateTranslations():
    def __init__(self):
    
        print "Scanning for accomplishments:"
        accoms = {}
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
                        accoms[accID] = {'origfile' : accompath, 'inlangfile' : os.path.join(item,accom), 'coll' : collection}
                else:
                    accID = collection + "/" + item[:-15]
                    print " " + accID
                    accoms[accID] = {'origfile' : itempath,'inlangfile' : item, 'coll' : collection}
    
        self.pofiles = glob.glob("generated/po/*.po")

        for f in self.pofiles:
            langcode = os.path.split(f)[1].split(".")[0]
            popath = "generated/po/" + langcode + ".po"
            
            print "Opening: " + langcode + " at " + popath
            
            self.currentpo = polib.pofile(popath)
                
            for accomID in accoms:
                collection = accoms[accomID]['coll']
                origfile = accoms[accomID]['origfile']
                inlangfile = accoms[accomID]['inlangfile']
                langdir = os.path.join(os.path.join("accomplishments/", collection), langcode)
                if not os.path.exists(langdir):
                    os.makedirs(langdir)
                    
                print "...processing: " + accomID
                self.masterconfig = ConfigParser.ConfigParser()
                self.masterconfig.read(origfile)
                #title = self.masterconfig.get("accomplishment", "title")
                self.outputconfig = ConfigParser.ConfigParser()
                self.outputconfig.add_section("accomplishment")

                title = self.process_field(accomID, "title")
                self.outputconfig.set("accomplishment", "title", title)
                
                description = self.process_field(accomID, "description")
                self.outputconfig.set("accomplishment", "description", description)
                
                if self.masterconfig.has_option("accomplishment", "collection"):
                    print self.masterconfig.get("accomplishment", "collection")                    
                    self.outputconfig.set("accomplishment", "collection", self.masterconfig.get("accomplishment", "collection"))
                
                if self.masterconfig.has_option("accomplishment", "category"):
                    self.outputconfig.set("accomplishment", "category", self.masterconfig.get("accomplishment", "category"))                

                if self.masterconfig.has_option("accomplishment", "needs-signing"):
                    self.outputconfig.set("accomplishment", "needs-signing", self.masterconfig.get("accomplishment", "needs-signing"))                
                
                if self.masterconfig.has_option("accomplishment", "needs-information"):
                    self.outputconfig.set("accomplishment", "needs-information", self.masterconfig.get("accomplishment", "needs-information")) 
                    
                if self.masterconfig.has_option("accomplishment", "icon"):
                    self.outputconfig.set("accomplishment", "icon", self.masterconfig.get("accomplishment", "icon"))                
                
                if self.masterconfig.has_option("accomplishment", "depends"):
                    self.outputconfig.set("accomplishment", "depends", self.masterconfig.get("accomplishment", "depends"))                

                if self.masterconfig.has_option("accomplishment", "author"):
                    self.outputconfig.set("accomplishment", "author", self.masterconfig.get("accomplishment", "author"))                

                # things that can be translated
                
                summary = self.process_field(accomID, "summary")
                self.outputconfig.set("accomplishment", "summary", summary)                

                steps = self.process_field(accomID, "steps")
                self.outputconfig.set("accomplishment", "steps", steps)

                tips = self.process_field(accomID, "tips")
                self.outputconfig.set("accomplishment", "tips", tips)
                
                pitfalls = self.process_field(accomID, "pitfalls")
                self.outputconfig.set("accomplishment", "pitfalls", pitfalls)
                
                help = self.process_field(accomID, "help")
                self.outputconfig.set("accomplishment", "help", help)

                inlangfile_splitted = inlangfile.split("/")
                if len(inlangfile_splitted) == 2:
                    if not os.path.exists(os.path.join(langdir, inlangfile_splitted[0])):
                        os.makedirs(os.path.join(langdir, inlangfile_splitted[0]))
                path = os.path.join(langdir, inlangfile)

                outfile = open(path, "w")
                self.outputconfig.write(outfile)
                outfile.close()
                
        print "Done."

    def process_field(self, accomID, field):
        print field
        try:
            val = None
            final = None
            val = self.currentpo.find(accomID + "_" + field).msgstr.split("\r\n")
            
            while True:
                try:
                    val.remove("")
                except ValueError:
                    break
            final = ""
            
            for l in val:
                final = final + (l + "\n")
            
            # remove the final \n
            final = final.rstrip()
            
            if final == "":
                final = self.masterconfig.get("accomplishment", field)
            return final.encode("utf-8")
        except:
            if self.masterconfig.has_option("accomplishment", field):
                print "......" + field + " not found,using original translation."
                content = self.masterconfig.get("accomplishment", field)
                return content.rstrip().encode("utf-8")

if __name__=="__main__":
    trans = GenerateTranslations()
