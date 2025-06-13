from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar Selenium con Chrome
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Opcional: Ejecutar en modo invisible
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Ir a la página de la factura
url = "https://ofv.edenorte.com.do/"
driver.get(url)

# Esperar que la página cargue (ajustar según sea necesario)
time.sleep(5)

# Si hay login, completar credenciales
try:
    usuario = driver.find_element(By.NAME, "login-form[login]")  # Ajustar según el HTML real
    contraseña = driver.find_element(By.NAME, "login-form[password]")  # Ajustar según el HTML real
    usuario.send_keys("enmanuelbcf@gmail.com")
    contraseña.send_keys("Prueba01*")
    contraseña.send_keys(Keys.RETURN)
    time.sleep(5)  # Esperar el login
except:
    print("No se requirió login o los campos son diferentes.")

# Descargar el PDF (si hay un botón de descarga)
try:
    boton_descarga = driver.find_element(By.XPATH, "//a[contains(@href, '.pdf')]")  # Ajustar XPATH según el sitio
    enlace_pdf = boton_descarga.get_attribute("href")
    print(f"Enlace del PDF: {enlace_pdf}")
except:
    print("No se encontró el botón de descarga.")

# Cerrar el navegador
driver.quit()
