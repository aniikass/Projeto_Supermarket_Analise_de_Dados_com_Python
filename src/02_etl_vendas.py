from pathlib import Path

import pandas as pd

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
origem = RAIZ_PROJETO / "data" / "raw" / "vendas_raw_exportadas.csv"

# Lê como texto para controlar as conversões posteriormente.
df = pd.read_csv(origem, dtype="string")

# Adapta os nomes à tabela tratada.
nomes_colunas = {
    "invoice_id": "id_venda",
    "branch": "filial",
    "city": "cidade",
    "customer_type": "tipo_cliente",
    "gender": "genero",
    "product_line": "linha_produto",
    "unit_price": "preco_unitario",
    "quantity": "quantidade",
    "tax_5_percent": "imposto",
    "sales": "valor_total",
    "date": "data_venda",
    "time": "hora_venda",
    "payment": "forma_pagamento",
    "cogs": "custo_mercadoria",
    "gross_margin_percentage": "margem_percentual",
    "gross_income": "receita_bruta",
    "rating": "avaliacao",
}

df = df.rename(columns=nomes_colunas)

print("Tamanho da base:", df.shape)
print("\nNomes das colunas:")
print(df.columns.tolist())