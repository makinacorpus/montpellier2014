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

    fname = "VilleMTP_MTP_Municipale2014_full.csv"
    outfilename = "bureaux_decoupage.json"
    #outfilename = "resultatsG1.json"
    offices = { '275': {}, '276': {} }
    candidats = {"nuls": "Nuls"}
    partis = {"nuls": "Nuls"}
    G = {'275': {"nuls": 0}, '276': {"nuls": 0}}
    total = {'275': {}, '276': {}}
    with open(fname, 'r') as csv_file:

        reader = csv.DictReader(csv_file)
        current_bureau = ""
        current_election = ""

        for row in reader:
            print row.keys()
            all = row["Candidat"]

            nom_candidat = unicode(str(all.split("(")[-1]).split(")")[0].decode("utf8"))
            nom_parti = all.split("(")[0]
            normalized_nom = unicodedata.normalize('NFKD', nom_candidat).encode('ascii', 'ignore').lower().replace(" ", "_")
            num_bureau = row["N\xc2\xb0 Bureau"]
            num_election = row["N\xc2\xb0 Election"]
            nbr_voix = float(row["Nombre de Voix"])
            #print nbr_voix
            votants = float(row["Votants"])
            #print votants
            pourcentage = nbr_voix * 100 / votants
            #print pourcentage

            offices[num_election].setdefault(num_bureau, [])
            offices[num_election][num_bureau].append({normalized_nom: pourcentage})
            
            G[num_election].setdefault(normalized_nom, 0)
            G[num_election][normalized_nom] += nbr_voix
            
            total[num_election].setdefault(num_bureau, votants)
            
            candidats.setdefault(normalized_nom, nom_candidat)
            partis.setdefault(normalized_nom, nom_parti)

            if (current_bureau != num_bureau) or (current_election != num_election):
                offices[num_election][num_bureau].append({"nuls": float(row["Nuls"]) * 100 / votants})
                G[num_election]["nuls"] += float(row["Nuls"])
                current_bureau = num_bureau
                current_election = num_election
        pass
    
    for office in offices["275"].keys():
        offices["275"][office] = sorted(offices["275"][office], key=lambda k: k.values()[0], reverse=True)
    for office in offices["276"].keys():
        offices["276"][office] = sorted(offices["276"][office], key=lambda k: k.values()[0], reverse=True)

    with open("bureaux_decoupage_1.json", 'w') as outfile:
        response_json = json.dump(offices["275"], outfile)

    with open("bureaux_decoupage_2.json", 'w') as outfile:
        response_json = json.dump(offices["276"], outfile)

    with open("candidats.json", 'w') as outfile:
        response_json = json.dump(candidats, outfile)

    with open("partis.json", 'w') as outfile:
        response_json = json.dump(partis, outfile)

    total1 = sum(total["275"].values())
    G1 = sorted([{nom: float(value) * 100 / float(total1)} for nom, value in G["275"].items()], key=lambda k: k.values()[0], reverse=True)
    total2 = sum(total["275"].values())
    G2 = sorted([{nom: float(value) * 100 / float(total2)} for nom, value in G["276"].items()], key=lambda k: k.values()[0], reverse=True)

    with open("resultatsG1.json", 'w') as outfile:
        response_json = json.dump(G1, outfile)

    with open("resultatsG2.json", 'w') as outfile:
        response_json = json.dump(G2, outfile)
