#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import csv
import unicodedata
import json

candidates = {
    "gerard_de_mellon": 'Gerard DE MELLON',
    "nathalie_appere": 'Nathalie APPÉRÉ',
    "matthieu_theurier": 'Matthieu THEURIER',
    "valerie_hamon": 'Valérie HAMON',
    "caroline_ollivro": 'Caroline OLLIVRO',
    "pierre_priet": 'Pierre PRIET',
    "alexandre_noury": 'Alexandre NOURY',
}

if __name__ == '__main__':

    fname = "VilleMTP_MTP_Municipale2014_1.csv"
    outfilename = "bureaux_decoupage.json"
    #outfilename = "resultatsG1.json"
    offices = {}
    candidats = {}
    partis = {}
    with open(fname, 'r') as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:
            print row.keys()
            all = row["Candidat"]
            nom_candidat = unicode(str(all.split("(")[-1]).split(")")[0].decode("utf8"))
            nom_parti = all.split("(")[0]
            normalized_nom = unicodedata.normalize('NFKD', nom_candidat).encode('ascii', 'ignore').lower().replace(" ", "_")
            nbr_voix = float(row["Nombre de Voix"])
            print nbr_voix
            votants = float(row["Votants"])
            print votants
            pourcentage = nbr_voix * 100 / votants
            print pourcentage
            num_bureau = row["N\xc2\xb0 Bureau"]
            offices.setdefault(num_bureau, [])
            offices[num_bureau].append({normalized_nom: pourcentage})
            candidats.setdefault(normalized_nom, nom_candidat)
            partis.setdefault(normalized_nom, nom_parti)
            pass
            #newrow = []
            #if(row["NIVEAU_DETAIL"] == "bu"):
            #if(row["NIVEAU_DETAIL"] == "vi"):
                # Get results for each political list
                #for i in range(1, 10):
                    #print("%s -> %s" % ("CANDIDAT_%s" % (i), row["CANDIDAT_%s" % (i)]))
                    #nom_candidat = unicode(row["CANDIDAT_%s" % (i)].decode("utf8"))
                    #normalize name
                    #normalized_nom = unicodedata.normalize('NFKD', nom_candidat).encode('ascii', 'ignore').lower().replace(" ", "_")
                    #newrow.append({normalized_nom: float(row["POURCENTAGE_%s" % i].replace(",", "."))})

                #results = sorted(newrow, key=lambda k: k.values()[0], reverse=True)
                #offices[row["NUMERO_LIEU"]] = results
                #offices = results
                #break
    for office in offices.keys():
        offices[office] = sorted(offices[office], key=lambda k: k.values()[0], reverse=True)

    with open("bureaux_decoupage.json", 'w') as outfile:
        response_json = json.dump(offices, outfile)

    with open("candidats.json", 'w') as outfile:
        response_json = json.dump(candidats, outfile)

    with open("partis.json", 'w') as outfile:
        response_json = json.dump(partis, outfile)
