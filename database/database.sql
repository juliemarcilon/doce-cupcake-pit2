CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    descricao TEXT NOT NULL,
    preco REAL NOT NULL,
    peso_gramas INTEGER DEFAULT 120
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    cep TEXT NOT NULL,
    endereco TEXT NOT NULL,
    numero TEXT NOT NULL,
    complemento TEXT,
    bairro TEXT NOT NULL,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    subtotal REAL NOT NULL,
    frete REAL NOT NULL,
    total REAL NOT NULL,
    status TEXT DEFAULT 'Confirmado',
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- Dados iniciais (Catálogo do Wireframe)
INSERT INTO produtos (nome, categoria, descricao, preco, peso_gramas) VALUES
('Cupcake Chocolate', 'Chocolate', 'Delicioso cupcake de chocolate com cobertura cremosa e granulado.', 10.00, 120),
('Cupcake Morango', 'Frutados', 'Massa leve de baunilha com recheio e cobertura de morango fresco.', 12.00, 120),
('Cupcake Red Velvet', 'Especiais', 'Clássico veludo vermelho com cobertura suave de cream cheese.', 11.00, 120),
('Cupcake Oreo', 'Chocolate', 'Massa de cacau intenso com creme de baunilha e pedaços de Oreo.', 12.00, 120),
('Cupcake Limão Siciliano', 'Frutados', 'Refrescante massa cítrica com merengue suíço maçaricado.', 10.00, 120),
('Cupcake Paçoca', 'Especiais', 'Sabor brasileiro com cobertura cremosa de amendoim e paçoca.', 11.00, 120),
('Cupcake Leite Ninho', 'Especiais', 'Massa fofinha recheada com brigadeiro gourmet de Leite Ninho.', 12.00, 120),
('Kit 6 Unidades', 'Kits', 'Caixa presenteável com 6 cupcakes variados à escolha da casa.', 60.00, 720);