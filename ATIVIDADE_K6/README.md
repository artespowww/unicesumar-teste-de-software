# Atividade 05 — Testes de Desempenho com k6 no ServeRest

## 1. Objetivo

O objetivo desta atividade é compreender os fundamentos dos testes de desempenho e implementar testes de carga utilizando a ferramenta k6, analisando o comportamento da API ServeRest em diferentes condições de utilização.

Foram realizados dois cenários de testes: um com carga inicial de um usuário virtual e outro com aumento progressivo de usuários virtuais, chegando até 10 VUs.

Os testes foram executados exclusivamente em ambiente local, utilizando Docker para disponibilizar a API ServeRest.

---

## 2. Tecnologias utilizadas

- **k6:** ferramenta utilizada para executar os testes de desempenho.
- **JavaScript:** linguagem utilizada para implementar os scripts de testes.
- **Docker:** utilizado para executar a API ServeRest localmente.
- **ServeRest:** API utilizada como objeto dos testes.
- **Visual Studio Code:** editor utilizado para desenvolver e organizar os arquivos.

---

## 3. Pesquisa sobre os fundamentos do k6

### 3.1. Qual é a finalidade dos testes de desempenho e como os testes de carga se diferenciam dos testes funcionais?

Os testes de desempenho avaliam a capacidade de um sistema de responder às solicitações, considerando fatores como velocidade, estabilidade e quantidade de acessos simultâneos.

Os testes de carga verificam como o sistema se comporta quando recebe várias requisições ao mesmo tempo. Já os testes funcionais verificam se as funcionalidades estão funcionando corretamente, como consultar, cadastrar, alterar ou excluir informações.

### 3.2. O que são usuários virtuais (VUs) e como eles influenciam a carga gerada?

Os usuários virtuais (VUs) são usuários simulados pelo k6 que executam as operações definidas no script de teste.

Quanto maior a quantidade de VUs, maior poderá ser o número de requisições simultâneas enviadas à API. Isso permite observar como o sistema reage ao aumento de acessos.

### 3.3. Qual é a diferença entre checks e thresholds no k6?

Os checks verificam se uma resposta atende a determinada condição, como retornar o código HTTP 200.

Os thresholds definem critérios de desempenho, como o tempo máximo de resposta ou a taxa aceitável de falhas. Caso esses critérios não sejam atendidos, o k6 sinaliza que o teste não atingiu os objetivos estabelecidos.

### 3.4. O que representam as métricas http_req_duration, http_req_failed e http_reqs?

- **http_req_duration:** representa o tempo total gasto para realizar uma requisição HTTP e receber a resposta.
- **http_req_failed:** representa a taxa de requisições que apresentaram falhas.
- **http_reqs:** representa a quantidade total de requisições HTTP realizadas e sua taxa por segundo.

### 3.5. Qual é a importância do percentil 95 (p95) na análise dos tempos de resposta?

O percentil 95 representa o tempo dentro do qual 95% das requisições foram concluídas. Os outros 5% tiveram tempos de resposta superiores.

Essa métrica é importante porque permite identificar lentidões que poderiam passar despercebidas ao analisar somente o tempo médio, oferecendo uma visão melhor da experiência dos usuários.

---

## 4. Preparação do ambiente

### 4.1. Execução do ServeRest

A API ServeRest foi executada localmente utilizando Docker, por meio do seguinte comando:

```powershell
docker run -d --name serverest-local -p 3000:3000 paulogoncalvesbh/serverest:latest
```

Após iniciar o container, foi possível acessar a API pelo endereço:

http://localhost:3000

Também foi realizada a consulta ao endpoint:

http://localhost:3000/status

### 4.2. Instalação do k6

A instalação do k6 foi realizada no Windows utilizando o Winget:

```powershell
winget install k6 --source winget
```

Para verificar a instalação:

```powershell
k6 version
```

A ferramenta foi executada diretamente no Windows, enquanto a API permaneceu em execução no Docker.

---

## 5. Implementação dos testes

Foram desenvolvidos dois scripts utilizando JavaScript e a ferramenta k6.

Os endpoints utilizados foram:

- GET /produtos
- GET /usuarios

Ambos foram configurados para verificar o retorno HTTP 200.

A URL da API pode ser configurada por meio da variável de ambiente BASE_URL, sem necessidade de alterar a lógica dos scripts.

### 5.1. Cenário 1 — Carga inicial

O primeiro cenário foi configurado com:

- 1 usuário virtual (VU).
- Duração de 30 segundos.
- Requisições aos endpoints de produtos e usuários.
- Verificação dos códigos de resposta HTTP 200.

O objetivo foi observar o comportamento inicial da API com uma carga reduzida.

### 5.2. Cenário 2 — Carga progressiva

O segundo cenário utilizou stages para aumentar e reduzir gradualmente a quantidade de usuários virtuais.

A configuração foi:

| Etapa | Duração | Usuários virtuais |
|---|---:|---:|
| Inicial | 15 segundos | 1 |
| Crescimento | 15 segundos | 5 |
| Pico | 15 segundos | 10 |
| Redução | 15 segundos | 5 |
| Finalização | 15 segundos | 0 |

A duração planejada dos estágios foi de 75 segundos.

O objetivo foi observar se o aumento da quantidade de usuários provocaria alterações nos tempos de resposta ou na taxa de falhas.

### 5.3. Critérios de desempenho (Thresholds)

Foram definidos os seguintes critérios para os dois cenários:

| Métrica | Critério | Justificativa |
|---|---|---|
| http_req_duration | p95 < 1000 ms | Espera-se que 95% das requisições sejam concluídas em menos de 1 segundo. |
| http_req_failed | rate < 0.01 | A taxa de falhas deve permanecer abaixo de 1%. |
| checks | rate > 0.99 | Espera-se que mais de 99% das verificações sejam aprovadas. |

Esses critérios foram definidos para avaliar a estabilidade da API e estabelecer parâmetros de comparação entre os cenários.

---

## 6. Execução dos testes

Os testes foram executados pelo terminal do Windows, utilizando os seguintes comandos:

**Cenário 1:**

```powershell
k6 run --summary-export resultados/cenario-1.json tests/carga-inicial.js
```

**Cenário 2:**

```powershell
k6 run --summary-export resultados/cenario-2.json tests/carga-progressiva.js
```

Os resultados foram coletados por meio das métricas disponibilizadas pelo k6.

---

## 7. Resultados obtidos

### 7.1. Cenário 1 — Carga inicial

Configuração: 1 usuário virtual durante 30 segundos.

Resultados observados:

| Indicador | Resultado |
|---|---:|
| Usuários virtuais | 1 |
| Duração | 30 segundos |
| Iterações | 30 |
| Total de requisições | 60 |
| Requisições por segundo | 1,967004 |
| Tempo médio de resposta | 7,26 ms |
| Tempo mínimo | 2,15 ms |
| Tempo máximo | 79,41 ms |
| Percentil 95 (p95) | 10,6 ms |
| Taxa de falhas | 0% |
| Checks realizados | 60 |
| Checks aprovados | 100% (60 de 60) |
| Checks reprovados | 0 |

**Resultado dos thresholds:**

Todos os critérios de desempenho foram aprovados.

O endpoint GET /produtos retornou HTTP 200 e o endpoint GET /usuarios também retornou HTTP 200 em todas as verificações realizadas.

### 7.2. Cenário 2 — Carga progressiva

Configuração: aumento gradual de 1 até 10 usuários virtuais, seguido pela redução da carga.

Resultados observados na captura:

| Indicador