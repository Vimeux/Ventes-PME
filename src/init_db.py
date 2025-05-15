# src/init_db.py
import sqlite3
import os

DB_PATH = os.getenv("DATABASE_URL", "sqlite:///data/database.db").replace("sqlite:///", "")

def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Table products
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                price REAL NOT NULL CHECK (price >= 0),
                stock INTEGER NOT NULL CHECK (stock >= 0)
            );
        """)
        
        # Table stores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stores (
                store_id TEXT PRIMARY KEY,
                city TEXT NOT NULL,
                employee_count INTEGER NOT NULL CHECK (employee_count > 0)
            );
        """)
        
        # Table sales avec les clés étrangères
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                product_id TEXT NOT NULL,
                store_id TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
                    ON DELETE RESTRICT
                    ON UPDATE CASCADE,
                FOREIGN KEY (store_id) REFERENCES stores(store_id)
                    ON DELETE RESTRICT
                    ON UPDATE CASCADE
            );
        """)
        
        conn.commit()
        print("✅ Tables créées avec succès")
        
        # Afficher les tables et leurs relations
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\n📋 Structure de la base de données :")
        for table in tables:
            print(f"\n📊 Table : {table[0]}")
            
            # Afficher les colonnes
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            print("  Colonnes :")
            for col in columns:
                print(f"    - {col[1]} ({col[2]})")
            
            # Afficher les clés étrangères
            cursor.execute(f"PRAGMA foreign_key_list({table[0]})")
            foreign_keys = cursor.fetchall()
            if foreign_keys:
                print("  Clés étrangères :")
                for fk in foreign_keys:
                    print(f"    - {fk[3]} -> {fk[2]}({fk[4]})")

if __name__ == "__main__":
    create_tables()