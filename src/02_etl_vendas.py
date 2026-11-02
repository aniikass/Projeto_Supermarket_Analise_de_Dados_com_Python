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

# Remove espaços nas extremidades dos textos.
for coluna in df.columns:
    df[coluna] = df[coluna].str.strip()

# Converte textos vazios em valores ausentes.
df = df.replace("", pd.NA)

print("\nValores ausentes após verificar espaços e campos vazios:")
print(df.isna().sum())

# Identifica linhas totalmente iguais.
duplicadas = df.duplicated()
print("\nLinhas totalmente duplicadas:", duplicadas.sum())

# Mantém uma ocorrência de cada linha totalmente igual.
df = df.drop_duplicates().copy()

# Verifica IDs repetidos, inclusive em linhas com valores diferentes.
ids_repetidos = df["id_venda"].duplicated(keep=False)
print("\nLinhas com ID de venda repetido:", ids_repetidos.sum())

print("\nTamanho após remover duplicadas:", df.shape)

# Converte as colunas numéricas e interrompe se houver texto inválido.
colunas_numericas = [
    "preco_unitario",
    "quantidade",
    "imposto",
    "valor_total",
    "custo_mercadoria",
    "margem_percentual",
    "receita_bruta",
    "avaliacao",
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="raise")

# Confere se as quantidades são inteiras antes da conversão.
if (df["quantidade"] % 1 != 0).any():
    raise ValueError("Existem quantidades com casas decimais.")

df["quantidade"] = df["quantidade"].astype("Int64")

print("\nTipos das colunas numéricas:")
print(df[colunas_numericas].dtypes)

# Converte as datas: mês/dia/ano no arquivo de origem.
df["data_venda"] = pd.to_datetime(
    df["data_venda"],
    format="%m/%d/%Y",
    errors="raise",
)

# Converte horários com AM/PM para objetos de horário.
df["hora_venda"] = pd.to_datetime(
    df["hora_venda"],
    format="%I:%M:%S %p",
    errors="raise",
).dt.time

print("\nDatas e horários convertidos:")
print(df[["id_venda", "data_venda", "hora_venda"]].head())