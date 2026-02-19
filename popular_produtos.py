import mysql.connector              
from mysql.connector import Error   
from faker import Faker             
import pandas as pd                 
import os                           
from dotenv import load_dotenv      
import random 

load_dotenv()

fake = Faker('pt_BR')

def popular_produtos(qtd=50):
    conn = None
    categorias_disponiveis = ['Eletrônicos', 'Roupas', 'Alimentos', 'Outros']
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
        )

        if conn.is_connected():
            cursor = conn.cursor()  
            print(f"Populando tabela com {qtd} produtos.")

            for _ in range(qtd):
                nome = fake.catch_phrase()
                descricao = fake.sentence(nb_words=10)
                preco = fake.pydecimal(left_digits=4, right_digits=2, min_value=10, max_value=2000)
                quantidade = fake.random_int(min=1, max=100)
                categoria = random.choice(categorias_disponiveis)
                
                
                query = "INSERT INTO produtos (nome_produto, descricao_produto, preco_produto, estoque_produto, categoria_produto) VALUES (%s, %s, %s, %s, %s)"
                
                cursor.execute(query, (nome, descricao, preco, quantidade, categoria))

            conn.commit()
            print("Dados inseridos na tabela.")

            print("Visualização de dados usando pandas")
            query_select = "SELECT * FROM produtos"
            
            df = pd.read_sql(query_select, conn)
            
            pd.set_option('display.max_columns', None)  
            pd.set_option('display.width', 1000)       
            
            print(df.head(35)) 
            print(f"\n Total de registros: {len(df)}")

    except Error as e:
        
        print(f"Erro: {e}")
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Fim do programa.")

if __name__ == "__main__":
    popular_produtos(50)                  