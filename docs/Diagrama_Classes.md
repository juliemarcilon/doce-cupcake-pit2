# Diagrama de Classes - Doce Cupcake

```mermaid
classDiagram
    class Usuario {
        +int id
        +string nome
        +string email
        +string senha
        +bool is_admin
        +cadastrar()
        +autenticar()
    }
    class Produto {
        +int id
        +string nome
        +string categoria
        +string descricao
        +float preco
        +int peso_gramas
        +listar()
        +cadastrar()
    }
    class Pedido {
        +int id
        +int usuario_id
        +string cep
        +string endereco
        +string numero
        +string complemento
        +string bairro
        +string cidade
        +string estado
        +float subtotal
        +float frete
        +float total
        +string status
        +datetime data_pedido
        +confirmar()
    }
    class ItemPedido {
        +int id
        +int pedido_id
        +int produto_id
        +int quantidade
        +float preco_unitario
    }

    Usuario "1" --> "0..*" Pedido : realiza
    Pedido "1" *-- "1..*" ItemPedido : contém
    Produto "1" --> "0..*" ItemPedido : compõe