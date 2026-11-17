# Diagrama de Atividades UML — Fluxo de Compra (Doce Cupcake)

```mermaid
flowchart TD
    Start((Início)) --> A[Cliente acessa a Loja Virtual]
    A --> B[Visualiza Catálogo de Cupcakes]
    B --> C{Deseja filtrar ou buscar?}
    C -- Sim --> D[Filtra por Categoria ou Busca por Nome]
    D --> B
    C -- Não --> E[Seleciona Cupcake e Visualiza Detalhes]
    E --> F[Adiciona Cupcake ao Carrinho]
    F --> G{Continuar comprando?}
    G -- Sim --> B
    G -- Não --> H[Acessa Carrinho e Ajusta Quantidades]
    H --> I[Clica em Finalizar Compra]
    I --> J{Usuário autenticado?}
    J -- Não --> K[Realiza Login ou Cadastro]
    K --> L[Preenche Endereço e Forma de Pagamento]
    J -- Sim --> L
    L --> M[Confirma Pedido]
    M --> N[Sistema Registra Pedido no Banco e Exibe Comprovante]
    N --> End((Fim))