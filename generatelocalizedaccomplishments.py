import os
import glob
import polib
import ConfigParser


class GenerateTranslations():
    def __init__(self):
        self.accoms = glob.glob("accomplishments/*/en/*")
        self.files = glob.glob("generated/po/*.po")

        self.accomset = self.accoms[0].split("/")[1]

        for f in self.files:
            langcode = os.path.split(f)[1].split(".")[0]
            langdir = os.path.join(os.path.join("accomplishments/", self.accomset), langcode)
            popath = "generated/po/" + langcode + ".po"
            
            print "Opening: " + langcode + " at " + popath
            
            self.currentpo = polib.pofile(popath)

            if not os.path.exists(langdir):
                os.makedirs(langdir)

            for a in self.accoms:
                accomname = os.path.split(a)[1].split(".")[0]
                print "...processing: " + accomname
                self.masterconfig = ConfigParser.ConfigParser()
                self.masterconfig.read(a)
                #title = self.masterconfig.get("accomplishment", "title")
                self.outputconfig = ConfigParser.ConfigParser()
                self.outputconfig.add_section("accomplishment")

                title = self.process_field(accomname, "title")
                self.outputconfig.set("accomplishment", "title", title)
                
                description = self.process_field(accomname, "description")
                self.outputconfig.set("accomplishment", "description", description)
                
                if self.masterconfig.has_option("accomplishment", "application"):
                    self.outputconfig.set("accomplishment", "application", self.masterconfig.get("accomplishment", "application"))
                
                if self.masterconfig.has_option("accomplishment", "category"):
                    self.outputconfig.set("accomplishment", "category", self.masterconfig.get("accomplishment", "category"))                
                
                if self.masterconfig.has_option("accomplishment", "icon"):
                    self.outputconfig.set("accomplishment", "icon", self.masterconfig.get("accomplishment", "icon"))                
                
                if self.masterconfig.has_option("accomplishment", "depends"):
                    self.outputconfig.set("accomplishment", "depends", self.masterconfig.get("accomplishment", "depends"))                
                
                summary = self.process_field(accomname, "summary")
                self.outputconfig.set("accomplishment", "summary", summary)                

                steps = self.process_field(accomname, "steps")
                self.outputconfig.set("accomplishment", "steps", steps)

                tips = self.process_field(accomname, "tips")
                self.outputconfig.set("accomplishment", "tips", tips)
                
                pitfalls = self.process_field(accomname, "pitfalls")
                self.outputconfig.set("accomplishment", "pitfalls", pitfalls)
                
                help = self.process_field(accomname, "help")
                self.outputconfig.set("accomplishment", "help", help)

                path = os.path.join(os.path.join(os.path.join("accomplishments", self.accomset), langcode), accomname + ".accomplishment")

                outfile = open(path, "w")
                self.outputconfig.write(outfile)
                outfile.close()
        print "Done."

    def process_field(self, accomname, field):
        try:
            val = None
            final = None
            
            val = self.currentpo.find(accomname + "_" + field).msgstr.split("\r\n")
            
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
            return final
        except:
            print "......not found: " + field
            if self.masterconfig.has_option("accomplishment", field):
                print ".........using English translation."
                content = self.masterconfig.get("accomplishment", field)
                return content.rstrip()

if __name__=="__main__":
    trans = GenerateTranslations()
