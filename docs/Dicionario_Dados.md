# Dicionário de Dados - Doce Cupcake

### Tabela: `usuarios`
| Campo | Tipo | Restrição | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, AUTOINCREMENT | Identificador único do usuário |
| `nome` | VARCHAR(100) | NOT NULL | Nome completo do cliente ou admin |
| `email` | VARCHAR(100) | NOT NULL, UNIQUE | E-mail de login |
| `senha` | VARCHAR(255) | NOT NULL | Senha de acesso |
| `is_admin` | BOOLEAN | DEFAULT 0 | Define se é administrador (1) ou cliente (0) |

### Tabela: `produtos`
| Campo | Tipo | Restrição | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, AUTOINCREMENT | Identificador único do cupcake |
| `nome` | VARCHAR(100) | NOT NULL | Nome/Sabor do produto |
| `categoria` | VARCHAR(50) | NOT NULL | Categoria (Chocolate, Frutados, Especiais, Kits) |
| `descricao` | TEXT | NOT NULL | Descrição detalhada do cupcake |
| `preco` | DECIMAL(10,2) | NOT NULL | Valor unitário em Reais (R$) |
| `peso_gramas` | INTEGER | DEFAULT 120 | Peso aproximado em gramas |

### Tabela: `pedidos`
| Campo | Tipo | Restrição | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, AUTOINCREMENT | Número identificador do pedido |
| `usuario_id` | INTEGER | FK (`usuarios.id`) | Cliente que realizou o pedido |
| `cep` | VARCHAR(10) | NOT NULL | CEP de entrega |
| `endereco` | VARCHAR(150) | NOT NULL | Logradouro de entrega |
| `numero` | VARCHAR(20) | NOT NULL | Número do endereço |
| `complemento` | VARCHAR(100) | NULL | Apto / Bloco (opcional) |
| `bairro` | VARCHAR(80) | NOT NULL | Bairro de entrega |
| `cidade` | VARCHAR(80) | NOT NULL | Cidade de entrega |
| `estado` | VARCHAR(2) | NOT NULL | Sigla da UF |
| `subtotal` | DECIMAL(10,2) | NOT NULL | Soma dos itens |
| `frete` | DECIMAL(10,2) | NOT NULL | Valor fixo do frete (R$ 8,00) |
| `total` | DECIMAL(10,2) | NOT NULL | Valor total pago |
| `status` | VARCHAR(30) | DEFAULT 'Confirmado' | Situação atual do pedido |
| `data_pedido` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Data e hora da confirmação |

### Tabela: `itens_pedido`
| Campo | Tipo | Restrição | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, AUTOINCREMENT | Identificador do item |
| `pedido_id` | INTEGER | FK (`pedidos.id`) | Pedido ao qual o item pertence |
| `produto_id` | INTEGER | FK (`produtos.id`) | Cupcake comprado |
| `quantidade` | INTEGER | NOT NULL | Quantidade comprada |
| `preco_unitario` | DECIMAL(10,2) | NOT NULL | Preço no momento da compra |