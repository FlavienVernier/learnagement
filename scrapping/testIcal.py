import icalendar
from urllib.request import urlretrieve
import csv 
import json

#url = "https://ade-usmb-ro.grenet.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=b5cfb898a9c27be94975c12c6eb30e9233bdfae22c1b52e2cd88eb944acf5364c69e3e5921f4a6ebe36e93ea9658a08f,1&resources=9497,7954,4941,4886&projectId=1&calType=ical&lastDate=2042-08-14"
#url = "https://ade-usmb-ro.grenet.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=b5cfb898a9c27be94975c12c6eb30e9233bdfae22c1b52e2cd88eb944acf5364c69e3e5921f4a6ebe36e93ea9658a08f,1&resources=1697&projectId=1&calType=ical&lastDate=2042-08-14"
fichier = "ADECal.ics"
#urlretrieve(url, fichier)

with open(fichier) as f:
    calendar = icalendar.Calendar.from_ical(f.read())
#print(calendar)

with open("enseignant.json") as f:
    enseignants = json.load(f)
noms_enseignants = {e["nom"].upper() for e in enseignants}

evenement=[]
for event in calendar.walk('VEVENT'):
    description = str(event.get('DESCRIPTION')).split("\n")
    intervenants = []
    for field in description:
        texte = field.strip().upper()
        if any(nom in texte for nom in noms_enseignants):
            intervenants.append(field)
    #print(intervenants)
    if(len(intervenants) == 0):
        print(description)
    date  = str(event.get('DTSTART').dt).split(" ")[0]
    debut = (str(event.get('DTSTART').dt).split(" ")[1]).split("+")[0]
    fin   = str(event.get('DTEND').dt).split(" ")[1].split("+")[0]
    evenement.append([str(event.get('SUMMARY')), str(event.get('LOCATION')), date , debut, fin, ", ".join(intervenants)])
#print(evenement)

#sauvergarde CSV
with open("evenement.csv","wt+",newline="") as f:
    writer=csv.writer(f)
    for row in evenement:
        writer.writerow(row)
 

data={}
n=0
#sauvegarde json
for elt in evenement:
    data[f'evenement-{n}']={
        'nom':elt[0],
        'salle':elt[1],
        'debut':elt[2][10:-17],
        'fin':elt[3][10:-17],
    }
    n+=1

with open("evenement_cal.json","w") as f:
    json.dump(data,f,indent=4)