import os
import json
from datetime import datetime

# ==================== ARQUIVOS ====================
ARQUIVOS = {
    "clientes": "clientes.json",
    "produtos": "produtos.json",
    "estoque": "estoque.json",
    "vendas": "vendas.json",
    "despesas": "despesas.json",
    "fornecedores": "fornecedores.json",
    "funcionarios": "funcionarios.json",
    "ponto": "ponto.json",
    "movimentacoes": "movimentacoes.json",
    "dispensas": "dispensas.json"
}

# ==================== FUNÇÕES DE ARQUIVO ====================
def carregar_arquivo(nome, default):
    if os.path.exists(ARQUIVOS[nome]):
        with open(ARQUIVOS[nome], "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def salvar_arquivo(nome, dados):
    with open(ARQUIVOS[nome], "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def criar_arquivos():
    for nome, arquivo in ARQUIVOS.items():
        if not os.path.exists(arquivo):
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write("[]")

# ==================== CARREGAR DADOS ====================
criar_arquivos()
clientes = carregar_arquivo("clientes", [])
produtos = carregar_arquivo("produtos", [])
estoque = carregar_arquivo("estoque", [])
vendas_realizadas = carregar_arquivo("vendas", [])
despesas = carregar_arquivo("despesas", [])
fornecedores = carregar_arquivo("fornecedores", [])
funcionarios = carregar_arquivo("funcionarios", [])
ponto = carregar_arquivo("ponto", [])
movimentacoes = carregar_arquivo("movimentacoes", [])
dispensas = carregar_arquivo("dispensas", [])

# ==================== UTIL ====================
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    input("\nPressione ENTER para continuar...")

# ==================== CLIENTES ====================
def cadastrar_cliente():
    nome = input("Nome do Cliente: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    contato = input("Contato adicional: ")
    clientes.append({"nome": nome, "telefone": telefone, "email": email, "contato": contato})
    salvar_arquivo("clientes", clientes)
    print("Cliente cadastrado com sucesso!")
    pausa()

def listar_clientes():
    if not clientes:
        print("Nenhum cliente cadastrado.")
        pausa()
        return
    print("===== LISTA DE CLIENTES =====")
    for i, c in enumerate(clientes):
        print(f"{i+1} - Nome: {c.get('nome','')}, Telefone: {c.get('telefone','')}, E-mail: {c.get('email','')}, Contato: {c.get('contato','')}")
    pausa()

def buscar_cliente():
    termo = input("Digite nome ou telefone do cliente: ").lower()
    encontrados = [c for c in clientes if termo in c.get('nome','').lower() or termo in c.get('telefone','')]
    if encontrados:
        for c in encontrados:
            print(f"Nome: {c.get('nome','')}, Telefone: {c.get('telefone','')}, E-mail: {c.get('email','')}, Contato: {c.get('contato','')}")
    else:
        print("Cliente não encontrado.")
    pausa()

def remover_cliente():
    listar_clientes()
    indice = input("Digite o número do cliente para remover (ou 0 para cancelar): ")
    if not indice.isdigit() or int(indice) < 0 or int(indice) > len(clientes):
        print("Opção inválida!")
        pausa()
        return
    if int(indice) == 0:
        return
    cliente = clientes.pop(int(indice)-1)
    salvar_arquivo("clientes", clientes)
    print(f"Cliente {cliente.get('nome','')} removido com sucesso!")
    pausa()

def submenu_clientes():
    while True:
        limpar_tela()
        print("\n--- CLIENTES ---")
        print("1 - Cadastrar Cliente")
        print("2 - Listar Clientes")
        print("3 - Buscar Cliente")
        print("4 - Remover Cliente")
        print("0 - Voltar")
        escolha = input("Escolha: ")
        if escolha == "1":
            cadastrar_cliente()
        elif escolha == "2":
            listar_clientes()
        elif escolha == "3":
            buscar_cliente()
        elif escolha == "4":
            remover_cliente()
        elif escolha == "0":
            break
        else:
            print("Opção inválida!")
            pausa()

# ==================== PRODUTOS / ESTOQUE ====================
def cadastrar_produto():
    nome = input("Nome do Produto: ")
    preco = float(input("Preço: R$ "))
    quantidade = int(input("Quantidade em estoque: "))
    produtos.append({"nome": nome, "preco": preco})
    estoque.append({"nome": nome, "quantidade": quantidade})
    movimentacoes.append({"tipo": "entrada", "produto": nome, "quantidade": quantidade, "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
    salvar_arquivo("produtos", produtos)
    salvar_arquivo("estoque", estoque)
    salvar_arquivo("movimentacoes", movimentacoes)
    print("Produto cadastrado com sucesso!")
    pausa()

def listar_produtos():
    if not produtos:
        print("Nenhum produto cadastrado.")
        pausa()
        return
    print("===== LISTA DE PRODUTOS =====")
    for i, p in enumerate(produtos):
        q = next((e.get('quantidade',0) for e in estoque if e.get('nome','') == p.get('nome','')), 0)
        print(f"{i+1} - Nome: {p.get('nome','')}, Preço: R$ {p.get('preco',0):.2f}, Estoque: {q}")
    pausa()

def adicionar_estoque():
    nome = input("Nome do produto: ")
    quantidade = int(input("Quantidade a adicionar: "))
    for e in estoque:
        if e.get('nome','').lower() == nome.lower():
            e['quantidade'] += quantidade
            movimentacoes.append({"tipo": "entrada", "produto": nome, "quantidade": quantidade, "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
            salvar_arquivo("estoque", estoque)
            salvar_arquivo("movimentacoes", movimentacoes)
            print("Estoque atualizado!")
            pausa()
            return
    print("Produto não encontrado.")
    pausa()

def remover_produto():
    nome = input("Nome do produto para remover: ")
    global produtos, estoque
    produtos = [p for p in produtos if p.get('nome','').lower() != nome.lower()]
    estoque = [e for e in estoque if e.get('nome','').lower() != nome.lower()]
    salvar_arquivo("produtos", produtos)
    salvar_arquivo("estoque", estoque)
    print("Produto removido se existia.")
    pausa()

def ver_estoque():
    print("===== ESTOQUE =====")
    for e in estoque:
        print(f"Produto: {e.get('nome','')}, Quantidade: {e.get('quantidade',0)}")
    pausa()

def submenu_produtos():
    while True:
        limpar_tela()
        print("\n--- PRODUTOS / ESTOQUE ---")
        print("1 - Cadastrar Produto")
        print("2 - Listar Produtos")
        print("3 - Adicionar Estoque")
        print("4 - Ver Estoque")
        print("5 - Remover Produto")
        print("0 - Voltar")
        escolha = input("Escolha: ")
        if escolha == "1":
            cadastrar_produto()
        elif escolha == "2":
            listar_produtos()
        elif escolha == "3":
            adicionar_estoque()
        elif escolha == "4":
            ver_estoque()
        elif escolha == "5":
            remover_produto()
        elif escolha == "0":
            break
        else:
            print("Opção inválida!")
            pausa()

# ==================== VENDAS ====================
def registrar_venda():
    nome_prod = input("Produto vendido: ")
    qtd = int(input("Quantidade: "))
    produto = next((p for p in produtos if p.get('nome','').lower() == nome_prod.lower()), None)
    if not produto:
        print("Produto não encontrado.")
        pausa()
        return
    estoque_item = next((e for e in estoque if e.get('nome','').lower() == nome_prod.lower()), None)
    if estoque_item['quantidade'] < qtd:
        print("Estoque insuficiente!")
        pausa()
        return
    valor_total = produto['preco'] * qtd
    vendas_realizadas.append({"produto": nome_prod, "quantidade": qtd, "valor": valor_total, "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
    estoque_item['quantidade'] -= qtd
    movimentacoes.append({"tipo": "saida", "produto": nome_prod, "quantidade": qtd, "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
    salvar_arquivo("vendas", vendas_realizadas)
    salvar_arquivo("estoque", estoque)
    salvar_arquivo("movimentacoes", movimentacoes)
    print(f"Venda registrada! Total: R$ {valor_total:.2f}")
    pausa()

def listar_vendas():
    if not vendas_realizadas:
        print("Nenhuma venda registrada.")
        pausa()
        return
    print("===== VENDAS =====")
    for i, v in enumerate(vendas_realizadas):
        print(f"{i+1} - Produto: {v.get('produto','')}, Quantidade: {v.get('quantidade',0)}, Valor: R$ {v.get('valor',0):.2f}, Data/Hora: {v.get('data','')}")
    pausa()

def submenu_vendas():
    while True:
        limpar_tela()
        print("\n--- VENDAS ---")
        print("1 - Registrar Venda")
        print("2 - Listar Vendas")
        print("0 - Voltar")
        escolha = input("Escolha: ")
        if escolha == "1":
            registrar_venda()
        elif escolha == "2":
            listar_vendas()
        elif escolha == "0":
            break
        else:
            print("Opção inválida!")
            pausa()

# ==================== FINANCEIRO ====================
def registrar_despesa():
    desc = input("Descrição da despesa: ")
    valor = float(input("Valor: R$ "))
    despesas.append({"descricao": desc, "valor": valor, "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
    salvar_arquivo("despesas", despesas)
    print("Despesa registrada.")
    pausa()

def ver_caixa():
    total_vendas = sum(v.get('valor',0) for v in vendas_realizadas)
    total_despesas = sum(d.get('valor',0) for d in despesas)
    saldo = total_vendas - total_despesas
    print(f"Total de vendas: R$ {total_vendas:.2f}")
    print(f"Total de despesas: R$ {total_despesas:.2f}")
    print(f"Saldo atual: R$ {saldo:.2f}")
    pausa()

def submenu_financeiro():
    while True:
        limpar_tela()
        print("\n--- FINANCEIRO ---")
        print("1 - Registrar Despesa")
        print("2 - Ver Caixa")
        print("0 - Voltar")
        escolha = input("Escolha: ")
        if escolha == "1":
            registrar_despesa()
        elif escolha == "2":
            ver_caixa()
        elif escolha == "0":
            break
        else:
            print("Opção inválida!")
            pausa()

# ==================== RH / FUNCIONÁRIOS ====================
def cadastrar_funcionario():
    nome = input("Nome: ")
    cargo = input("Cargo: ")
    salario = float(input("Salário: R$ "))
    funcionarios.append({"nome": nome, "cargo": cargo, "salario": salario})
    salvar_arquivo("funcionarios", funcionarios)
    print("Funcionário cadastrado!")
    pausa()

def listar_funcionarios():
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        pausa()
        return
    print("===== FUNCIONÁRIOS =====")
    for f in funcionarios:
        print(f"Nome: {f.get('nome','')}, Cargo: {f.get('cargo','')}, Salário: R$ {f.get('salario',0):.2f}")
    pausa()

def registrar_ponto():
    nome = input("Nome do funcionário: ")
    data = input("Data (dd/mm/aaaa): ")
    entrada = input("Hora entrada: ")
    saida = input("Hora saída: ")
    ponto.append({"nome": nome, "data": data, "entrada": entrada, "saida": saida})
    salvar_arquivo("ponto", ponto)
    print("Ponto registrado!")
    pausa()

def remover_funcionario():
    nome = input("Nome do funcionário para remover: ")
    motivo = input("Motivo da dispensa: ")
    global funcionarios
    removidos = [f for f in funcionarios if f.get('nome','').lower() == nome.lower()]
    for f in removidos:
        dispensas.append({"nome": f.get('nome',''), "cargo": f.get('cargo',''), "salario": f.get('salario',0), "motivo": motivo, "data": datetime.now().strftime("%d/%m/%Y")})
    funcionarios = [f for f in funcionarios if f.get('nome','').lower() != nome.lower()]
    salvar_arquivo("funcionarios", funcionarios)
    salvar_arquivo("dispensas", dispensas)
    print("Funcionário removido e histórico de dispensa registrado.")
    pausa()

def folha_pagamento():
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        pausa()
        return
    print("===== FOLHA DE PAGAMENTO =====")
    for f in funcionarios:
        print(f"Nome: {f.get('nome','')}, Cargo: {f.get('cargo','')}, Salário: R$ {f.get('salario',0):.2f}")
    pausa()

def submenu_rh():
    while True:
        limpar_tela()
        print("\n--- RH ---")
        print("1 - Cadastrar Funcionário")
        print("2 - Listar Funcionários")
        print("3 - Registrar Ponto")
        print("4 - Remover Funcionário")
        print("5 - Folha de Pagamento")
        print("0 - Voltar")
        escolha = input("Escolha: ")
        if escolha == "1":
            cadastrar_funcionario()
        elif escolha == "2":
            listar_funcionarios()
        elif escolha == "3":
            registrar_ponto()
        elif escolha == "4":
            remover_funcionario()
        elif escolha == "5":
            folha_pagamento()
        elif escolha == "0":
            break
        else:
            print("Opção inválida!")
            pausa()

# ==================== FORNECEDORES ====================
def cadastrar_fornecedor():
    nome = input("Nome do fornecedor: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    cnpj = input("CNPJ: ")
    fornecedores.append({"nome": nome, "telefone": telefone, "email": email, "cnpj": cnpj})
    salvar_arquivo("fornecedores", fornecedores)
    print("Fornecedor cadastrado.")
    pausa()

def listar_fornecedores():
    if not fornecedores:
        print("Nenhum fornecedor cadastrado.")
        pausa()
        return
    print("===== FORNECEDORES =====")
    for f in fornecedores:
        print(f"Nome: {f.get('nome','')}, Telefone: {f.get('telefone','')}, E-mail: {f.get('email','')}, CNPJ: {f.get('cnpj','')}")
    pausa()

def remover_fornecedor():
    nome = input("Nome do fornecedor para remover: ")
    global fornecedores
    fornecedores = [f for f in fornecedores if f.get('nome','').lower() != nome.lower()]
    salvar_arquivo("fornecedores", fornecedores)
    print("Fornecedor removido se existia.")
    pausa()

def submenu_fornecedores():
    while True:
        limpar_tela()
        print("\n--- FORNECEDORES ---")
        print("1 - Cadastrar Fornecedor")
        print("2 - Listar Fornecedores")
        print("3 - Remover Fornecedor")
        print("0 - Voltar")
        escolha = input("Escolha: ")
        if escolha == "1":
            cadastrar_fornecedor()
        elif escolha == "2":
            listar_fornecedores()
        elif escolha == "3":
            remover_fornecedor()
        elif escolha == "0":
            break
        else:
            print("Opção inválida!")
            pausa()

# ==================== RELATÓRIOS ====================
def relatorio_geral():
    print("===== RELATÓRIO GERAL =====")
    print(f"Total de clientes: {len(clientes)}")
    print(f"Total de produtos: {len(produtos)}")
    print(f"Total de vendas: {len(vendas_realizadas)}")
    print(f"Total de despesas: {len(despesas)}")
    print(f"Total de fornecedores: {len(fornecedores)}")
    print(f"Total de funcionários: {len(funcionarios)}")
    print("\n--- Movimentações de Estoque ---")
    for m in movimentacoes:
        print(f"{m.get('tipo','').capitalize()} - Produto: {m.get('produto','')}, Quantidade: {m.get('quantidade',0)}, Data/Hora: {m.get('data','')}")
    print("\n--- Dispensas de Funcionários ---")
    for d in dispensas:
        print(f"Nome: {d.get('nome','')}, Cargo: {d.get('cargo','')}, Salário: R$ {d.get('salario',0):.2f}, Motivo: {d.get('motivo','')}, Data: {d.get('data