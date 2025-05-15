# src/main.py
from init_db import create_tables
from import_data import import_stores_data, import_products_data, import_sales_data
from analytics import display_analytics

def main():
    # Initialiser la base de données
    print("🔄 Initialisation de la base de données...")
    create_tables()
    
    # Importer les données
    print("\n🔄 Importation des données...")
    import_stores_data()
    import_products_data()
    import_sales_data()
    
    # Afficher les résultats d'analyse
    print("\n📊 Affichage des résultats d'analyse...")
    display_analytics()

if __name__ == "__main__":
    main()