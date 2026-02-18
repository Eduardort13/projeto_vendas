import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import random
from faker import Faker
import pandas as pd

load_dotenv()
fake = Faker('pt_BR')

def popular_produtos(qtd=100):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
        )

        if conn.is_connected():
            cursor = conn.cursor()
            print(f"📦 Populando {qtd} produtos no estoque...")

            # Categorias IDÊNTICAS ao seu ENUM do MySQL
            categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Outros']
            adjetivos = ['Pro', 'Gamer', 'Ultra', 'Wireless', 'Premium', 'v2']

            for _ in range(qtd):
                nome_p = f"{fake.word().capitalize()} {random.choice(adjetivos)}"
                desc_p = fake.sentence(nb_words=10)
                cat = random.choice(categorias) # Agora só escolhe o que o banco aceita
                preco = round(random.uniform(50.0, 5000.0), 2)
                estoque = random.randint(1, 150)

                query = """INSERT INTO produtos 
                           (nome_produto, descricao_produto, preco_produto, estoque_produto, categoria_produto) 
                           VALUES (%s, %s, %s, %s, %s)"""
                
                cursor.execute(query, (nome_p, desc_p, preco, estoque, cat))

            conn.commit()
            print("✅ Produtos inseridos com sucesso!")

            print("\n--- Resumo do Estoque (Pandas) ---")
            df = pd.read_sql("SELECT * FROM produtos", conn)
            
            print(df[['ID_produto', 'nome_produto', 'preco_produto', 'estoque_produto', 'categoria_produto']].head(20))
            
            valor_total = (df['preco_produto'] * df['estoque_produto']).sum()
            print(f"\n💰 Valor total em estoque: R$ {valor_total:,.2f}")

    except Error as e:
        print(f"❌ Erro: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Conexão fechada.")

if __name__ == "__main__":
    popular_produtos(100)