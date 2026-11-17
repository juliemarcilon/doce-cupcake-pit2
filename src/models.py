import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'doce_cupcake.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'database.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    
    # Cria usuário admin padrão se não existir
    admin = conn.execute("SELECT * FROM usuarios WHERE email = 'admin@docecupcake.com'").fetchone()
    if not admin:
        conn.execute(
            "INSERT INTO usuarios (nome, email, senha, is_admin) VALUES (?, ?, ?, ?)",
            ('Administrador', 'admin@docecupcake.com', 'admin123', 1)
        )
    conn.commit()
    conn.close()

def calcular_totais_carrinho(itens_carrinho, frete_fixo=8.00):
    subtotal = sum(item['preco'] * item['quantidade'] for item in itens_carrinho)
    frete = frete_fixo if subtotal > 0 else 0.00
    total = subtotal + frete
    return {'subtotal': round(subtotal, 2), 'frete': round(frete, 2), 'total': round(total, 2)}




def remover_item_carrinho(carrinho, produto_id):
    produto_id_str = str(produto_id)
    if produto_id_str in carrinho:
        del carrinho[produto_id_str]
    return carrinho

def listar_pedidos_usuario(usuario_id):
    conn = get_db_connection()
    pedidos = conn.execute(
        'SELECT * FROM pedidos WHERE usuario_id = ? ORDER BY data_pedido DESC',
        (usuario_id,)
    ).fetchall()
    conn.close()
    return pedidos