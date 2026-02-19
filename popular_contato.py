import mysql.connector              
from mysql.connector import Error   
from faker import Faker             
import pandas as pd                 
import os                           
from dotenv import load_dotenv      
import random 

load_dotenv()

fake = Faker('pt_BR')

def popular_contatos():
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

            print(f"Populando contatos para {len(ids_clientes)} clientes.")

            opcoes_contato = ['E-mail', 'Telefone', 'WhatsApp']

            for id_cli in ids_clientes:
                contatos_para_gerar = random.sample(opcoes_contato, 2)
                
                for tipo in contatos_para_gerar:
                    tipo_contato = tipo
                    
                    if tipo == 'E-mail':
                        valor_contato = fake.email()
                    elif tipo == 'Telefone':
                        valor_contato = fake.phone_number() 
                    else: 
                        valor_contato = fake.cellphone_number() 
                    
                    query = """
                    INSERT INTO contato 
                    (tipo_contato, valor_contato, clientes_ID_cliente) 
                    VALUES (%s, %s, %s)
                    """
                    
                    cursor.execute(query, (tipo_contato, valor_contato, id_cli))

            conn.commit()
            print("Contatos inseridos com sucesso!")

            df = pd.read_sql("SELECT * FROM contato", conn)
            print("\n--- Amostra dos Contatos ---")
            print(df.head(15))
            print(f"\nTotal de registros na tabela contato: {len(df)}")

    except Error as e:
        print(f"Erro: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("\nConexão encerrada.")

if __name__ == "__main__":
    popular_contatos()