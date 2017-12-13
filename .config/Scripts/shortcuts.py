from pathlib import Path
import csv
from re import sub
from re import compile

quteshortcuts = ""
rangershortcuts = ""
bashshortcuts = ""
#fishshortcuts = ""
home = str(Path.home())+"/"
rangerlocation=home+".config/ranger/rc.conf"
bashlocation=home+".bashrc"
qutelocation=home+".config/qutebrowser/config.py"


# These are the labels that demarcate where the shortcuts
# go in the config files.
beg="# DO NOT DELETE LMAO\n"
end="# DO NOT DELETE LMAO"

#First we open the list of folder shortcuts and go down each line adding each in the required syntax to each of the three configs:

with open(home+".config/Scripts/folders") as fold:
    for line in csv.reader(fold, dialect="excel-tab"):
        #Adds the ranger go, tab, move and yank commands:
        rangershortcuts+=("map g"+line[0]+" cd "+line[1]+"\n")
        rangershortcuts+=("map t"+line[0]+" tab_new "+line[1]+"\n")
        rangershortcuts+=("map m"+line[0]+" shell mv %s "+line[1]+"\n")
        rangershortcuts+=("map Y"+line[0]+" shell cp -r %s "+line[1]+"\n")
        #Adds the bashshortcuts shortcuts:
        bashshortcuts+=("alias "+line[0]+"=\"cd "+line[1]+" && ls -a\"\n")
        #qutebrowser shortcuts:
        quteshortcuts+="config.bind(';"+line[0]+"', 'set downloads.location.directory "+line[1]+" ;; hint links download')\n"

#Goes thru the config file file and adds the shortcuts to both bashshortcuts and ranger.

with open(home+".config/Scripts/configs") as conf:
    for line in csv.reader(conf, dialect="excel-tab"):
        bashshortcuts+=("alias "+line[0]+"=\"vim "+line[1]+"\"\n")
        #fishshortcuts+=("alias "+line[0]+"=\"vim "+line[1]+"\"\n")
        #fishshortcuts+=("abbr --add "+line[0]+" \"vim "+line[1]+"\"\n")
        rangershortcuts+=("map "+line[0]+" shell vim "+line[1]+"\n")


def replaceInMarkers(text, shortcuts):
    markers = compile(beg+"(.|\s)*"+end)
    replacement =beg+shortcuts+end
    return sub(markers, replacement, text)



def writeShortcuts(location, shortcuts):
    with open(location, "r+") as input:
        final = ""
        final += input.read()
        final = replaceInMarkers(final, shortcuts)
        input.seek(0)
        input.write(final)
        input.truncate()

writeShortcuts(rangerlocation, rangershortcuts)
writeShortcuts(bashlocation, bashshortcuts)
writeShortcuts(qutelocation, quteshortcuts)
