import mysql.connector
from mysql.connector import Error
from faker import Faker
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

fake = Faker('pt_BR')

def popular_tabela(qtd=100):
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
            print(f"Populando tabela com {qtd} clientes.")

            for _ in range(qtd):
                nome = fake.name()
                cpf = fake.unique.cpf().replace('.','').replace('-','')
                data_nasc = fake.date_of_birth(minimum_age=18, maximum_age=80)
                
                query = "INSERT INTO clientes (nome_cliente, cpf_cliente, data_nascimento) VALUES (%s, %s, %s)"
                cursor.execute(query, (nome, cpf, data_nasc))

            conn.commit()
            print("Dados inseridos na tabela.")

            print("Visualização de dados usando pandas")
            query_select = "SELECT * FROM clientes"

            
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
    popular_tabela(100)