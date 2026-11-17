from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import get_db, init_db, calcular_totais_carrinho

app = Flask(__name__)
app.secret_key = 'chave_secreta_doce_cupcake_pit2'

# Garante criação das tabelas ao iniciar
with app.app_context():
    conn = get_db()
    tabela = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produtos'").fetchone()
    conn.close()
    if not tabela:
        init_db()

@app.context_processor
def inject_cart_count():
    carrinho = session.get('carrinho', {})
    total_itens = sum(carrinho.values())
    return dict(total_itens_carrinho=total_itens)

# 1. CATÁLOGO
@app.route('/')
def catalogo():
    categoria = request.args.get('categoria', 'Todos')
    busca = request.args.get('q', '').strip()
    conn = get_db()
    
    query = "SELECT * FROM produtos WHERE 1=1"
    params = []
    if categoria != 'Todos':
        query += " AND categoria = ?"
        params.append(categoria)
    if busca:
        query += " AND nome LIKE ?"
        params.append(f"%{busca}%")
        
    produtos = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('catalogo.html', produtos=produtos, categoria_atual=categoria, busca=busca)

# 2. DETALHE DO PRODUTO
@app.route('/produto/<int:id>')
def detalhe(id):
    conn = get_db()
    produto = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for('catalogo'))
    return render_template('detalhe.html', produto=produto)

# 3. CARRINHO DE COMPRAS
@app.route('/carrinho')
def carrinho():
    carrinho_sessao = session.get('carrinho', {})
    itens = []
    conn = get_db()
    for prod_id, qtd in carrinho_sessao.items():
        prod = conn.execute("SELECT * FROM produtos WHERE id = ?", (prod_id,)).fetchone()
        if prod:
            itens.append({
                'id': prod['id'],
                'nome': prod['nome'],
                'preco': prod['preco'],
                'quantidade': qtd,
                'subtotal': round(prod['preco'] * qtd, 2)
            })
    conn.close()
    totais = calcular_totais_carrinho(itens)
    return render_template('carrinho.html', itens=itens, totais=totais)

@app.route('/carrinho/adicionar/<int:id>', methods=['POST'])
def adicionar_carrinho(id):
    qtd = int(request.form.get('quantidade', 1))
    carrinho = session.get('carrinho', {})
    prod_key = str(id)
    carrinho[prod_key] = carrinho.get(prod_key, 0) + qtd
    session['carrinho'] = carrinho
    flash("Cupcake adicionado ao carrinho!", "success")
    return redirect(request.referrer or url_for('catalogo'))

@app.route('/carrinho/atualizar/<int:id>/<acao>')
def atualizar_carrinho(id, acao):
    carrinho = session.get('carrinho', {})
    prod_key = str(id)
    if prod_key in carrinho:
        if acao == 'mais':
            carrinho[prod_key] += 1
        elif acao == 'menos':
            carrinho[prod_key] -= 1
            if carrinho[prod_key] <= 0:
                del carrinho[prod_key]
    session['carrinho'] = carrinho
    return redirect(url_for('carrinho'))

@app.route('/carrinho/remover/<int:id>', methods=['POST'])
def remover_carrinho(id):
    carrinho = session.get('carrinho', {})
    prod_key = str(id)
    if prod_key in carrinho:
        del carrinho[prod_key]
        session['carrinho'] = carrinho
        flash("Item removido do carrinho.", "info")
    return redirect(url_for('carrinho'))

# 4. LOGIN / CADASTRO
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        email = request.form.get('email')
        senha = request.form.get('senha')
        conn = get_db()
        
        if tipo == 'cadastro':
            nome = request.form.get('nome')
            try:
                cur = conn.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
                conn.commit()
                session['usuario_id'] = cur.lastrowid
                session['usuario_nome'] = nome
                session['is_admin'] = 0
                flash("Conta criada com sucesso!", "success")
                return redirect(url_for('catalogo'))
            except Exception:
                flash("E-mail já cadastrado!", "danger")
        else:
            user = conn.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha)).fetchone()
            if user:
                session['usuario_id'] = user['id']
                session['usuario_nome'] = user['nome']
                session['is_admin'] = user['is_admin']
                flash(f"Bem-vindo(a), {user['nome']}!", "success")
                return redirect(url_for('catalogo'))
            else:
                flash("E-mail ou senha inválidos.", "danger")
        conn.close()
    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('catalogo'))

# 5. FINALIZAR COMPRA (CHECKOUT)
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'usuario_id' not in session:
        flash("Faça login ou crie uma conta para finalizar o pedido.", "warning")
        return redirect(url_for('auth'))
        
    carrinho_sessao = session.get('carrinho', {})
    if not carrinho_sessao:
        flash("Seu carrinho está vazio.", "warning")
        return redirect(url_for('catalogo'))

    conn = get_db()
    itens = []
    for prod_id, qtd in carrinho_sessao.items():
        prod = conn.execute("SELECT * FROM produtos WHERE id = ?", (prod_id,)).fetchone()
        if prod:
            itens.append({'id': prod['id'], 'nome': prod['nome'], 'preco': prod['preco'], 'quantidade': qtd})
    totais = calcular_totais_carrinho(itens)

    if request.method == 'POST':
        cur = conn.execute("""
            INSERT INTO pedidos (usuario_id, cep, endereco, numero, complemento, bairro, cidade, estado, subtotal, frete, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session['usuario_id'], request.form['cep'], request.form['endereco'],
            request.form['numero'], request.form.get('complemento', ''),
            request.form['bairro'], request.form['cidade'], request.form['estado'],
            totais['subtotal'], totais['frete'], totais['total']
        ))
        pedido_id = cur.lastrowid
        for item in itens:
            conn.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item['id'], item['quantidade'], item['preco'])
            )
        conn.commit()
        conn.close()
        session['carrinho'] = {}
        return redirect(url_for('confirmacao', pedido_id=pedido_id))

    conn.close()
    return render_template('checkout.html', itens=itens, totais=totais)

# 6. CONFIRMAÇÃO E HISTÓRICO DE PEDIDOS
@app.route('/confirmacao/<int:pedido_id>')
def confirmacao(pedido_id):
    conn = get_db()
    pedido = conn.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,)).fetchone()
    conn.close()
    return render_template('confirmacao.html', pedido=pedido)

@app.route('/meus-pedidos')
def meus_pedidos():
    if 'usuario_id' not in session:
        flash("Faça login para visualizar seus pedidos.", "warning")
        return redirect(url_for('auth'))
    conn = get_db()
    pedidos = conn.execute(
        "SELECT * FROM pedidos WHERE usuario_id = ? ORDER BY id DESC",
        (session['usuario_id'],)
    ).fetchall()
    conn.close()
    return render_template('meus_pedidos.html', pedidos=pedidos)

# 7. ADMINISTRAÇÃO (HU5 - Cadastrar Produtos)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'):
        flash("Acesso restrito. Entre com admin@docecupcake.com / admin123", "danger")
        return redirect(url_for('auth'))
    conn = get_db()
    if request.method == 'POST':
        conn.execute(
            "INSERT INTO produtos (nome, categoria, descricao, preco, peso_gramas) VALUES (?, ?, ?, ?, ?)",
            (request.form['nome'], request.form['categoria'], request.form['descricao'], float(request.form['preco']), int(request.form['peso']))
        )
        conn.commit()
        flash("Novo cupcake cadastrado no catálogo!", "success")
    produtos = conn.execute("SELECT * FROM produtos").fetchall()
    conn.close()
    return render_template('admin.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)