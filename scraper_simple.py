# scraper_windows_simple.py - SUPER SIMPLE
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime
import csv

print("SCRAPING")
print("---------------------------")


def extraer_hoteles_pagina(driver, datos_hoteles):
    # H1 (nombres de hoteles)
    h1_elems = driver.find_elements(By.TAG_NAME, "h1")
    h1_textos = [h.text.strip() for h in h1_elems if h.text.strip()]

    # Enlaces con la descripción
    enlaces = driver.find_elements(By.CSS_SELECTOR, "div.subtitular p a")
    # Bloques de categoría (estrellas)
    categorias = driver.find_elements(By.CSS_SELECTOR, "div.categoria")
    # Imágenes
    imagenes = driver.find_elements(By.CSS_SELECTOR, "div.imagenNoticia a img")

    n = min(len(h1_textos), len(enlaces), len(categorias), len(imagenes))
    print(f"Hoteles encontrados en esta página: {n}")

    for i in range(n):
        nombre = h1_textos[i]

        a_desc = enlaces[i]
        descripcion = a_desc.text.strip()
        enlace = a_desc.get_attribute("href")

        pueblo = "Málaga"

        estrellas = len(
            categorias[i].find_elements(By.CSS_SELECTOR, "span.icon-star")
        )

        img = imagenes[i].get_attribute("src")

        datos_hoteles.append({
            "nombre": nombre,
            "enlace": enlace,
            "pueblo": pueblo,
            "estrellas": estrellas,
            "imagen": img,
            "descripcion": descripcion
        })


try:
    # 1. Iniciar Chrome
    print("Iniciando Chrome...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # 2. Ir a la página
    url = "https://visita.malaga.eu/es/planifica/donde-dormir/hoteles"
    print(f"Accediendo a: {url}")
    driver.get(url)

    # 2.1 Aceptar cookies
    wait = WebDriverWait(driver, 10)
    try:
        boton_cookies = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input#cookie-acepto-todas")
            )
        )
        boton_cookies.click()
        print("Cookies aceptadas (Aceptar todas)")
    except Exception as e:
        print("No se pudo hacer clic en el botón de cookies:", e)

    # 3. Esperar
    print("Esperando 10 segundos...")
    time.sleep(10)
    
    # 4. Obtener información básica (solo primera página)
    print("\nINFORMACION OBTENIDA:")
    print(f"- Titulo: {driver.title}")
    print(f"- URL: {driver.current_url}")
    
    h1_elems = driver.find_elements(By.TAG_NAME, "h1")
    h1_textos = [h.text.strip() for h in h1_elems if h.text.strip()]
    print(f"- H1 encontrados: {len(h1_textos)}")
    
    # 5. Preparar directorios de salida
    base_dir = os.path.join(os.getcwd(), "salidas")
    csv_dir = os.path.join(base_dir, "csv")

    os.makedirs(csv_dir, exist_ok=True)
    
    # Timestamp
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 6. Scrapeo con paginación
    datos_hoteles = []

    while True:
        print("Scrapeando página de resultados...")
        extraer_hoteles_pagina(driver, datos_hoteles)

        # Buscar botón "next"
        try:
            next_li = driver.find_element(
                By.CSS_SELECTOR,
                "div.paginationv2 li.next"
            )
        except:
            print("No se encontró bloque 'next'. Fin de paginación.")
            break

        # si está desactivado (por ejemplo 'next off'), paramos
        clase_next = next_li.get_attribute("class") or ""
        if "off" in clase_next:
            print("Botón 'next' desactivado. Fin de paginación.")
            break

        try:
            next_link = next_li.find_element(By.TAG_NAME, "a")
        except:
            print("No hay enlace en 'next'. Fin de paginación.")
            break

        driver.execute_script("arguments[0].click();", next_link)
        print("Pasando a la siguiente página...")
        time.sleep(5)

    # Guardar CSV con todas las páginas
    csv_path = os.path.join(csv_dir, f"hoteles_{ts}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as fcsv:
        campos = ["nombre", "enlace", "pueblo", "estrellas", "imagen", "descripcion"]
        writer = csv.DictWriter(fcsv, fieldnames=campos)
        writer.writeheader()
        writer.writerows(datos_hoteles)

    print(f"- {csv_path} (datos de hoteles en CSV con todas las páginas)")

finally:
    try:
        driver.quit()
        print("\nChrome cerrado.")
    except:
        pass
