from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()


@app.get("/")
def accueil():
    return {"message":"ça marche"}



class tableau (BaseModel) :
    nom : str
    prix : float 
    statut : str

@app.get("/tableau")
def afficher_tableau() :
    mer = tableau (nom="Mer", prix=30, statut="Dispo")
    Foret = tableau (nom="Foret", prix=45, statut="Vendu")
    tableaux = [mer, Foret]
    print(tableaux)
    return tableaux

@app.get("/tableau/{id}")
def afficher_un_tableau(id:int) :
    mer = tableau (nom="Mer", prix=30, statut="Dispo")
    Foret = tableau (nom="Foret", prix=45, statut="Vendu")
    tableaux = [mer, Foret]
    
    return tableau[id]
    