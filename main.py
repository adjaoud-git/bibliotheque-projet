import json
import os

# === Chargement et sauvegarde des données ===
def charger_bibliotheque(fichier):
    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"livres": [], "prochain_id": 1}

def sauvegarder_bibliotheque(bibliotheque, fichier):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(bibliotheque, f, indent=4, ensure_ascii=False)

# === Affichage ===
def afficher_menu():
    print("Menu - Gestion de Bibliothèque")
    print("1.Afficher tous les livres")
    print("2. Ajouter un livre")
    print("3. Supprimer un livre")
    print("4. Rechercher un livre")
    print("5. Marquer un livre comme lu")
    print("6. Afficher uniquement les livres lus")
    print("7. Afficher uniquement les livres non lus")
    print("8. Trier les livres")
    print("9. Quitter")

def afficher_livre(livre):
    lu = "Oui" if livre["Lu"] else "Non"
    note = livre["Note"] if livre["Note"] is not None else "-"
    print(f"{livre['ID']}. {livre['Titre']} par {livre['Auteur']} ({livre['Année']}) | Lu: {lu} | Note: {note}")

# === Fonctions de gestion des livres ===
def generer_nouvel_id(bibliotheque):
    id_actuel = bibliotheque["prochain_id"]
    bibliotheque["prochain_id"] += 1
    return id_actuel

def ajouter_livre(bibliotheque):
    titre = input("Titre du livre : ")
    auteur = input("Auteur du livre : ")
    annee = input("Année de publication : ")
    try:
        annee = int(annee)
    except ValueError:
        print("Année invalide.")
        return

    nouveau_livre = {
        "ID": generer_nouvel_id(bibliotheque),
        "Titre": titre,
        "Auteur": auteur,
        "Année": annee,
        "Lu": False,
        "Note": None
    }

    bibliotheque["livres"].append(nouveau_livre)
    print("Livre ajouté avec succès.")

def supprimer_livre(bibliotheque):
    try:
        id_livre = int(input("Entrez l'ID du livre à supprimer : "))
    except ValueError:
        print("ID invalide.")
        return

    for livre in bibliotheque["livres"]:
        if livre["ID"] == id_livre:
            confirmation = input(f"Êtes-vous sûr de vouloir supprimer '{livre['Titre']}' ? (o/n) ").lower()
            if confirmation == 'o':
                bibliotheque["livres"].remove(livre)
                print("Livre supprimé.")
            return
    print("Aucun livre trouvé avec cet ID.")

def rechercher_livre(bibliotheque):
    mot_cle = input("Entrez un mot-clé (titre ou auteur) : ").lower()
    resultats = [livre for livre in bibliotheque["livres"]
                 if mot_cle in livre["Titre"].lower() or mot_cle in livre["Auteur"].lower()]
    if resultats:
        print("\n🔍 Résultats de recherche :")
        for livre in resultats:
            afficher_livre(livre)
    else:
        print("🚫 Aucun résultat trouvé.")

def marquer_comme_lu(bibliotheque):
    try:
        id_livre = int(input("Entrez l'ID du livre que vous avez lu : "))
    except ValueError:
        print("⚠️ ID invalide.")
        return

    for livre in bibliotheque["livres"]:
        if livre["ID"] == id_livre:
            if livre["Lu"]:
                print("ℹ️ Ce livre est déjà marqué comme lu.")
                return
            livre["Lu"] = True
            try:
                note = float(input("Donnez une note sur 10 : "))
                if 0 <= note <= 10:
                    livre["Note"] = note
                else:
                    print("⚠️ Note doit être entre 0 et 10.")
            except ValueError:
                print("⚠️ Entrée invalide pour la note.")
            print("✅ Livre marqué comme lu.")
            return
    print("❌ Aucun livre trouvé avec cet ID.")

def afficher_par_etat(bibliotheque, lu=True):
    filtre = [livre for livre in bibliotheque["livres"] if livre["Lu"] == lu]
    if filtre:
        print("\n📖 Livres " + ("lus" if lu else "non lus") + " :")
        for livre in filtre:
            afficher_livre(livre)
    else:
        print(f"🚫 Aucun livre {'lu' if lu else 'non lu'} trouvé.")

def trier_livres(bibliotheque):
    critere = input("Trier par (auteur, annee, note) : ").lower()
    if critere == "auteur":
        tri = sorted(bibliotheque["livres"], key=lambda x: x["Auteur"])
    elif critere == "annee":
        tri = sorted(bibliotheque["livres"], key=lambda x: x["Année"])
    elif critere == "note":
        tri = sorted(bibliotheque["livres"], key=lambda x: (x["Note"] if x["Note"] is not None else -1), reverse=True)
    else:
        print("⚠️ Critère de tri invalide.")
        return

    print(f"\n📊 Livres triés par {critere} :")
    for livre in tri:
        afficher_livre(livre)

# === Boucle principale ===
def main():
    fichier = "bibliotheque.json"
    bibliotheque = charger_bibliotheque(fichier)

    while True:
        afficher_menu()
        choix = input("Entrez votre choix (1-9) : ")

        if choix == "9":
            print("Sauvegarde et fermeture du programme...")
            sauvegarder_bibliotheque(bibliotheque, fichier)
            break
        elif choix == "1":
            print("\n📚 Liste des livres :")
            for livre in bibliotheque["livres"]:
                afficher_livre(livre)
        elif choix == "2":
            ajouter_livre(bibliotheque)
        elif choix == "3":
            supprimer_livre(bibliotheque)
        elif choix == "4":
            rechercher_livre(bibliotheque)
        elif choix == "5":
            marquer_comme_lu(bibliotheque)
        elif choix == "6":
            afficher_par_etat(bibliotheque, lu=True)
        elif choix == "7":
            afficher_par_etat(bibliotheque, lu=False)
        elif choix == "8":
            trier_livres(bibliotheque)
        else:
            print(" Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()