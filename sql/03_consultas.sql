-- Confere a quantidade de registros da camada Raw.
SELECT COUNT(*) AS total_vendas
FROM public.raw_vendas;

-- Mostra uma amostra dos dados.
SELECT *
FROM public.raw_vendas
ORDER BY id_raw
LIMIT 5;

-- Filtra as vendas de clientes Member.
SELECT *
FROM public.raw_vendas
WHERE customer_type = 'Member';

-- Conta as vendas por cidade.
SELECT city, COUNT(*) AS quantidade_vendas
FROM public.raw_vendas
GROUP BY city
ORDER BY quantidade_vendas DESC;