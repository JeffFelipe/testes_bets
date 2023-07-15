from playwright.sync_api import sync_playwright
import json
import time



login = 'zuriel123'
passw = 'zurielions123'


def aguardar(page, xpath):
    contador = 0
    while True:
        page.wait_for_timeout(2000)
        contador += 1
        if contador == 20 or contador == 40:
            page.reload()
        try:
            page.wait_for_selector(xpath)
            break
        except:
            pass


def puxar_historico(page):
    lista = page.wait_for_selector('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div').text_content()
    lista_dois = lista
    while lista_dois == lista:
        lista_dois = page.wait_for_selector('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div').text_content()
        time.sleep(1)
    return lista_dois


def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(storage_state='auth.json')
    page = context.new_page()
    page.goto("https://www.bettilt.com/en")
    page.wait_for_timeout(5000)
    login_button = page.locator('//html/body/div[1]/div[1]/div[1]/div/div[2]/button[1]/span')
    if login_button.is_visible():
        login_button.click()
        page.fill('input[name="username"]', login)
        page.fill('input[name="password"]', passw)
        page.wait_for_timeout(1000)
        page.keyboard.press('Enter')
        page.wait_for_timeout(5000)
        new_storage_state = context.storage_state()
        with open('new_auth.json', 'w') as f:
            json.dump(new_storage_state, f)

    page.goto("https://www.bettilt.com/en/game/aviator-spribe/real")
    page.wait_for_timeout(10000)
    print('0')
    # Entrar no iframe do jogo
    aguardar(page, '//*[@id="root"]/div[1]/div[3]/div/div/div/div[2]/div/div/iframe')
    iframe = page.wait_for_selector('//*[@id="root"]/div[1]/div[3]/div/div/div/div[2]/div/div/iframe')
    page = iframe.content_frame()
    print('1')

    # Aguardar e entrar no iframe do jogo novamente
    aguardar(page, '//*[@id="gameFrame"]')
    iframe = page.wait_for_selector('//*[@id="gameFrame"]')
    page = iframe.content_frame()
    print('2')
    # Aguardar e puxar o histórico
    aguardar(page, '//html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]')
    xpath_historico = '//html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div'
    historico_antigo = page.locator(xpath_historico).text_content()
    while True:
        historico_atual = page.locator(xpath_historico).text_content()
        if historico_atual != historico_antigo:
            historico_antigo = historico_atual
            historico_lista = [float(valor.strip('x')) for valor in historico_atual.split()]
            print(historico_lista)


with sync_playwright() as playwright:
    run(playwright)


