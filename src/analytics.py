# src/analytics.py
import sqlite3
import os
import pandas as pd

DB_PATH = os.getenv("DATABASE_URL", "sqlite:///data/database.db").replace("sqlite:///", "")

def get_total_revenue():
    """Calcule le chiffre d'affaires total et la période"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
            SELECT 
                SUM(s.quantity * p.price) as chiffre_affaires_total,
                MIN(s.sale_date) as date_debut,
                MAX(s.sale_date) as date_fin
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            """
            result = pd.read_sql_query(query, conn)
            return {
                'ca_total': result['chiffre_affaires_total'][0],
                'date_debut': result['date_debut'][0],
                'date_fin': result['date_fin'][0]
            }
    except Exception as e:
        print(f"❌ Erreur lors du calcul du CA total : {e}")
        return None

def get_sales_by_product():
    """Calcule les ventes par produit"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
            SELECT 
                p.product_name,
                SUM(s.quantity) as quantite_vendue,
                SUM(s.quantity * p.price) as chiffre_affaires,
                COUNT(s.sale_id) as nombre_ventes
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.product_id, p.product_name
            ORDER BY chiffre_affaires DESC
            """
            return pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"❌ Erreur lors du calcul des ventes par produit : {e}")
        return None

def get_sales_by_region():
    """Calcule les ventes par région"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
            SELECT 
                s.city as region,
                SUM(sa.quantity) as quantite_vendue,
                SUM(sa.quantity * p.price) as chiffre_affaires,
                COUNT(sa.sale_id) as nombre_ventes
            FROM sales sa
            JOIN stores s ON sa.store_id = s.store_id
            JOIN products p ON sa.product_id = p.product_id
            GROUP BY s.city
            ORDER BY chiffre_affaires DESC
            """
            return pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"❌ Erreur lors du calcul des ventes par région : {e}")
        return None

def display_analytics():
    """Affiche toutes les analyses"""
    print("\n📊 ANALYSE DES VENTES")
    print("=" * 50)
    
    # Chiffre d'affaires total
    ca_data = get_total_revenue()
    if ca_data is not None:
        print(f"\n⏱️ Chiffre d'affaires total sur la période du {ca_data['date_debut']} au {ca_data['date_fin']} :")
        print(f"{ca_data['ca_total']:.2f} €")
    
    # Ventes par produit
    print("\n💰 Ventes par produit :")
    ventes_produits = get_sales_by_product()
    if ventes_produits is not None:
        print(ventes_produits)
    
    # Ventes par région
    print("\n🏪 Ventes par région :")
    ventes_region = get_sales_by_region()
    if ventes_region is not None:
        print(ventes_region)

if __name__ == "__main__":
    display_analytics()