from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os 
import shutil
from fastapi import UploadFile
from database import Tableau, obtenir_tableaux, obtenir_un_tableau, ajouter_tableau, modifier_tableau, supprimer_tableau


# CREATION "RESTAURANT"
app = FastAPI()


# CORS  = PROTECTION NAVIGATEUR QUI EMPECHE REQUETE DE COMMUNIQUER ENTRE 2 ORIGINES DIFFERENTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ajouter_tableau("Mer", 30, "Dispo")
ajouter_tableau("Foret", 45, "Vendu")




@app.get("/tableau")
def afficher_tableau() :
    return obtenir_tableaux


# CHAQUE TABLEAU A SON ID
# POUR VISITER UN TABLEAU EN PARTICULIER, ON AJOUTE URL /{id}
@app.get("/tableau/{id}")
def afficher_un_tableau(id:int) :
    resultat = obtenir_un_tableau(id)
    if resultat == None :
        raise HTTPException(status_code=404, detail="Tableau introuvable")
    return obtenir_un_tableau(id)



# ROUTE PUT
@app.put("/tableau/{id}")
def maj_tableau(id: int, donnees: Tableau):
    resultat = modifier_tableau(id, donnees.nom, donnees.prix, donnees.statut)
    if resultat is None:
        raise HTTPException(status_code=404, detail="Tableau introuvable")
    return resultat




@app.delete("/tableau/{id}")
def suppr_tableau(id:int):
    supprimer = supprimer_tableau(id)
    if not supprimer:
        raise HTTPException(status_code=404, detail="Tableau introuvable")
    return {"message":"Tableau supprimé"}



@app.post("/tableau/{id}/image")

# fichier: UploadFile = communique avec fastapi pour dire que la route attend un fichier et non du texte(json)
def uploader_image(id:int, fichier: UploadFile):
    dossier = "uploads"

    # creer le dossier upload si il n'existe pas deja  (exist_ok=True vérifie)
    os.makedirs(dossier, exist_ok=True)

    # construit le chemin ou le fichier sera save en gardant son nom
    chemin = f"{dossier}/{fichier.filename}"

    # ouvre nv fichier en écriture en binaire ("wb" = write binary — nécessaire car une image n'est pas du texte)
    with open(chemin, "wb") as buffer:
        
        # copie contenu fichier vers nv fichier du disque
        shutil.copyfileobj(fichier.file, buffer)
        return {"chemin": chemin}