
import os
import requests

from dotenv import load_dotenv
from pymongo import MongoClient, ReplaceOne
from urllib.parse import quote_plus

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
username = quote_plus(os.getenv("MONGODB_USER"))
password = quote_plus(os.getenv("MONGODB_PASSWORD"))
host = os.getenv("MONGODB_HOST")
database_name = os.getenv("MONGODB_DATABASE")

uri = (
    f"mongodb+srv://{username}:{password}@{host}/"
    "?retryWrites=true&w=majority"
)

client = MongoClient(uri, serverSelectionTimeoutMS=10000)
db = client[database_name]

# Collections MongoDB
collection_users = db["Utilisateurs"]
collection_products = db["Produits"]
collection_carts = db["Paniers"]


# Récupération des données API
def get_api_data(url):
    response = requests.get(
        url,
        params={"limit": 0},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


# Importation des utilisateurs
def import_users():
    data = get_api_data("https://dummyjson.com/users")

    users = []

    for user in data["users"]:
        users.append({
            "_id": user["id"],
            "identite": (
                user.get("firstName", "")
                + " "
                + user.get("lastName", "")
            ),
            "coordonnees": {
                "email": user.get("email"),
                "telephone": user.get("phone"),
                "adresse": user.get("address")
            }
        })

    if users:
        collection_users.bulk_write([
            ReplaceOne({"_id": u["_id"]}, u, upsert=True)
            for u in users
        ])

    print(f"{len(users)} utilisateurs importés")


# Importation des produits
def import_products():
    data = get_api_data("https://dummyjson.com/products")

    products = []

    for product in data["products"]:
        products.append({
            "_id": product["id"],
            "titre": product.get("title"),
            "prix": product.get("price"),
            "description": product.get("description"),
            "categorie": product.get("category"),
            "marque": product.get("brand"),
            "caracteristiques": {
                "dimensions": product.get("dimensions"),
                "poids": product.get("weight"),
                "stock": product.get("stock"),
                "note": product.get("rating")
            }
        })

    if products:
        collection_products.bulk_write([
            ReplaceOne({"_id": p["_id"]}, p, upsert=True)
            for p in products
        ])

    print(f"{len(products)} produits importés")


# Importation des paniers
def import_carts():
    data = get_api_data("https://dummyjson.com/carts")

    carts = []

    for cart in data["carts"]:
        for product in cart["products"]:

            carts.append({
                "_id": f'{cart["id"]}_{product["id"]}',
                "id_panier": cart["id"],
                "utilisateur_id": cart["userId"],
                "produit_id": product["id"],
                "quantite": product["quantity"]
            })

    if carts:
        collection_carts.bulk_write([
            ReplaceOne({"_id": c["_id"]}, c, upsert=True)
            for c in carts
        ])

    print(f"{len(carts)} lignes de paniers importées")


# Programme principal
def main():

    try:
        # Tester la connexion
        client.admin.command("ping")
        print("Connexion MongoDB réussie !")

        # Importation des données
        import_users()
        import_products()
        import_carts()

        print("\nImportation terminée avec succès !")

    except Exception as error:
        print("Erreur :", error)

    finally:
        client.close()


if __name__ == "__main__":
    main()
