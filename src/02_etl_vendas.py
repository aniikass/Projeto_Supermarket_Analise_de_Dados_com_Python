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

# Verifica campos obrigatórios.
campos_obrigatorios = [
    "id_venda",
    "filial",
    "cidade",
    "linha_produto",
    "forma_pagamento",
]

if df[campos_obrigatorios].isna().any().any():
    raise ValueError("Existem campos obrigatórios sem valor.")

if df["id_venda"].duplicated().any():
    raise ValueError("Existem IDs de venda repetidos.")

# Verifica os limites numéricos.
campos_nao_negativos = [
    "preco_unitario",
    "imposto",
    "valor_total",
    "custo_mercadoria",
    "receita_bruta",
]

if (df[campos_nao_negativos] < 0).any().any():
    raise ValueError("Existem valores negativos não permitidos.")

if (df["quantidade"] <= 0).any():
    raise ValueError("Existem quantidades iguais ou menores que zero.")

if (~df["avaliacao"].between(0, 10)).any():
    raise ValueError("Existem avaliações fora do intervalo de 0 a 10.")

# Confere os cálculos com a precisão original.
tolerancia = 0.000001

conferencias = {
    "Custo = preço × quantidade": (
        df["custo_mercadoria"]
        - df["preco_unitario"] * df["quantidade"]
    ).abs() <= tolerancia,

    "Imposto = 5% do custo": (
        df["imposto"] - df["custo_mercadoria"] * 0.05
    ).abs() <= tolerancia,

    "Total = custo + imposto": (
        df["valor_total"]
        - (df["custo_mercadoria"] + df["imposto"])
    ).abs() <= tolerancia,

    "Receita bruta = imposto": (
        df["receita_bruta"] - df["imposto"]
    ).abs() <= tolerancia,
}

for descricao, resultado in conferencias.items():
    inconsistentes = ~resultado.fillna(False)
    print(f"\n{descricao}: {inconsistentes.sum()} inconsistências")

    if inconsistentes.any():
        print(df.loc[inconsistentes, ["id_venda"]].head())
        raise ValueError(f"Falha na conferência: {descricao}")

print("\nValidações concluídas sem inconsistências.")

# Cria colunas derivadas para análises por período.
df["ano_mes"] = df["data_venda"].dt.strftime("%Y-%m")
df["dia_semana"] = df["data_venda"].dt.dayofweek

print("\nColunas derivadas:")
print(df[["data_venda", "ano_mes", "dia_semana"]].head())

# Organiza os resultados das conferências de cálculo.
relatorio = pd.DataFrame([
    {
        "verificacao": descricao,
        "linhas_verificadas": len(df),
        "inconsistencias": int((~resultado.fillna(False)).sum()),
    }
    for descricao, resultado in conferencias.items()
])

# Cria a pasta, caso ainda não exista.
pasta_resultados = RAIZ_PROJETO / "resultados"
pasta_resultados.mkdir(parents=True, exist_ok=True)

destino_relatorio = pasta_resultados / "validacao_calculos.csv"

relatorio.to_csv(
    destino_relatorio,
    index=False,
    encoding="utf-8",
)

print(f"\nRelatório salvo em: {destino_relatorio}")

# Cria a pasta de saída, caso ainda não exista.
pasta_processed = RAIZ_PROJETO / "data" / "processed"
pasta_processed.mkdir(parents=True, exist_ok=True)

# Exporta a base tratada.
destino_tratado = pasta_processed / "vendas_tratadas.csv"

df.to_csv(
    destino_tratado,
    index=False,
    encoding="utf-8",
    date_format="%Y-%m-%d",
)

print(f"\nBase tratada salva em: {destino_tratado}")
print("Tamanho da base exportada:", df.shape)