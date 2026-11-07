
from playwright.sync_api import Page, expect
import uuid
import secrets
import string

def test_cadastro_usuario(page: Page):

    # Gerar informacoes aleatorias
    identificador = uuid.uuid4().hex[:8]

    nome_value = f"Usuario_{identificador}"
    email_value = f"teste_{identificador}@teste.com"
    senha_value = ''.join(
        secrets.choice(string.ascii_letters + string.digits)
        for _ in range(12)
    )

    # Acessar pagina
    page.goto("https://front.serverest.dev/login")

 #colocar as credenciais na tela de login que nao foram cadastradas antes.

    barra_email = page.locator('xpath=//*[@id="email"]')
    barra_email.fill(email_value)
    barra_senha = page.locator('xpath=//*[@id="password"]')
    barra_senha.fill(senha_value)

    botao_entrar = page.locator(
        'xpath=//*[@id="root"]/div/div/form/button'
    )
    botao_entrar.click()

    mensagem_erro = page.locator('xpath=//*[@id="root"]/div/div/form/div[1]/span')
    expect(mensagem_erro).to_have_text(
        "Email e/ou senha inválidos"   )
    
    print("Mensagem de erro exibida corretamente: Email e/ou senha inválidos")
