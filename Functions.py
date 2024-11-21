import sqlite3

# Funções
def cumprimentar_usuario():
    return "Olá! Eu sou a PharmacIA, sua assistente virtual da farmácia. Estou aqui para ajudar você a encontrar o medicamento que precisa, tirar dúvidas sobre nosso estoque e até ajudar com informações sobre receitas e compras. Como posso te ajudar hoje?"

def padronizar_nome(nome):
    # Remover aspas extras e espaços em branco, incluindo antes e depois
    nome = nome.strip('"').strip("'")
    return nome.strip().upper() 


# Função para buscar medicamentos no banco de dados
def buscar_medicamentos(nome):
    nome_padronizado = padronizar_nome(nome)
    
    conn = sqlite3.connect('farmacia.db', timeout=10)
    cursor = conn.cursor()
    query = "SELECT nome FROM medicamentos WHERE nome LIKE ?"
    cursor.execute(query, ('%' + nome_padronizado + '%',))
    medicamentos = cursor.fetchall()
    conn.close()

    if medicamentos:
        return "Medicamentos encontrados:\n" + "\n".join(f"* {medicamento[0]}" for medicamento in medicamentos)
    else:
        return "Nenhum medicamento encontrado com esse nome."

# Função para adicionar um medicamento ao carrinho
def adicionar_ao_carrinho(nome_medicamento, quantidade=1):
    nome_medicamento = padronizar_nome(nome_medicamento)
    nome_medicamento = nome_medicamento.strip().replace("\\", "")
    
    conn = sqlite3.connect('farmacia.db', timeout=10)
    cursor = conn.cursor()
    
    # Verificar se o medicamento existe na tabela de medicamentos
    cursor.execute("SELECT id, nome, preco FROM medicamentos WHERE nome LIKE ?", ('%' + nome_medicamento + '%',))
    medicamento = cursor.fetchone()
    
    if medicamento:
        medicamento_id, nome_encontrado, preco = medicamento
        
        # Verificar se o medicamento já está no carrinho
        cursor.execute("SELECT quantidade_no_carrinho FROM carrinho WHERE medicamento_id = ?", (medicamento_id,))
        existente = cursor.fetchone()
        
        if existente:
            # Atualizar a quantidade no carrinho
            nova_quantidade = existente[0] + quantidade
            cursor.execute("UPDATE carrinho SET quantidade_no_carrinho = ? WHERE medicamento_id = ?", (nova_quantidade, medicamento_id))
        else:
            # Adicionar o medicamento ao carrinho
            cursor.execute("INSERT INTO carrinho (medicamento_id, quantidade_no_carrinho) VALUES (?, ?)", (medicamento_id, quantidade))
        
        conn.commit()
        conn.close()
        return f"{nova_quantidade} unidades de {nome_encontrado} foram adicionadas ao seu carrinho."
    else:
        conn.close()
        return "Medicamento não encontrado."


# Função para consultar o estoque de um medicamento
def consultar_estoque(nome_medicamento):
    nome_medicamento = padronizar_nome(nome_medicamento)
    
    
    conn = sqlite3.connect('farmacia.db', timeout=10)
    cursor = conn.cursor()
    
    query = "SELECT nome, quantidade_estoque FROM medicamentos WHERE nome LIKE ?"
    cursor.execute(query, ('%' + nome_medicamento + '%',))
    medicamento = cursor.fetchone()
    conn.close()

    if medicamento:
        return f"O estoque do medicamento '{medicamento[0]}' é de {medicamento[1]} unidades."
    else:
        return "Medicamento não encontrado no estoque."

# Função para ver o conteúdo do carrinho
def ver_carrinho():
    conn = sqlite3.connect('farmacia.db', timeout=10)
    cursor = conn.cursor()
    
    # Consultar o conteúdo do carrinho com informações dos medicamentos
    query = """
    SELECT m.nome, m.preco, c.quantidade_no_carrinho
    FROM carrinho c
    JOIN medicamentos m ON c.medicamento_id = m.id
    """
    cursor.execute(query)
    carrinho = cursor.fetchall()
    conn.close()

    if carrinho:
        total = 0
        medicamentos_no_carrinho = []
        
        # Itera sobre os itens no carrinho
        for nome, preco, quantidade in carrinho:
            try:
                preco = float(preco)  # Garante que preco seja um número
                quantidade = int(quantidade)  # Garante que quantidade seja um número inteiro
                total += preco * quantidade
                medicamentos_no_carrinho.append(f"* {nome} - R${preco:.2f} x {quantidade}")
            except ValueError as e:
                # Caso ocorra um erro de conversão, trata-o
                print(f"Erro ao processar o item {nome}: {e}")
        
        if medicamentos_no_carrinho:
            return f"Medicamentos no seu carrinho:\n" + "\n".join(medicamentos_no_carrinho) + f"\n\nTotal: R${total:.2f}"
        else:
            return "Seu carrinho está vazio."
    else:
        return "Seu carrinho está vazio."

def remover_do_carrinho(nome_medicamento):
    print(f"Recebendo medicamento: {nome_medicamento}")
    nome_medicamento = padronizar_nome(nome_medicamento)
    print(f"Nome após padronização: {nome_medicamento}")
    
    conn = sqlite3.connect('farmacia.db', timeout=10)
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM medicamentos WHERE nome LIKE ?", ('%' + nome_medicamento + '%',))
    medicamento = cursor.fetchone()
    
    if medicamento:
        print(f"Medicamento encontrado com ID: {medicamento[0]}")
        medicamento_id = medicamento[0]
        cursor.execute("DELETE FROM carrinho WHERE medicamento_id = ?", (medicamento_id,))
        conn.commit()
        conn.close()
        return f"{medicamento[1]} foi removido do seu carrinho."
    else:
        print("Medicamento não encontrado.")
        conn.close()
        return f"Medicamento '{medicamento[1]}' não encontrado no carrinho."


def finalizar_compra():
    conn = sqlite3.connect('farmacia.db', timeout=10)
    cursor = conn.cursor()
    
    # Verificar se o carrinho está vazio
    cursor.execute("""
    SELECT m.nome, m.preco, c.quantidade_no_carrinho, m.precisa_receita
    FROM carrinho c
    JOIN medicamentos m ON c.medicamento_id = m.id
    """)
    carrinho = cursor.fetchall()

    if not carrinho:
        conn.close()
        return "Seu carrinho está vazio."

    medicamentos_com_receita = [medicamento[0] for medicamento in carrinho if medicamento[3]]
    
    if medicamentos_com_receita:
        lista_medicamentos = "\n".join(f"* {nome}" for nome in medicamentos_com_receita)
        conn.close()
        return (
            "Para concluir a compra, é necessário apresentar receita para os seguintes medicamentos:\n"
            f"{lista_medicamentos}"
        )

    # Calcular o total e limpar o carrinho
    total = sum(preco * quantidade for _, preco, quantidade, _ in carrinho)
    cursor.execute("DELETE FROM carrinho")
    conn.commit()
    conn.close()
    
    return f"Sua compra foi finalizada com sucesso. Total: R${total:.2f}"



def listar_todos_medicamentos():
    conn = sqlite3.connect('farmacia.db', timeout=10)
    cursor = conn.cursor()

    query = "SELECT nome, descricao, preco FROM medicamentos"
    cursor.execute(query)
    medicamentos = cursor.fetchall()

    conn.close()

    if medicamentos:
        return "Lista de todos os medicamentos:\n" + "\n".join(
            f"* {medicamento[0]} - {medicamento[1]} - R${medicamento[2]:.2f}" for medicamento in medicamentos
        )
    else:
        return "Nenhum medicamento encontrado no banco de dados."

# Função para verificar se um medicamento exige receita
def verificar_receita(nome_medicamento):
    nome_medicamento = padronizar_nome(nome_medicamento)
    
    conn = sqlite3.connect('farmacia.db', timeout=10)
    cursor = conn.cursor()
    
    query = "SELECT nome, precisa_receita FROM medicamentos WHERE nome LIKE ?"
    cursor.execute(query, ('%' + nome_medicamento + '%',))
    resultado = cursor.fetchone()
    conn.close()

    if resultado is not None:
        if resultado[1]:
            return f"O medicamento {resultado[0]} precisa de receita!"
        else:
            return f"O medicamento {resultado[0]} não precisa de receita!"
    else:
        return "Medicamento não encontrado."
    
def mostrar_todas_funcoes():
    return f"""
    Funções atualmente disponíveis do PharmacIA: 

        - Buscar medicamentos
        - Adicionar ao carrinho
        - Consultar estoque
        - Ver carrinho
        - Finalizar compra
        - Listar todos medicamentos
        - Verificar receita
        """


# Mapeamento das funções
mapa_funcoes = {
    "cumprimentar_usuario": cumprimentar_usuario,
    "buscar_medicamentos": buscar_medicamentos,
    "adicionar_ao_carrinho": adicionar_ao_carrinho,
    "consultar_estoque": consultar_estoque,
    "ver_carrinho": ver_carrinho,
    "finalizar_compra": finalizar_compra,
    "listar_todos_medicamentos": listar_todos_medicamentos,
    "verificar_receita": verificar_receita,
    'mostrar_todas_funcoes': mostrar_todas_funcoes
}

# Ferramentas do chatbot
ferramentas = [
    {
        "type": "function",
        "function": {
            "name": "buscar_medicamentos",
            "description": "Buscar por um medicamento específico",
            "parameters": {
                "type": "object",
                "properties": {"nome": {"type": "string", "description": "O nome do medicamento"}}},
            "required": ["nome"],
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cumprimentar_usuario",
            "description": "Cumprimentar o usuário e perguntar como ajudar",
            "parameters": {
                "type": "object",
                "properties": {},"required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "adicionar_ao_carrinho",
            "description": "Adicionar um medicamento ao carrinho",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_medicamento": {"type": "string", "description": "O nome do medicamento para adicionar"},
                },
                "required": ["nome_medicamento"],
            },
        },
    },
     {
        "type": "function",
        "function": {
            "name": "remover_do_carrinho",
            "description": "Remover um medicamento do carrinho",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_medicamento": {"type": "string", "description": "O nome do medicamento para remover"},
                },
                "required": ["nome_medicamento"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_estoque",
            "description": "Consultar o estoque de um medicamento específico",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_medicamento": {"type": "string", "description": "O nome do medicamento para consultar o estoque"},
                },
                "required": ["nome_medicamento"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ver_carrinho",
            "description": "Ver os medicamentos no carrinho e o total",
            "parameters": {
                "type": "object",
                "properties": {},"required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finalizar_compra",
            "description": "Finalizar a compra e processar o pagamento",
            "parameters": {
                "type": "object",
                "properties": {},"required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "listar_todos_medicamentos",
            "description": "Listar todos os medicamentos no banco de dados com descrição e preço",
            "parameters": {
                "type": "object",
                "properties": {},"required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "verificar_receita",
            "description": "Verificar se um medicamento exige receita médica",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_medicamento": {"type": "string", "description": "O nome do medicamento"},
                },
                "required": ["nome_medicamento"],
            },
        },
    }
]
