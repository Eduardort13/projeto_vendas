import mysql.connector              
from mysql.connector import Error   
from faker import Faker             
import pandas as pd                 
import os                           
from dotenv import load_dotenv      
import random 

load_dotenv()

fake = Faker('pt_BR')

def popular_endereco():
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
            
            cursor.execute("SELECT id_cliente FROM clientes")
            resultado = cursor.fetchall()  
            ids_clientes = [id[0] for id in resultado]

            print(f"Populando endereços para {len(ids_clientes)} clientes.")

            for id_cli in ids_clientes:
                logradouro = fake.street_name()
                numero = fake.building_number()
                complemento = random.choice(['Apto 101', 'Casa B', None])
                bairro = fake.bairro()
                cidade = fake.city()
                estado = fake.state_abbr()
                cep = fake.postcode().replace('-', '')
                tipo_endereco = random.choice(['Residencial', 'Entrega', 'Cobrança'])
                
                query = """
                INSERT INTO endereco 
                (logradouro, numero, complemento, bairro, cidade, estado, cep, tipo_endereco, clientes_ID_cliente) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(query, (logradouro, numero, complemento, bairro, cidade, estado, cep, tipo_endereco, id_cli))

            conn.commit()
            print("Dados inseridos com sucesso!")

            df = pd.read_sql("SELECT * FROM endereco", conn)
            print("\n--- Visualização dos Endereços ---")
            print(df.head(10))

    except Error as e:
        print(f"Erro ao inserir endereço: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("\nConexão encerrada.")

if __name__ == "__main__":
    popular_endereco()