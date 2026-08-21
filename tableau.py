import asyncio
from sqlmodel import SQLModel, Field
from sqlmodel import create_engine
from sqlmodel import Session
from sqlmodel import select

sqlite_url = "sqlite:///tableaux.db"
engine = create_engine(sqlite_url)

def creer_tables(): 
    SQLModel.metadata.create_all(engine)

creer_tables()

class Tableau (SQLModel, table = True) :
    id: int = Field(default=None, primary_key=True)
    nom: str
    prix: float
    statut: str


def ajouter_tableau(nom, prix, statut):
    with Session(engine) as session:
        nouveau = Tableau(nom=nom, prix=prix, statut=statut)
        session.add(nouveau)
        session.commit()



def obtenir_tableaux():
    with Session(engine) as session:
        resultats = session.exec(select(Tableau)).all
        return resultats












    def nommer_tableau(self):
        while True:
            nom_tableau = input("Indiquer le nom du tableau : ")
            if len(nom_tableau) == 0 :
                print("Veuillez entrer un nom pour le tableau !")
                continue
            self.nom = nom_tableau
            print(f"Le nom du tableau est désormais {nom_tableau}")
            break

    def chiffrer_tableau(self):
        while True :
            prix_tableau = float(input("Indiquer le prix du tableau en euros: "))
            if prix_tableau <= 0 :
                print("Veuillez entrer un prix supérieur à 0 euros !")
                continue
            self.prix = prix_tableau
            print(f"Le prix du tableau est {prix_tableau} euros.")
            break

    def statuer_tableau(self):
        while True :
            statut_tableau = input("Définir le statut du tableau : \nDisponible à la vente (1)\nVendu (2)")
            if statut_tableau == "1" or statut_tableau == "2" :
                print("Statut valide")                
            else :
                print("Veuillez choisir un statut valide pour continuer ! ")
                continue
            if statut_tableau == "1" : 
                self.statut = "Disponible"
            else : 
                self.statut = "Vendu"
            print(f"Le statut du tableau est désormais définit sur {self.statut}")
            break


mon_tableau = tableau("temp", 0, "temp")
mon_tableau.nommer_tableau()
mon_tableau.chiffrer_tableau()
mon_tableau.statuer_tableau()
    

print(mon_tableau.nom, mon_tableau.prix, mon_tableau.statut)



