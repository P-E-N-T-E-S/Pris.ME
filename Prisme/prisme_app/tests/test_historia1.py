from selenium_setup import setup_selenium, finalizar_selenium
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

intervalo_do_teste = 5

class Historia1(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        setup_selenium()
    
    @classmethod
    def tearDownClass(cls):
        finalizar_selenium()


    def test_000_setup(self):
        driver = setup_selenium()
        usuario = driver.find_element(by=By.ID, value="usuario")
        senha = driver.find_element(by=By.ID, value="senha")
        botao = driver.find_element(by=By.ID, value="Logar")

        usuario.send_keys("TestesM")
        senha.send_keys("Teste12345")
        botao.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/cadastrar_ong")

        nome_ong = driver.find_element(by=By.ID, value="nome_ong")
        cnpj = driver.find_element(by=By.ID, value="CNPJ")
        data = driver.find_element(by=By.ID, value="criacao")
        email = driver.find_element(by=By.ID, value="email_ong")
        descricao = driver.find_element(by=By.ID, value="descricao")
        area = driver.find_element(by=By.ID, value="areaAtuacao")
        area = Select(area)
        CEP = driver.find_element(by=By.ID, value="CEP")
        voluntarios = driver.find_element(by=By.ID, value="numeroDeVoluntarios")
        botao = driver.find_element(by=By.ID, value="cadastrar")

        nome_ong.send_keys("Teste1")
        cnpj.send_keys("04.712.500/0001-07")
        data.send_keys("29082003")
        email.send_keys("teste1@ong.com")
        descricao.send_keys("definitivamente é uma ong")
        area.select_by_visible_text("Outro")
        CEP.send_keys("52071-321")
        voluntarios.send_keys("4")
        botao.send_keys(Keys.ENTER)
        driver.get("http://127.0.0.1:8000/logout")

        driver.get("http://127.0.0.1:8000/")
        usuario = driver.find_element(by=By.ID, value="usuario")
        senha = driver.find_element(by=By.ID, value="senha")
        botao = driver.find_element(by=By.ID, value="Logar")

        usuario.send_keys("teste1@ong.com")
        senha.send_keys("senha_inicial")
        botao.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/add_projeto")
        nome = driver.find_element(by=By.ID, value="nome_projeto")
        descricao = driver.find_element(by=By.ID, value="descricao")
        metodologia = driver.find_element(by=By.ID, value="metodologia")
        publico = driver.find_element(by=By.ID, value="publico")
        data = driver.find_element(by=By.ID, value="criacao")
        botao = driver.find_element(by=By.ID, value="cadastrar")

        nome.send_keys("projeto_teste")
        descricao.send_keys("definitivamente é um projeto")
        metodologia.send_keys("cientifica")
        publico.send_keys("todos")
        data.send_keys("29082003")
        botao.send_keys(Keys.ENTER)
        driver.get("http://127.0.0.1:8000/logout")
        self.assertTrue(True)

    def test_001_cenario1(self):
        driver = setup_selenium()
        driver.get("http://127.0.0.1:8000/")
        usuario = driver.find_element(by=By.ID, value="usuario")
        senha = driver.find_element(by=By.ID, value="senha")
        botao = driver.find_element(by=By.ID, value="Logar")

        usuario.send_keys("teste1@ong.com")
        senha.send_keys("senha_inicial")
        botao.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/visualizar_projetos")
        projeto_id = driver.find_element(by=By.TAG_NAME, value="h2").get_attribute("id")
        driver.get(f"http://127.0.0.1:8000/add_dados/{projeto_id}/")

        titulo = driver.find_element(by=By.ID, value="titulo")
        descricao = driver.find_element(by=By.ID, value="descricao")
        eixoX = driver.find_element(by=By.ID, value="tipo1")
        eixoX = Select(eixoX)
        eixoY = driver.find_element(by=By.ID, value="tipo2")
        eixoY = Select(eixoY)
        botao = driver.find_element(by=By.ID, value="cadastrar")

        titulo.send_keys("dado_impacto_teste1")
        descricao.send_keys("ligeiramente é um dado de impacto")
        eixoX.select_by_visible_text("Pessoas Impactadas")
        eixoY.select_by_visible_text("Tempo")
        botao.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/visualizar_projetos")

        try:
            driver.find_element(by=By.ID, value="dado_impacto_teste1")
        except:
            validar = False
        else:
            validar = True
        self.assertTrue(validar)

    def test_002_cenario2(self):
        driver = setup_selenium()
        driver.get("http://127.0.0.1:8000/")
        usuario = driver.find_element(by=By.ID, value="usuario")
        senha = driver.find_element(by=By.ID, value="senha")
        botao = driver.find_element(by=By.ID, value="Logar")

        usuario.send_keys("teste1@ong.com")
        senha.send_keys("senha_inicial")
        botao.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/visualizar_projetos")
        projeto_id = driver.find_element(by=By.TAG_NAME, value="h2").get_attribute("id")
        driver.get(f"http://127.0.0.1:8000/add_dados/{projeto_id}/")

        botao = driver.find_element(by=By.ID, value="cadastrar")

        botao.send_keys(Keys.ENTER)

        self.assertEquals(
            driver.title, "Pris.ME Adicionar Dados"
        )

    def test_003_cenario3(self):
        driver = setup_selenium()

        driver.get("http://127.0.0.1:8000/logout")

        driver.get("http://127.0.0.1:8000/visualizar_projetos")

        self.assertEquals(
            driver.title, "Pris.ME"
        )

    def test_004_cenario4(self):
        driver = setup_selenium()
        driver.get("http://127.0.0.1:8000/")
        usuario = driver.find_element(by=By.ID, value="usuario")
        senha = driver.find_element(by=By.ID, value="senha")
        botao = driver.find_element(by=By.ID, value="Logar")

        usuario.send_keys("teste1@ong.com")
        senha.send_keys("senha_inicial")
        botao.send_keys(Keys.ENTER)

        driver.get("http://127.0.0.1:8000/visualizar_projetos")

        projeto_id = driver.find_element(by=By.TAG_NAME, value="h2").get_attribute("id")
        driver.get(f"http://127.0.0.1:8000/editar_dado/{projeto_id}/")

        titulo = driver.find_element(by=By.ID, value="titulo")
        botao = driver.find_element(by=By.ID, value="editar")
        titulo.send_keys(Keys.CONTROL + 'a')
        titulo.send_keys("teste nome alterado")
        botao.send_keys(Keys.ENTER)

        try:
            driver.find_element(by=By.ID, value="teste nome alterado")
        except:
            validar = False
        else:
            validar = True
        self.assertTrue(validar)
