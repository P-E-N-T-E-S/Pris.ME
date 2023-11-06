from selenium_setup import setup_selenium, finalizar_selenium
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time

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
        