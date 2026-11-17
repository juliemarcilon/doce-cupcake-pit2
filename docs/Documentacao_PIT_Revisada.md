# Documentação do Projeto — Loja Virtual Doce Cupcake (PIT I Revisado + PIT II)

## 1. Situação-Problema e Objetivo
A situação-problema trata do desenvolvimento de uma loja virtual de cupcakes gourmet (**Doce Cupcake**). O objetivo é estruturar funcionalidades de vitrine virtual com filtros por categoria e busca, cadastro e autenticação de usuários, carrinho de compras dinâmico, cálculo de frete, checkout online com endereço de entrega, confirmação de pedido e painel administrativo para gestão do catálogo.

## 2. Revisão e Melhorias Aplicadas (PIT I → PIT II)
Em conformidade com o ciclo de melhoria contínua (Kaizen) proposto no PIT II:
- **Escopo e Requisitos:** Mantidas as 5 Histórias de Usuário originais e implementada a interface administrativa (HU5) para cadastro de novos sabores no catálogo.
- **Modelagem UML:** Adicionado o **Diagrama de Classes** (`Diagrama_Classes.md`) contemplando as entidades `Usuario`, `Produto`, `Pedido` e `ItemPedido`.
- **Banco de Dados:** Elaborados o **Dicionário de Dados** (`Dicionario_Dados.md`) e o **Projeto Físico SQL** (`/database/database.sql`) utilizando SQLite.
- **Arquitetura de Software:** Aplicação desenvolvida no padrão **MVC (Model-View-Controller)** em Python (Flask), com testes unitários automatizados via `pytest`.

## 3. Histórias de Usuário (Revisadas)
| ID | História de Usuário | Status no PIT II |
| :--- | :--- | :--- |
| **HU1** | Como cliente, quero visualizar cupcakes disponíveis (por categoria ou busca) para escolher produtos. | Implementado |
| **HU2** | Como cliente, quero criar uma conta e fazer login para realizar pedidos online. | Implementado |
| **HU3** | Como cliente, quero adicionar cupcakes ao carrinho e ajustar quantidades para finalizar compras. | Implementado |
| **HU4** | Como cliente, quero informar endereço de entrega e realizar pagamentos online para concluir pedidos. | Implementado |
| **HU5** | Como administrador, quero cadastrar novos produtos para atualizar o catálogo da loja. | Implementado |

## 4. Backlog do Produto Priorizado
| ID | Funcionalidade / História | Prioridade |
| :--- | :--- | :--- |
| 1 | Cadastrar e autenticar usuário | Alta |
| 2 | Visualizar e filtrar cupcakes no catálogo | Alta |
| 3 | Adicionar e gerenciar itens no carrinho | Alta |
| 4 | Finalizar pedido e pagamento online | Alta |
| 5 | Gerenciar produtos (Painel Admin) | Média |

## 5. Artefatos e Diagramas UML
- **Diagrama de Classes UML:** `./Diagrama_Classes.md`
- **Diagrama de Atividades (Fluxo de Compra):** `./Diagrama_Atividades.md`
- **Dicionário de Dados:** `./Dicionario_Dados.md`
- **Protótipos de Tela (Wireframes):** `./wireframes_loja.jpg`