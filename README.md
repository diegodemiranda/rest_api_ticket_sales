# Flask REST API — Tutorial + Venda de Ingressos

## Estrutura do repositório

```
flask_tutorial/          ← Implementação do tutorial Real Python (Partes 1 e 2)
│   app.py               ← Ponto de entrada (Connexion + Flask)
│   config.py            ← Instância compartilhada do SQLAlchemy
│   models.py            ← ORM Person + schema Marshmallow
│   people.py            ← Handlers CRUD das rotas /api/people
│   swagger.yml          ← Especificação OpenAPI 3.0
│   templates/
│       home.html        ← Front-end HTML que consome a API

ingressos/               ← Aplicação de venda de ingressos
│   app.py
│   config.py
│   models.py            ← ORM Evento + Ingresso + schemas
│   eventos.py           ← Handlers CRUD de /api/eventos
│   ingressos.py         ← Handlers compra/cancelamento de /api/ingressos
│   swagger.yml
│   templates/
│       home.html        ← Front-end completo de venda
```

---

## PARTE 1 — Tutorial (flask_tutorial/)

### Instalação

```bash
cd flask_tutorial
pip install Flask==2.2.2 "connexion[swagger-ui]==2.14.2" \
            "flask-marshmallow[sqlalchemy]==0.14.0" "marshmallow==3.20.1"
python app.py
```

Acesse: http://localhost:8000

### API de Pessoas

| Método | Rota                  | Descrição              |
|--------|-----------------------|------------------------|
| GET    | /api/people           | Lista todas as pessoas |
| POST   | /api/people           | Cria nova pessoa       |
| GET    | /api/people/{lname}   | Busca por sobrenome    |
| PUT    | /api/people/{lname}   | Atualiza pessoa        |
| DELETE | /api/people/{lname}   | Remove pessoa          |

Documentação Swagger: http://localhost:8000/api/ui

### Conceitos do Tutorial

- **Parte 1** — Flask + Connexion + OpenAPI: roteamento automático via `operationId`
  no `swagger.yml`, validação de entrada/saída, Swagger UI gerado automaticamente.

- **Parte 2** — SQLAlchemy + Marshmallow: banco SQLite persistente, ORM para
  mapear objetos Python ↔ tabelas, Marshmallow para serializar/deserializar JSON.

---

## PARTE 2 — Venda de Ingressos (ingressos/)

### Instalação

```bash
cd ingressos
python app.py
```

Acesse: http://localhost:8001  
Swagger UI: http://localhost:8001/api/ui

### API de Ingressos

**Eventos**

| Método | Rota                          | Descrição                        |
|--------|-------------------------------|----------------------------------|
| GET    | /api/eventos                  | Lista eventos com vagas          |
| POST   | /api/eventos                  | Cria novo evento                 |
| GET    | /api/eventos/{id}             | Detalhes + vagas de um evento    |
| PUT    | /api/eventos/{id}             | Atualiza evento                  |
| DELETE | /api/eventos/{id}             | Remove evento (cascade ingressos)|
| GET    | /api/eventos/{id}/ingressos   | Lista ingressos de um evento     |

**Ingressos**

| Método | Rota                   | Descrição                     |
|--------|------------------------|-------------------------------|
| GET    | /api/ingressos         | Lista todas as compras        |
| POST   | /api/ingressos         | Realiza compra de ingresso(s) |
| GET    | /api/ingressos/{id}    | Consulta ingresso             |
| DELETE | /api/ingressos/{id}    | Cancela ingresso              |

### Regras de negócio

- Quantidade por compra: mínimo 1, máximo 10.
- Valor total = `preco_evento × quantidade` (calculado pelo servidor).
- Compra bloqueada se `vagas_disponiveis < quantidade`.
- Ingresso cancelado muda `status` para `"cancelado"` (soft delete).
- `vagas_disponiveis` é calculado em tempo real: `capacidade − ingressos_vendidos`.
- Deleção de evento usa cascade: apaga todos os ingressos vinculados.

### Exemplo de compra via cURL

```bash
# 1. Listar eventos
curl http://localhost:8001/api/eventos

# 2. Comprar 2 ingressos para o evento ID 1
curl -X POST http://localhost:8001/api/ingressos \
  -H "Content-Type: application/json" \
  -d '{
    "evento_id": 1,
    "nome_cliente": "Diego Silva",
    "email_cliente": "diego@email.com",
    "cpf_cliente": "123.456.789-00",
    "quantidade": 2
  }'

# 3. Cancelar ingresso ID 1
curl -X DELETE http://localhost:8001/api/ingressos/1
```
