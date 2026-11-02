-- Camada Raw: mantém os valores do CSV como texto.
CREATE TABLE raw_vendas (
    id_raw BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    invoice_id TEXT,
    branch TEXT,
    city TEXT,
    customer_type TEXT,
    gender TEXT,
    product_line TEXT,
    unit_price TEXT,
    quantity TEXT,
    tax_5_percent TEXT,
    sales TEXT,
    date TEXT,
    time TEXT,
    payment TEXT,
    cogs TEXT,
    gross_margin_percentage TEXT,
    gross_income TEXT,
    rating TEXT
);

-- Confere o banco conectado e o conteúdo da tabela Raw.
SELECT current_database();

SELECT * FROM public.raw_vendas LIMIT 5;