from fastapi import FastAPI
from pydantic import BaseModel


# CREATION "RESTAURANT"
app = FastAPI()


@app.get("/")
def accueil():
    return {"message":"ça marche"}


# VERIFIER QUE CHAQUE VALEUR CORRESPOND A SON TYPE
class tableau (BaseModel) :
    nom : str
    prix : float 
    statut : str

# ON CREE LES TABLEAUX SOUS FORME D'OBJETS
@app.get("/tableau")
def afficher_tableau() :
    mer = tableau (nom="Mer", prix=30, statut="Dispo")
    Foret = tableau (nom="Foret", prix=45, statut="Vendu")
    # ON CREE UNE LISTE DES OBJETS QUI CREE AUTO UN JSON
    tableaux = [mer, Foret]
    
    return tableaux


# CHAQUE TABLEAU A SON ID
# POUR VISITER UN TABLEAU EN PARTICULIER, ON AJOUTE URL /{id}
@app.get("/tableau/{id}")
def afficher_un_tableau(id:int) :
    mer = tableau (nom="Mer", prix=30, statut="Dispo")
    Foret = tableau (nom="Foret", prix=45, statut="Vendu")
    tableaux = [mer, Foret]
    
    return tableaux[id]
    