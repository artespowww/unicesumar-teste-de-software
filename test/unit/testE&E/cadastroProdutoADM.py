
from playwright.sync_api import Page, expect
import uuid
import secrets
import string
import time

def test_cadastro_usuario(page: Page):


    # Gerar informacoes aleatorias
    identificador = uuid.uuid4().hex[:8]
    #informacoes cadastro produto novo

    nome_produto = f"Produto Teste {identificador}"
    preco_produto = "100"
    desciricao_produto = f"Produto de teste para cadastro {identificador}"
    quantidade_produto = "10"

   

    nome_value = f"Usuario_{identificador}"
    email_value = f"teste_{identificador}@teste.com"
    senha_value = ''.join(
        secrets.choice(string.ascii_letters + string.digits)
        for _ in range(12)
    )

    # Acessar pagina
    page.goto("https://front.serverest.dev/login")

    # Clicar em Cadastre-se
    botao_cadastro = page.locator(
        'xpath=//*[@id="root"]/div/div/form/small/a'
    )
    botao_cadastro.click()

    expect(page).to_have_url(
        "https://front.serverest.dev/cadastrarusuarios"
    )

    # Preencher formulario
    nome = page.locator('xpath=//*[@id="nome"]')
    nome.fill(nome_value)

    email = page.locator('xpath=//*[@id="email"]')
    email.fill(email_value)

    senha = page.locator('xpath=//*[@id="password"]')
    senha.fill(senha_value)

    cadastro_adm = page.locator("#administrador")
    cadastro_adm.check()

    expect(cadastro_adm).to_be_checked()

    print("Administrador selecionado com sucesso")

    # Clicar em cadastrar
    botao_cadastrar = page.locator(
        'xpath=//*[@id="root"]/div/div/form/div[5]/button'
    )
    botao_cadastrar.click()






    #cadastrar produto
    botao_cadastro_produto = page.locator(
        'xpath=//*[@id="root"]/div/div/p[2]/div[4]/div/div/a'
    )
    botao_cadastro_produto.click()


    barra_nome_produto = page.locator('xpath=//*[@id="nome"]')
    barra_nome_produto.fill(nome_produto)
    barra_preco_produto = page.locator('xpath=//*[@id="price"]')
    barra_preco_produto.fill(preco_produto)
    barra_descricao_produto = page.locator('xpath=//*[@id="description"]')
    barra_descricao_produto.fill(desciricao_produto)
    barra_quantidade_produto = page.locator('xpath=//*[@id="quantity"]')
    barra_quantidade_produto.fill(quantidade_produto)

    botao_cadastrar_produto_interno = page.locator(
        'xpath=//*[@id="root"]/div/div/div/form/div[6]/div/button'
    )
    botao_cadastrar_produto_interno.click()

    expect(page).to_have_url(
        "https://front.serverest.dev/admin/listarprodutos"
    )

    print("Produto cadastrado com sucesso")