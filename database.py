from sqlmodel import SQLModel, Field
from sqlmodel import create_engine
from sqlmodel import Session
from sqlmodel import select

sqlite_url = "sqlite:///tableaux.db"
engine = create_engine(sqlite_url)

def creer_tables(): 
    SQLModel.metadata.create_all(engine)



class Tableau (SQLModel, table = True) :
    id: int = Field(default=None, primary_key=True)
    nom: str
    prix: float
    statut: str


creer_tables()

def ajouter_tableau(nom, prix, statut):
    with Session(engine) as session:
        nouveau = Tableau(nom=nom, prix=prix, statut=statut)
        session.add(nouveau)
        session.commit()



def obtenir_tableaux():
    with Session(engine) as session:
        resultats = session.exec(select(Tableau)).all()
        return resultats

def obtenir_un_tableau(id):
    with Session(engine) as session:
        resultat = session.exec(select(Tableau).where(Tableau.id == id)).first()
        return resultat



# ON AJOUTE F POUR MODIFIER LE TABLEAU 
def modifier_tableau(id, nom, prix, statut):
    with Session(engine) as session:
        tableau = session.get(Tableau, id)
        # SECURITE
        if tableau is None:
            return None
        tableau.nom = nom
        tableau.prix = prix
        tableau.statut = statut

        # PREPARATION
        session.add(tableau)

        # ENVOIE
        session.commit()

        # ACTUALISATION
        session.refresh(tableau)
        return tableau


def supprimer_tableau(id):
    with Session(engine) as session:
        tableau = session.get(Tableau, id)
        if tableau is None:
            return False
        session.delete(tableau)
        session.commit()
        return True