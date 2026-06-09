# Flask REST API — Venda de Ingressos 🎟️

## Estrutura do repositório

```
src/               ← Aplicação de venda de ingressos
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
