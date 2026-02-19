import mysql.connector
from mysql.connector import Error
from faker import Faker
import pandas as pd
import os
from dotenv import load_dotenv
import random

load_dotenv()
fake = Faker('pt_BR')

def popular_vendas_detalhado(qtd_pedidos=200):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
        )

        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT ID_cliente FROM clientes")
            ids_clientes = [c['ID_cliente'] for c in cursor.fetchall()]

            cursor.execute("SELECT ID_produto, preco_produto FROM produtos")
            lista_produtos = cursor.fetchall() 

            status_opcoes = ['Pendente', 'Pago', 'Processando', 'Enviado', 'Entregue', 'Cancelado']

            print(f"Gerando {qtd_pedidos} pedidos e seus itens.")

            for _ in range(qtd_pedidos):
                id_cliente = random.choice(ids_clientes)
                data_p = fake.date_time_between(start_date='-1y', end_date='now')
                status = random.choice(status_opcoes)
                
                query_pedido = """
                INSERT INTO pedidos (data_pedido, status_pedido, valor_total, clientes_ID_cliente) 
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query_pedido, (data_p, status, 0.00, id_cliente))
                id_do_pedido = cursor.lastrowid 

                
                n_itens = random.randint(1, 4) 
                escolhidos = random.sample(lista_produtos, n_itens)
                
                total_acumulado = 0

                for prod in escolhidos:
                    qtd = random.randint(1, 5)
                    preco_hist = float(prod['preco_produto'])
                    id_p = prod['ID_produto']
                    
                    total_acumulado += (qtd * preco_hist)

                    query_item = """
                    INSERT INTO pedido_itens (quantidade, preco_unitario_historico, produtos_ID_produto, pedidos_ID_pedidos) 
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_item, (qtd, preco_hist, id_p, id_do_pedido))

            
                cursor.execute("UPDATE pedidos SET valor_total = %s WHERE ID_pedidos = %s", (total_acumulado, id_do_pedido))

            conn.commit()
            print(f"{qtd_pedidos} pedidos gerados.")

        
            print("\nResumo dos últimos pedidos:")
            df = pd.read_sql("SELECT * FROM pedidos ORDER BY ID_pedidos DESC LIMIT 10", conn)
            print(df)

    except Error as e:
        print(f"Erro: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("\nFim do programa.")

if __name__ == "__main__":
    popular_vendas_detalhado(300) 