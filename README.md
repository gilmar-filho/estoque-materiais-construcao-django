# Sistema de Gerenciamento de Estoque para Materiais de Construção

**Disciplina:** GAC116 — Programação Web  
**Instituição:** Universidade Federal de Lavras (UFLA)  
**Projeto:** Projeto Prático I

---

## Integrantes

- Gilmar Silva de Medeiros Filho
- João Marcus Leite Silva

---

## Descrição do Projeto

Este repositório contém o sistema desenvolvido para a disciplina de Programação Web da UFLA. A proposta consiste na implementação de um sistema de gerenciamento de estoque voltado a uma loja de materiais de construção, com suporte a controle de entradas, saídas e reservas de produtos, desenvolvido com o framework Django.

O sistema adota uma arquitetura orientada a aplicações modulares, separando as responsabilidades em três domínios distintos: gerenciamento de usuários (`core`), controle de estoque (`estoque`) e interface de reservas (`vitrine`). A comunicação entre os módulos é realizada por meio do mecanismo de signals do Django, garantindo consistência dos dados sem acoplamento direto entre as aplicações.

---

## Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.12 | Linguagem principal |
| Django 6.0 | Framework web |
| PostgreSQL 15 | Banco de dados relacional |
| Cloudinary | Armazenamento de imagens em nuvem |
| Django Unfold | Customização da interface administrativa |
| Docker / Docker Compose | Conteinerização e orquestração do ambiente |
| django-environ | Gerenciamento de variáveis de ambiente |

---

## Arquitetura do Sistema

O projeto está organizado em três aplicações Django independentes, cada uma responsável por um domínio específico da lógica de negócio.

### `apps/core` — Gerenciamento de Usuários

Responsável pela autenticação e controle de acesso. Define um modelo de usuário customizado (`Usuario`) que estende o `AbstractUser` nativo do Django, acrescentando os campos `role` e `telefone`.

O campo `role` distingue dois perfis de uso: `ADMIN`, com acesso irrestrito ao painel administrativo, e `CLIENTE`, destinado aos usuários finais que realizam reservas de produtos.

### `apps/estoque` — Controle de Estoque

Núcleo do sistema. Contém a modelagem dos produtos e o registro de todas as movimentações de estoque. As entidades centrais são:

- **`Categoria` e `Marca`:** classificações auxiliares dos produtos, protegidas contra deleção enquanto houver produtos vinculados.
- **`Fornecedor`:** representa as empresas ou pessoas físicas que abastecem o estoque. O campo `cnpj_cpf` possui restrição de unicidade.
- **`Produto`:** entidade central, com três campos dedicados ao controle de estoque — `quantidade_fisica`, `quantidade_reservada` e `estoque_minimo`. Esses campos são atualizados automaticamente via signals, não por edição direta.
- **`MovimentacaoEstoque`:** registra cada evento de alteração do estoque físico, classificado em `ENTRADA`, `SAIDA` ou `AJUSTE_PERDA`. Toda entrada de estoque exige um fornecedor vinculado, regra validada na camada de formulário do painel administrativo.

### `apps/vitrine` — Reservas de Produtos

Responsável pelo fluxo de reserva por parte dos clientes. Composta por duas entidades:

- **`Reserva`:** associa um cliente a um conjunto de itens, com ciclo de vida definido pelos status `PENDENTE`, `CONCLUIDO` e `CANCELADO`.
- **`ItemReserva`:** linha individual da reserva, registrando o produto, a quantidade e o `preco_unitario` no momento da reserva (snapshot de preço, dissociado de alterações futuras no cadastro do produto).

---

## Fluxo de Dados e Lógica de Negócio

O sistema opera em dois fluxos principais, ambos com impacto direto nos campos de estoque do modelo `Produto`.

### Fluxo de Entrada de Estoque

Ao registrar uma `MovimentacaoEstoque` do tipo `ENTRADA` pelo painel administrativo, o signal `atualizar_estoque_fisico` é disparado via `post_save`, incrementando o campo `quantidade_fisica` do produto correspondente. Movimentações dos tipos `SAIDA` e `AJUSTE_PERDA` decrementam o mesmo campo pelo mesmo mecanismo.

### Fluxo de Reserva e Retirada

Quando um `ItemReserva` é criado, o signal `adicionar_reserva` incrementa o campo `quantidade_reservada` do produto. Caso o item seja removido, o signal `remover_reserva` realiza o decremento correspondente.

A conclusão de uma reserva — transição do status para `CONCLUIDO` — é tratada diretamente no método `save_model` do painel administrativo, dentro de uma transação atômica (`transaction.atomic`). Nesse momento, para cada item da reserva, o sistema verifica a disponibilidade de estoque físico e, em caso de suficiência, decrementa simultaneamente `quantidade_fisica` e `quantidade_reservada`. Se o estoque for insuficiente para qualquer item, a transação é revertida e uma mensagem de erro é exibida ao administrador, sem alterar o status da reserva.

### Restrições Relevantes para consistência do Banco de Dados

| Entidade | Restrição |
|---|---|
| `Fornecedor.cnpj_cpf` | Unicidade (`UNIQUE`) |
| `Produto.categoria` / `.marca` | Deleção bloqueada se houver produtos vinculados (`PROTECT`) |
| `Produto` | Deleção bloqueada se houver `ItemReserva` vinculado (`PROTECT`) |
| `MovimentacaoEstoque.produto` | Deleção em cascata junto ao produto (`CASCADE`) |
| `MovimentacaoEstoque.fornecedor` | Anulado em caso de deleção do fornecedor (`SET_NULL`) |
| `Reserva.cliente` | Deleção do usuário bloqueada se houver reservas (`PROTECT`) |
| `ItemReserva.reserva` | Deleção em cascata junto à reserva (`CASCADE`) |
| `MovimentacaoEstoque` tipo `ENTRADA` | Fornecedor obrigatório (validação na camada de formulário) |

---

## Mecanismo de Signals

O projeto utiliza o sistema de signals do Django para manter a consistência dos campos de estoque sem acoplamento direto entre as aplicações `estoque` e `vitrine`. Os três signals implementados em `apps/estoque/signals.py` são:

- **`adicionar_reserva`** (`post_save` em `ItemReserva`, somente em criações): incrementa `quantidade_reservada` do produto.
- **`remover_reserva`** (`post_delete` em `ItemReserva`): decrementa `quantidade_reservada` do produto.
- **`atualizar_estoque_fisico`** (`post_save` em `MovimentacaoEstoque`, somente em criações): incrementa ou decrementa `quantidade_fisica` conforme o tipo da movimentação.

O registro dos signals ocorre no método `ready()` da classe `EstoqueConfig`, garantindo que sejam carregados junto à inicialização da aplicação.

---

## Configuração e Execução

### Pré-requisitos

- Docker e Docker Compose instalados
- Conta configurada no Cloudinary

### Variáveis de Ambiente

Criar um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DEBUG=True
SECRET_KEY=sua_chave_secreta
DATABASE_URL=postgres://postgres:progweb@db:5432/construcao_db
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

### Execução

```bash
# Subir os containers
docker compose up --build

# Em outro terminal, aplicar as migrações
docker compose exec web python manage.py migrate

# Criar superusuário para acesso ao painel administrativo
docker compose exec web python manage.py createsuperuser
```

O painel administrativo estará disponível em `http://localhost:8000/admin/`.

---

## Estrutura de Diretórios Principal

```
.
├── apps/
│   ├── core/          # Modelo de usuário customizado
│   ├── estoque/       # Produtos, categorias, fornecedores e movimentações
│   └── vitrine/       # Reservas e itens de reserva
├── config/            # Configurações do projeto Django (settings, urls, wsgi)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```
