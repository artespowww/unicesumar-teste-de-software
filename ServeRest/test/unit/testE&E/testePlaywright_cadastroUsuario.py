
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

    # Clicar em cadastrar
    botao_cadastrar = page.locator(
        'xpath=//*[@id="root"]/div/div/form/div[5]/button'
    )
    botao_cadastrar.click()

    # Validar redirecionamento
    expect(page).to_have_url(
        "https://front.serverest.dev/home"
    )

    print("========== DADOS DO CADASTRO ==========", flush=True)
    print(f"Nome: {nome_value}", flush=True)
    print(f"Email: {email_value}", flush=True)
    print(f"Senha: {senha_value}", flush=True)
    print("======================================", flush=True)
