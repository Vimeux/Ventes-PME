# src/import_data.py
import sqlite3
import os
import pandas as pd
import requests
from io import StringIO

DB_PATH = os.getenv("DATABASE_URL", "sqlite:///data/database.db").replace("sqlite:///", "")

def import_stores_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
    
    try:
        print("\n📥 Téléchargement des données magasins...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Lire le CSV
        df = pd.read_csv(StringIO(response.text), encoding='utf-8')
        
        with sqlite3.connect(DB_PATH) as conn:
            # Vérifier les données existantes
            existing_data = pd.read_sql_query("""
                SELECT store_id, city, employee_count 
                FROM stores
            """, conn)
            
            if not existing_data.empty:
                print(f"📊 Magasins existants : {len(existing_data)}")
            
            # Créer un nouveau DataFrame
            df_to_insert = pd.DataFrame({
                'store_id': df['ID Magasin'].astype(str),
                'city': df['Ville'],
                'employee_count': df['Nombre de salariÃ©s']
            })
            
            # Identifier les nouveaux magasins
            if not existing_data.empty:
                new_stores = df_to_insert[~df_to_insert['store_id'].isin(existing_data['store_id'])]
                
                print(f"📝 Nouveaux magasins à importer : {len(new_stores)}")
                
                if len(new_stores) > 0:
                    new_stores.to_sql('stores', conn, if_exists='append', index=False)
                    print(f"✅ {len(new_stores)} nouveaux magasins importés avec succès")
                else:
                    print("ℹ️ Aucun nouveau magasin à importer")
            else:
                print("📝 Importation de tous les magasins...")
                df_to_insert.to_sql('stores', conn, if_exists='append', index=False)
                print(f"✅ {len(df_to_insert)} magasins importés avec succès")
            
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM stores")
            total_stores = cursor.fetchone()[0]
            print(f"📊 Total des magasins dans la base : {total_stores}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'importation des magasins : {e}")
        import traceback
        print(traceback.format_exc())

def import_products_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
    
    try:
        print("\n📥 Téléchargement des données produits...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Lire le CSV
        df = pd.read_csv(StringIO(response.text), encoding='utf-8')
        
        with sqlite3.connect(DB_PATH) as conn:
            # Vérifier les données existantes
            existing_data = pd.read_sql_query("""
                SELECT product_id, product_name, price, stock 
                FROM products
            """, conn)
            
            if not existing_data.empty:
                print(f"📊 Produits existants : {len(existing_data)}")
            
            # Créer un nouveau DataFrame
            df_to_insert = pd.DataFrame({
                'product_id': df['ID RÃ©fÃ©rence produit'],
                'product_name': df['Nom'],
                'price': df['Prix'],
                'stock': df['Stock']
            })
            
            # Identifier les nouveaux produits
            if not existing_data.empty:
                new_products = df_to_insert[~df_to_insert['product_id'].isin(existing_data['product_id'])]
                
                print(f"📝 Nouveaux produits à importer : {len(new_products)}")
                
                if len(new_products) > 0:
                    new_products.to_sql('products', conn, if_exists='append', index=False)
                    print(f"✅ {len(new_products)} nouveaux produits importés avec succès")
                else:
                    print("ℹ️ Aucun nouveau produit à importer")
            else:                # Si la table est vide, importer toutes les données
                print("📝 Importation de tous les produits...")
                df_to_insert.to_sql('products', conn, if_exists='append', index=False)
                print(f"✅ {len(df_to_insert)} produits importés avec succès")
            
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products")
            total_products = cursor.fetchone()[0]
            print(f"📊 Total des produits dans la base : {total_products}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'importation des produits : {e}")
        import traceback
        print(traceback.format_exc())

def import_sales_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"
    
    try:
        print("\n📥 Téléchargement des données de ventes...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Lire le CSV
        df = pd.read_csv(StringIO(response.text), encoding='utf-8')
        
        with sqlite3.connect(DB_PATH) as conn:
            existing_data = pd.read_sql_query("""
                SELECT sale_date, product_id, store_id, quantity 
                FROM sales
            """, conn)
            
            if not existing_data.empty:
                print(f"📊 Données existantes : {len(existing_data)} ventes")
            
            # Créer un nouveau DataFrame
            df_to_insert = pd.DataFrame({
                'sale_date': df['Date'],
                'product_id': df['ID RÃ©fÃ©rence produit'],
                'quantity': df['QuantitÃ©'],
                'store_id': df['ID Magasin']
            })
            
            # Identifier les nouvelles ventes
            if not existing_data.empty:
                existing_data['key'] = existing_data['sale_date'] + '_' + existing_data['product_id'] + '_' + existing_data['store_id'].astype(str)
                df_to_insert['key'] = df_to_insert['sale_date'] + '_' + df_to_insert['product_id'] + '_' + df_to_insert['store_id'].astype(str)
                
                # Filtrer les nouvelles ventes
                new_sales = df_to_insert[~df_to_insert['key'].isin(existing_data['key'])]
                new_sales = new_sales.drop('key', axis=1)
                
                print(f"📝 Nouvelles ventes à importer : {len(new_sales)}")
                
                if len(new_sales) > 0:
                    new_sales.to_sql('sales', conn, if_exists='append', index=False)
                    print(f"✅ {len(new_sales)} nouvelles ventes importées avec succès")
                else:
                    print("ℹ️ Aucune nouvelle vente à importer")
            else:
                print("\n📝 Importation de toutes les données...")
                df_to_insert.to_sql('sales', conn, if_exists='append', index=False)
                print(f"✅ {len(df_to_insert)} ventes importées avec succès")
            
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sales")
            total_sales = cursor.fetchone()[0]
            print(f"📊 Total des ventes dans la base : {total_sales}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'importation : {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    import_sales_data()