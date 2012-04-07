import os
import glob
import polib
import ConfigParser


class GenerateTranslations():
    def __init__(self):
        accoms = glob.glob("accomplishments/*/en/*")
        files = glob.glob("generated/po/*.po")

        accomset = accoms[0].split("/")[1]

        for f in files:
            langcode = os.path.split(f)[1].split(".")[0]
            langdir = os.path.join(os.path.join("accomplishments/", accomset), langcode)
            popath = "generated/po/" + langcode + ".po"
            
            print "Opening: " + langcode + " at " + popath
            
            self.currentpo = polib.pofile(popath)

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

                title = self.process_field(accomname, "title")
                outputconfig.set("accomplishment", "title", title)
                
                description = self.process_field(accomname, "description")
                outputconfig.set("accomplishment", "description", description)
                
                if masterconfig.has_option("accomplishment", "application"):
                    outputconfig.set("accomplishment", "application", masterconfig.get("accomplishment", "application"))
                
                if masterconfig.has_option("accomplishment", "category"):
                    outputconfig.set("accomplishment", "category", masterconfig.get("accomplishment", "category"))                
                
                if masterconfig.has_option("accomplishment", "icon"):
                    outputconfig.set("accomplishment", "icon", masterconfig.get("accomplishment", "icon"))                
                
                if masterconfig.has_option("accomplishment", "depends"):
                    outputconfig.set("accomplishment", "depends", masterconfig.get("accomplishment", "depends"))                
                
                summary = self.process_field(accomname, "summary")
                outputconfig.set("accomplishment", "summary", summary)                

                steps = self.process_field(accomname, "steps")
                outputconfig.set("accomplishment", "steps", steps)

                tips = self.process_field(accomname, "tips")
                outputconfig.set("accomplishment", "tips", tips)

                pitfalls = self.process_field(accomname, "pitfalls")
                outputconfig.set("accomplishment", "pitfalls", pitfalls)
                
                help = self.process_field(accomname, "help")
                outputconfig.set("accomplishment", "help", help)

                path = os.path.join(os.path.join(os.path.join("accomplishments", accomset), langcode), accomname + ".accomplishment")

                outfile = open(path, "w")
                outputconfig.write(outfile)
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
            return final
        except:
            print "......not found: " + field
            pass

if __name__=="__main__":
    trans = GenerateTranslations()
