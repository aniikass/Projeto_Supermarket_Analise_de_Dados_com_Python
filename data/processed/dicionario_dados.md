
# Dicionário de dados — vendas_tratadas.csv

Cada linha representa um registro de venda do dataset Supermarket Sales.
A base tratada contém 19 colunas.

CSV não armazena tipos de dados. Os tipos abaixo representam a
interpretação das colunas após o tratamento com Python/Pandas.

| Coluna            | Tipo lógico | Descrição e regras                                                                                                                                                                                                                                                                                                                                                                      |
| ----------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id_venda          | Texto        | Identificador da venda. Obrigatório e único. Origem: Invoice ID.                                                                                                                                                                                                                                                                                                                        |
| filial            | Texto        | Identificação da filial. Obrigatória. Origem: Branch.                                                                                                                                                                                                                                                                                                                                  |
| cidade            | Texto        | Cidade onde ocorreu a venda. Obrigatória. Origem: City.# Dicionário de dados — vendas_tratadas.csv<br /><br />Cada linha representa um registro de venda do dataset Supermarket Sales.<br />A base tratada contém 19 colunas.<br /><br />CSV não armazena tipos de dados. Os tipos abaixo representam a<br />interpretação das colunas após o tratamento com Python/Pandas.<br /> |
| tipo_cliente      | Texto        | Tipo de cliente: Member ou Normal. Origem: Customer type.                                                                                                                                                                                                                                                                                                                                 |
| genero            | Texto        | Gênero informado no dataset. Origem: Gender.                                                                                                                                                                                                                                                                                                                                             |
| linha_produto     | Texto        | Categoria dos produtos vendidos. Obrigatória. Origem: Product line.                                                                                                                                                                                                                                                                                                                      |
| preco_unitario    | Decimal      | Preço por unidade, maior ou igual a zero. Origem: Unit price.                                                                                                                                                                                                                                                                                                                            |
| quantidade        | Inteiro      | Quantidade de itens, maior que zero. Origem: Quantity.                                                                                                                                                                                                                                                                                                                                    |
| imposto           | Decimal      | Imposto da venda, maior ou igual a zero. Origem: Tax 5%.                                                                                                                                                                                                                                                                                                                                  |
| valor_total       | Decimal      | Valor da venda incluindo imposto, maior ou igual a zero. Origem: Sales.                                                                                                                                                                                                                                                                                                                   |
| data_venda        | Data         | Data da venda no formato AAAA-MM-DD. Origem interpretada como mês/dia/ano.                                                                                                                                                                                                                                                                                                               |
| hora_venda        | Horário     | Horário da venda no formato HH:MM:SS, de 24 horas.                                                                                                                                                                                                                                                                                                                                       |
| forma_pagamento   | Texto        | Forma de pagamento. Obrigatória. Origem: Payment.                                                                                                                                                                                                                                                                                                                                        |
| custo_mercadoria  | Decimal      | Custo da mercadoria, maior ou igual a zero. Origem: cogs.                                                                                                                                                                                                                                                                                                                                 |
| margem_percentual | Decimal      | Margem percentual informada na origem. Origem: gross margin percentage.                                                                                                                                                                                                                                                                                                                   |
| receita_bruta     | Decimal      | Campo gross income da origem, maior ou igual a zero. Nome adotado conforme o enunciado.                                                                                                                                                                                                                                                                                                   |
| avaliacao         | Decimal      | Avaliação do cliente, entre 0 e 10. Origem: Rating.                                                                                                                                                                                                                                                                                                                                     |
| ano_mes           | Texto        | Coluna derivada de data_venda, no formato AAAA-MM.                                                                                                                                                                                                                                                                                                                                        |
| dia_semana        | Inteiro      | Coluna derivada de data_venda: segunda-feira = 0 até domingo = 6.                                                                                                                                                                                                                                                                                                                        |

## Precisão numérica

O CSV tratado mantém a precisão numérica usada no tratamento, sem
arredondamento explícito para duas casas decimais.

A tabela PostgreSQL tratada_vendas foi definida com duas casas decimais
nos campos NUMERIC. A política de arredondamento deve ser aplicada e
documentada na etapa de carga.

## Observações

- O arquivo original permanece preservado em data/raw.
- As 17 colunas de origem foram renomeadas.
- ano_mes e dia_semana foram criadas no tratamento e não fazem parte
  da estrutura atual da tabela tratada_vendas.
- A igualdade observada entre gross income e Tax 5% é uma característica
  deste dataset, não uma regra geral de negócio.
- A moeda não foi confirmada nesta etapa; por isso, não se atribui
  automaticamente o símbolo R$ aos valores.# Dicionário de dados — vendas_tratadas.csv

  automaticamente o símbolo R$ aos valores.# Dicionário de dados — vendas_tratadas.csv



Cada linha representa um registro de venda do dataset Supermarket Sales.

A base tratada contém 19 colunas.



CSV não armazena tipos de dados. Os tipos abaixo representam a

interpretação das colunas após o tratamento com Python/Pandas.



| Coluna | Tipo lógico | Descrição e regras |

|---|---|---|

| id_venda | Texto | Identificador da venda. Obrigatório e único. Origem: Invoice ID. |

| filial | Texto | Identificação da filial. Obrigatória. Origem: Branch. |

| cidade | Texto | Cidade onde ocorreu a venda. Obrigatória. Origem: City. |

| tipo_cliente | Texto | Tipo de cliente: Member ou Normal. Origem: Customer type. |

| genero | Texto | Gênero informado no dataset. Origem: Gender. |

| linha_produto | Texto | Categoria dos produtos vendidos. Obrigatória. Origem: Product line. |

| preco_unitario | Decimal | Preço por unidade, maior ou igual a zero. Origem: Unit price. |

| quantidade | Inteiro | Quantidade de itens, maior que zero. Origem: Quantity. |

| imposto | Decimal | Imposto da venda, maior ou igual a zero. Origem: Tax 5%. |

| valor_total | Decimal | Valor da venda incluindo imposto, maior ou igual a zero. Origem: Sales. |

| data_venda | Data | Data da venda no formato AAAA-MM-DD. Origem interpretada como mês/dia/ano. |

| hora_venda | Horário | Horário da venda no formato HH:MM:SS, de 24 horas. |

| forma_pagamento | Texto | Forma de pagamento. Obrigatória. Origem: Payment. |

| custo_mercadoria | Decimal | Custo da mercadoria, maior ou igual a zero. Origem: cogs. |

| margem_percentual | Decimal | Margem percentual informada na origem. Origem: gross margin percentage. |

| receita_bruta | Decimal | Campo gross income da origem, maior ou igual a zero. Nome adotado conforme o enunciado. |

| avaliacao | Decimal | Avaliação do cliente, entre 0 e 10. Origem: Rating. |

| ano_mes | Texto | Coluna derivada de data_venda, no formato AAAA-MM. |

| dia_semana | Inteiro | Coluna derivada de data_venda: segunda-feira = 0 até domingo = 6. |



## Precisão numérica



O CSV tratado mantém a precisão numérica usada no tratamento, sem

arredondamento explícito para duas casas decimais.



A tabela PostgreSQL tratada_vendas foi definida com duas casas decimais

nos campos NUMERIC. A política de arredondamento deve ser aplicada e

documentada na etapa de carga.



## Observações



- O arquivo original permanece preservado em data/raw.

- As 17 colunas de origem foram renomeadas.

- ano_mes e dia_semana foram criadas no tratamento e não fazem parte

  da estrutura atual da tabela tratada_vendas.

- A igualdade observada entre gross income e Tax 5% é uma característica

  deste dataset, não uma regra geral de negócio.

- A moeda não foi confirmada nesta etapa; por isso, não se atribui

  automaticamente o símbolo R$ aos valores.
