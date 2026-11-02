import os
from pathlib import Path
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

# Localiza a raiz do projeto e carrega suas configurações.
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ_PROJETO / ".env")

# Monta a conexão usando as configurações do .env.
url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(url)

# Consulta o nome do banco conectado.
with engine.connect() as conexao:
    banco = conexao.execute(text("SELECT current_database();")).scalar()
    print(f"Conectado ao banco: {banco}")

# engine.dispose()

# Consulta os campos originais, mantendo a ordem da carga.
consulta = text("""
    SELECT
        invoice_id, branch, city, customer_type, gender,
        product_line, unit_price, quantity, tax_5_percent,
        sales, "date", "time", payment, cogs,
        gross_margin_percentage, gross_income, rating
    FROM public.raw_vendas
    ORDER BY id_raw;
""")

with engine.connect() as conexao:
    df = pd.read_sql_query(consulta, conexao)

# Inspeção inicial.
print("\nPrimeiras cinco linhas:")
print(df.head())

print("\nQuantidade de linhas e colunas:")
print(df.shape)

print("\nTipos e quantidade de valores preenchidos:")
df.info()

print("\nValores ausentes por coluna:")
print(df.isna().sum())

print("\nQuantidade de linhas totalmente duplicadas:")
print(df.duplicated().sum())

# Exporta os dados sem incluir o índice do DataFrame.
destino = RAIZ_PROJETO / "data" / "raw" / "vendas_raw_exportadas.csv"
destino.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(destino, index=False, encoding="utf-8")

print(f"\nCSV exportado para: {destino}")

engine.dispose()