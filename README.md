# cnpj-etl

ETL em Python puro que carrega os dados públicos de CNPJ da Receita Federal
(~29 milhões de empresas) em um banco SQLite consultável por linha de comando.

**Zero dependências externas.** Apenas a biblioteca padrão: `zipfile`, `csv`,
`sqlite3`, `decimal`, `dataclasses`, `argparse`. Sem pandas, sem ORM.

O objetivo do projeto é processar um volume que não cabe em memória e medir o
custo de cada decisão técnica, em vez de assumir o que é rápido.

---

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) para gerenciar o ambiente

```bash
git clone <url-do-repo>
cd cnpj-etl
uv sync
```

Os arquivos de origem não acompanham o repositório. Baixe os `.zip` de empresas
em [dados.gov.br — Cadastro Nacional da Pessoa Jurídica](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj)
e coloque em `data/zips/`.

---

## Uso

Criar o schema:

```bash
uv run scripts/criar_banco.py
```

Carregar um arquivo:

```bash
uv run etl.py carregar --zip data/zips/Empresas0.zip
```

```
gravado 29069564 empresas
```

Consultar:

```bash
uv run etl.py buscar --natureza 2135 --capital-min 20000 --limite 10
```

```
41273592  41.273.592 HELIO DE JESUS PEREIRA         R$      30,000.00
41273600  41.273.600 AVANILSON BRUNO MATIAS DA SIL   R$      50,000.00
41273606  MARCOS CESAR DE MELO JUNIOR 025693271     R$      72,000.00
```

Ambos os filtros são opcionais e combináveis. `uv run etl.py --help` lista os
comandos disponíveis.

---

## Decisões de projeto

Cada decisão abaixo foi tomada por um motivo específico e verificada com medição.

### Leitura preguiçosa (generator)

O maior arquivo tem ~2 GB descompactados. Carregar tudo em memória mata o
processo. `ler_empresas()` é um generator: produz um registro por vez, e o
consumo de memória fica constante independentemente do tamanho da entrada.

O pipeline inteiro — ler, converter e gravar — nunca materializa mais que um
registro mais o lote de gravação.

### `Decimal` na leitura, inteiro em centavos no banco

Valor monetário não pode ser `float`: o padrão IEEE 754 é binário e não
representa frações decimais exatamente (`0.1 + 0.2 == 0.30000000000000004`).

O SQLite não tem tipo decimal — só `INTEGER`, `REAL`, `TEXT`, `BLOB`. A primeira
versão gravava como `TEXT`, o que preserva o valor mas quebra a comparação:
texto compara lexicograficamente, então `'9000.00' > '1000000.00'` retorna
verdadeiro e a consulta devolve resultado errado **sem erro**.

A solução é armazenar o valor multiplicado por 100 como `INTEGER`. Exato,
comparável, somável e indexável. O custo é que o valor no banco não é legível
diretamente e toda leitura precisa converter.

### Transação em lote

Cada `commit()` força um `fsync()` — uma chamada de sistema que só retorna
quando o dado está fisicamente no disco. É a garantia de durabilidade (o "D" do
ACID), e custa milissegundos.

Commitar por linha significa 29 milhões de `fsync`. Agrupando 10.000 inserções
por transação, paga-se um `fsync` a cada 10.000 registros.

O tamanho do lote é um trade-off explícito: lote maior é mais rápido e consome
mais memória; lote menor perde menos dados se o processo for interrompido no
meio.

### Lookup em dicionário

As tabelas de referência (natureza jurídica, CNAE, município) são pequenas e
cabem em memória. Carregadas como `dict`, cada consulta é O(1) — contra O(n) de
uma busca linear em lista dentro do loop principal, que produziria O(n×m).

### Extração idempotente

`obter_csv()` verifica se o CSV já existe antes de descompactar e devolve
`(caminho, foi_extraido)`. Reexecutar o comando não gasta minutos
redescompactando 1 GB.

---

## Medições

Todos os tempos são de execuções reais. Windows e Linux aparecem separados
porque não são comparáveis entre si — o mesmo trabalho leva 91s no Windows e
26s no Linux, provavelmente pela inspeção do antivírus em cada leitura de disco.

### Leitura e conversão — 29.069.564 registros

| Variação | Tempo | Taxa |
|---|---|---|
| `print()` dentro do loop | ~1.200s (interrompido) | ~9 mil linhas/s |
| sem `print` no loop | 91,4s | 318 mil linhas/s |

**35x.** Mesma lógica; a única diferença é uma operação de I/O executada por
item em vez de por lote. O mesmo padrão reaparece três vezes neste projeto.

Complexidade verificada com dois arquivos de tamanhos diferentes:

| Arquivo | Registros | Tempo | Taxa |
|---|---|---|---|
| Empresas1 | 4.494.860 | 13,4s | 335 mil linhas/s |
| Empresas0 | 29.069.564 | 91,4s | 318 mil linhas/s |

6,5x mais dados, 6,8x mais tempo, taxa por registro praticamente constante —
comportamento O(n).

### Estrutura de dados — 29.069.564 registros, Linux

| Representação | Tempo | Taxa |
|---|---|---|
| `dict` | 25,96s | 1,12 mi linhas/s |
| `@dataclass` | 31,80s | 914 mil linhas/s |
| `@dataclass(slots=True)` | 32,90s | 884 mil linhas/s |

A `dataclass` custa +22% e vale: com `dict`, um erro de digitação no nome do
campo (`registro["razao_socail"]`) só aparece em runtime; com atributo, o
verificador de tipos acusa antes de executar.

**`slots=True` foi testado e descartado.** A hipótese era que eliminar o
`__dict__` por instância aceleraria — mas `slots` otimiza *acesso a atributo*, e
o loop de carga não lê atributo nenhum. Otimizar o que não é gargalo não ajuda,
e aqui piorou 3%.

### Carga no SQLite — 29.069.564 registros, Windows

| Estratégia | Tempo | Taxa |
|---|---|---|
| `execute` + `commit` por linha | ~2h20 (projetado) | ~3.500 linhas/s |
| `execute` + `commit` a cada 10.000 | 399,8s | 72,7 mil linhas/s |
| `executemany` + `commit` a cada 10.000 | 336,3s | 86,4 mil linhas/s |
| loop movido para dentro de função | 251,2s | 115,7 mil linhas/s |
| `capital_social` como `INTEGER` | 227,7s | 127,7 mil linhas/s |

Três observações:

- A transação em lote deu **21x**; o `executemany`, 1,16x. A primeira
  otimização certa vale mais que dez otimizações plausíveis.
- Mover o loop para dentro de uma função rendeu 25% sem nenhuma intenção de
  performance — variável local usa `LOAD_FAST` (índice em array) contra
  `LOAD_GLOBAL` (busca em dicionário), e a diferença aparece em 29 milhões de
  acessos. A refatoração foi feita por separação de responsabilidade; o ganho
  veio de brinde.
- Trocar `TEXT` por `INTEGER` foi uma correção de bug que também deixou 9% mais
  rápido, por ocupar menos bytes por registro.

### Índice — `natureza_juridica`

Índice criado em 34,1s.

| Filtro | Registros retornados | Sem índice | Com índice | Ganho |
|---|---|---|---|---|
| `= '2135'` | 20.343.707 (70% da tabela) | 22,023s | 1,403s | 15,7x |
| `= '3999'` | 278.274 (~1%) | 4,161s | 0,016s | 260x |

O plano de execução muda de `SCAN empresa` para
`SEARCH empresa USING COVERING INDEX`. *Covering index* significa que o índice
contém todas as colunas de que a consulta precisa, então o banco responde sem
visitar a tabela.

O ponto mais interessante é a diferença entre as duas linhas. **Sem índice, o
custo quase não depende do resultado** (22,0s e 4,2s para resultados 73x
diferentes) — ele lê a tabela inteira nos dois casos. **Com índice, o custo
passa a ser proporcional ao resultado.** É essa mudança de regime que importa,
não o número de aceleração: um índice não tem "fator de ganho", ele tem um
efeito que depende de quanto o filtro consegue descartar.

Índice não é grátis: custa 34s de construção, espaço em disco e uma atualização
de árvore a cada inserção futura. Por isso a carga é feita antes da criação dos
índices, e não o contrário.

### Lookup — 200.000 empresas contra 91 naturezas jurídicas

| Estrutura | Tempo |
|---|---|
| `list` + busca linear | 2,12s |
| `dict` (hash) | 0,85s |

2,5x com apenas 91 entradas na tabela de referência. O ganho cresce junto com
ela: 91 itens exigem ~45 comparações em média na busca linear; 5.500 municípios
exigiriam ~2.750. Com `dict`, sempre 1.

---

## Estrutura

A separação segue um critério: **o que faria este módulo mudar?** Cada arquivo
tem um único motivo de mudança.

```
cnpj-etl/
├── etl.py                    # CLI: subcomandos carregar e buscar
├── scripts/                  # executáveis avulsos (benchmarks, setup)
│   ├── criar_banco.py
│   ├── consultar.py          # experimento de índice
│   └── enriquecer.py         # experimento de lookup
└── src/cnpj/                 # pacote importável
    ├── modelo.py             # dataclass Empresa + ordem das colunas
    ├── aquisicao.py          # extração idempotente do zip
    ├── leitura.py            # CSV -> Empresa (generator)
    ├── referencia.py         # tabelas de domínio como dict
    ├── persistencia.py       # gravação em lote no SQLite
    └── consultar.py          # consultas com filtros opcionais
```

| Módulo | Muda quando |
|---|---|
| `modelo` | o layout do arquivo da Receita muda |
| `aquisicao` | a origem deixa de ser zip (download direto, outro formato) |
| `leitura` | o encoding, o separador ou o parsing muda |
| `referencia` | outra tabela de domínio precisa ser carregada |
| `persistencia` | a estratégia de gravação ou o banco muda |
| `consultar` | novos filtros são necessários |
| `etl` | a ordem das etapas ou a interface muda |

A direção das dependências aponta sempre para dentro, sem ciclos:

```
etl -> {aquisicao, leitura, persistencia, consultar} -> modelo
```

Módulos irmãos não se conhecem. `leitura` não sabe que o SQLite existe;
`persistencia` recebe um iterável de `Empresa` e não sabe se veio de CSV, de uma
API ou de uma lista fixa. Quem conhece a ordem das etapas é apenas o `etl.py`.

Funções de biblioteca não imprimem: `obter_csv()` devolve
`(caminho, foi_extraido)` e `carregar_naturezas()` devolve
`(mapa, linhas_ignoradas)`. A decisão de exibir é da camada de borda.

Conexões de banco são recebidas por parâmetro, nunca abertas dentro do módulo —
o que permite testar contra `sqlite3.connect(":memory:")`.

### SQL parametrizado

O filtro do comando `buscar` é montado dinamicamente, mas os valores nunca
entram na string do SQL:

```python
condicoes, valores = [], []

if natureza is not None:
    condicoes.append("natureza_juridica = ?")
    valores.append(natureza)

if condicoes:
    sql += " WHERE " + " AND ".join(condicoes)
```

Duas listas crescem em paralelo: uma com as condições e seus `?`, outra com os
valores. Isso dá o dinamismo sem abrir SQL injection, e permite que o banco
reaproveite o plano de execução preparado.

---

## Sobre os dados

Os dados da Receita são reais e, como todo dado real, são sujos:

- Sem cabeçalho — a ordem das colunas vem do layout oficial em PDF.
- Encoding Latin-1, separador `;`, campos entre aspas.
- Valores com vírgula decimal (`"5000,00"`).
- Campos vazios (`""`), que não são o mesmo que zero.
- Outliers evidentes: empresas individuais com capital social declarado de
  centenas de milhões, provavelmente erro de digitação na declaração. Qualquer
  agregação por capital precisa lidar com isso.

`carregar_naturezas()` conta e reporta linhas com formato inesperado em vez de
falhar ou aceitá-las silenciosamente.

---

## Limitações e próximos passos

- Só a tabela de empresas está implementada. Estabelecimentos, sócios, CNAEs e
  municípios ficaram de fora.
- O layout das colunas é descrito em três lugares (`COLUNAS`, a dataclass
  `Empresa` e o `CREATE TABLE`). Acrescentar uma coluna exige alterar os três,
  sem nada que avise se um for esquecido.
- Não há testes automatizados. As funções puras (`leitura`, `referencia`) e as
  que recebem conexão por parâmetro (`persistencia`) já são testáveis; falta
  escrever.
- `INSERT` simples: recarregar um arquivo já processado falha por violação de
  chave primária. Para reprocessamento, `INSERT OR IGNORE` seria mais adequado.
- A formatação monetária usa a convenção americana (`30,000.00`).