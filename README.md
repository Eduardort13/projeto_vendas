# Projeto End-to-End: Pipeline de Dados para BI

Este projeto automatiza o processo de geracao de dados, armazenamento em banco SQL e exportacao para analise de negocios.

## Estrutura do Projeto

- popular_produtos.py: Gera dados aleatorios de produtos.
- popular_clientes.py: Gera dados de clientes ficticios.
- popular_pedidos.py: Simula transacoes de vendas com precos historicos.
- setup_banco.py: Script principal que executa toda a carga de dados na ordem correta.
- gerar_excel.py: Extrai os dados do MySQL e gera um arquivo .xlsx para dashboards.

## Tecnologias Utilizadas

- Python
- MySQL
- Pandas (para tratamento de dados)
- Operadores LIKE e JOIN para consultas complexas

## Como Executar

1. Configure as credenciais no arquivo .env
2. Execute o arquivo setup_banco.py
3. O script gerar_excel.py criara o relatorio automaticamente para uso no Power BI ou Excel.