from sqlmodel import SQLModel, Field
from sqlmodel import create_engine
from sqlmodel import Session
from sqlmodel import select
from passlib.context import CryptContext

sqlite_url = "sqlite:///tableaux.db"
engine = create_engine(sqlite_url)

def creer_tables(): 
    SQLModel.metadata.create_all(engine)




class Utilisateur(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    mdp_hash: str


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




# ==================== PARTIE ADMINISTRATEUR =============================



def force_mdp(mdp):
    mdp_force = False
    mdp_test = mdp

    # ON VERIFIE SI LE MDP A DES MAJ
    a_maj = False
    for lettres in mdp_test :
        if lettres.isupper():
            a_maj = True

    # ON VERIFIE SI LE MDP A AU MOINS 8 CARACTERES 
    longueur = False
    if len(mdp_test) >= 8 :
        longueur=True

    caracteres_spe = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", ":", ";", "'", '"', "<", ">", ",", ".", "?", "/", "|", "~", "`"]

    # on vérifie que le mdp contienne un caractere spécial
    a_spe = False
    for lettres in mdp_test:
        if lettres in caracteres_spe:
            a_spe = True

    if a_maj == True and longueur == True and a_spe == True :
        mdp_force=True

    return mdp_force
    



# CONFIGURE OUTIL UNE FOIS AVEC ALGO CHOISI (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# PREND MDP EN CLAIR + RENVOI SON HASHE (UTILISER UNE FOIS CREATION COMPTE)
def hasher_mdp(mdp):
    return pwd_context.hash(mdp)

#   PREND MDP TAPE ET HASHE STOCKE, RENVOI TRUE/FALSE
# MDP EN QUESTION EST CELUI QUE UTILISATEUR VIENT DE TAPER PAS LANCIEN
def verifier_mdp(mdp, hash_stocke):
    return pwd_context.verify(mdp, hash_stocke)



# F POUR CREER COMPTES ADMIN
# MDP EST SOTCKE BRIEVEMENT EN CLAIR (TEL QUEL, VIENT DETRE TAPE PAR UTILISATEUR)
def creer_utilisateur(email, mdp):
    # OUVRE SESSION TEMP
    with Session(engine) as session :

        if force_mdp(mdp):

        # TRANSFORME MDP EN HASHE, PLUS BESOIN DE MDP
            hash_mdp = hasher_mdp(mdp)

        # ON CREE OBJECT AVEC CLASSE UTILISATEUR, PAS DE MDP EN CLAIR !!!!
            nouvel_utilisateur = Utilisateur(email=email, mdp_hash=hash_mdp)

        # PREPARE
            session.add(nouvel_utilisateur)

        # ON VALIDE 
            session.commit()

        else:
            return "Le mot de passe doit posséder au moins 8 caractères, un caractère spécial et une majuscule"
# creer_tables()


def recuperer_utilisateur(email):
    with Session(engine) as session: 
        user = session.exec(select(Utilisateur).where(Utilisateur.email == email)).first()
        return user