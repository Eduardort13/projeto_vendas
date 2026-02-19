import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def exportar_para_excel():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS')
    )
    
    query = """
    SELECT 
        p.ID_pedidos,
        p.data_pedido,
        p.status_pedido,
        c.nome_cliente,
        pr.nome_produto,
        pi.quantidade,
        pi.preco_unitario_historico,
        (pi.quantidade * pi.preco_unitario_historico) AS subtotal
    FROM pedidos p
    JOIN clientes c ON p.clientes_ID_cliente = c.ID_cliente
    JOIN pedido_itens pi ON p.ID_pedidos = pi.pedidos_ID_pedidos
    JOIN produtos pr ON pi.produtos_ID_produto = pr.ID_produto
    """
    
    df = pd.read_sql(query, conn)
    
    df.to_excel("relatorio_vendas.xlsx", index=False)
    
    print("Arquivo relatorio_vendas.xlsx foi gerado.")
    conn.close()

if __name__ == "__main__":
    exportar_para_excel()