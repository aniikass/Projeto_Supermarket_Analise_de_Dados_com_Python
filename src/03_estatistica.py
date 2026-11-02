from decimal import Decimal
from pathlib import Path

import pandas as pd

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
origem = RAIZ_PROJETO / "data" / "processed" / "vendas_tratadas.csv"

# Lê a base produzida pelo ETL.
df = pd.read_csv(origem, dtype="string")

# Converte os valores monetários preservando as casas decimais.
df["valor_total"] = df["valor_total"].map(Decimal)

# Pergunta 1: quantas vendas existem na base tratada?
total_vendas = len(df)

# Pergunta 2: qual foi o faturamento total?
faturamento_total = sum(df["valor_total"], Decimal("0.00"))

print(f"Quantidade de vendas: {total_vendas}")
print(f"Faturamento total: {faturamento_total:.2f}")

# Perguntas 3, 4 e 5: quantidade de compras por grupo.
vendas_por_cidade = df.groupby("cidade").size().sort_values(ascending=False)
vendas_por_tipo = df.groupby("tipo_cliente").size().sort_values(ascending=False)
vendas_por_genero = df.groupby("genero").size().sort_values(ascending=False)

print("\nQuantidade de vendas por cidade:")
print(vendas_por_cidade)

print("\nQuantidade de compras por tipo de cliente:")
print(vendas_por_tipo)

print("\nQuantidade de compras por gênero:")
print(vendas_por_genero)

# Converte os campos necessários para os próximos cálculos.
df["quantidade"] = pd.to_numeric(df["quantidade"], errors="raise")
df["avaliacao"] = pd.to_numeric(df["avaliacao"], errors="raise")

# Pergunta 6: qual linha de produto vendeu mais itens?
itens_por_linha = (
    df.groupby("linha_produto")["quantidade"]
    .sum()
    .sort_values(ascending=False)
)

print("\nQuantidade de itens vendidos por linha de produto:")
print(itens_por_linha)

# Pergunta 7: qual foi a avaliação média geral?
avaliacao_media = df["avaliacao"].mean()

print(f"\nAvaliação média geral: {avaliacao_media:.2f}")

# Pergunta 8: qual foi a menor venda registrada?
menor_venda = df["valor_total"].min()

print(f"\nMenor valor de venda: {menor_venda:.2f}")

# Monta a resposta dos grupos com maior quantidade.
def resumir_lideres(contagens):
    maior_quantidade = contagens.max()
    lideres = contagens[contagens == maior_quantidade].index

    return (
        f"{', '.join(lideres)} — "
        f"{int(maior_quantidade)}"
    )


# Organiza as oito respostas em uma tabela.
respostas = pd.DataFrame([
    {
        "pergunta": "Quantas vendas existem na base tratada?",
        "resposta": str(total_vendas),
        "unidade": "vendas",
    },
    {
        "pergunta": "Qual foi o faturamento total?",
        "resposta": f"{faturamento_total:.2f}",
        "unidade": "unidade monetária da origem",
    },
    {
        "pergunta": "Qual cidade realizou mais vendas?",
        "resposta": resumir_lideres(vendas_por_cidade),
        "unidade": "vendas",
    },
    {
        "pergunta": "Qual tipo de cliente realizou mais compras?",
        "resposta": resumir_lideres(vendas_por_tipo),
        "unidade": "compras",
    },
    {
        "pergunta": "Qual gênero realizou mais compras?",
        "resposta": resumir_lideres(vendas_por_genero),
        "unidade": "compras",
    },
    {
        "pergunta": "Qual linha de produto vendeu mais itens?",
        "resposta": resumir_lideres(itens_por_linha),
        "unidade": "itens",
    },
    {
        "pergunta": "Qual foi a avaliação média geral?",
        "resposta": f"{avaliacao_media:.2f}",
        "unidade": "pontos na escala de 0 a 10",
    },
    {
        "pergunta": "Qual foi a menor venda registrada?",
        "resposta": f"{menor_venda:.2f}",
        "unidade": "unidade monetária da origem",
    },
])

# Salva as respostas.
pasta_resultados = RAIZ_PROJETO / "resultados"
pasta_resultados.mkdir(parents=True, exist_ok=True)

destino_respostas = pasta_resultados / "respostas_negocio.csv"

respostas.to_csv(
    destino_respostas,
    index=False,
    encoding="utf-8-sig",
)

print(f"\nRespostas salvas em: {destino_respostas}")