from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import csv
import requests
import os
from urllib.parse import urljoin

URL = "https://www.carflix.com.br/comprar"
OUT_CSV = "carflix_listings.csv"
IMAGES_DIR = "car_images"
SCROLL_PAUSE = 2.0  
MAX_SCROLL_ATTEMPTS = 30

def create_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
   
    service = ChromeService() 
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def setup_images_directory():
    """Cria diretório para salvar imagens"""
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        print(f"Diretório {IMAGES_DIR} criado")

def scroll_to_load_all(driver):
    print("Rolando página para carregar todos os anúncios...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0
    
    while attempts < MAX_SCROLL_ATTEMPTS:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        
        
        driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(0.5)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(f"Altura da página: {last_height} -> {new_height}")
        
        if new_height == last_height:
            attempts += 1
            print(f"Mesma altura ({attempts}/{MAX_SCROLL_ATTEMPTS})")
        else:
            attempts = 0
            last_height = new_height
    
    print("Rolagem concluída")

def extract_image_url(element, driver):
    """Extrai URL da imagem do anúncio com múltiplas estratégias"""
    image_selectors = [
        "img",
        ".card-img",
        ".vehicle-image",
        ".car-image", 
        ".listing-image",
        ".product-image",
        "[data-testid*='image']",
        ".MuiCardMedia-root",  # Material-UI
        ".image",
        "picture img",
        ".thumbnail",
        ".photo"
    ]
    
    for selector in image_selectors:
        try:
            img_elements = element.find_elements(By.CSS_SELECTOR, selector)
            for img in img_elements:
                try:
                   
                    src = img.get_attribute("src")
                    if src and is_valid_image_url(src):
                        return src
                    
                    
                    srcset = img.get_attribute("srcset")
                    if srcset:
                  
                        first_src = srcset.split(',')[0].split(' ')[0]
                        if first_src and is_valid_image_url(first_src):
                            return first_src
                    
                    
                    data_src = img.get_attribute("data-src")
                    if data_src and is_valid_image_url(data_src):
                        return data_src
                        
                   
                    for attr in ["data-lazy", "data-original", "data-srcset"]:
                        data_attr = img.get_attribute(attr)
                        if data_attr and is_valid_image_url(data_attr):
                            return data_attr.split(' ')[0] if ' ' in data_attr else data_attr
                            
                except StaleElementReferenceException:
                    continue
        except:
            continue
    
    
    try:
        elements_with_bg = element.find_elements(By.CSS_SELECTOR, "[style*='background-image']")
        for elem in elements_with_bg:
            style = elem.get_attribute("style")
            if "url(" in style:
                import re
                url_match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
                if url_match:
                    bg_url = url_match.group(1)
                    if is_valid_image_url(bg_url):
                        return bg_url
    except:
        pass
    
    return None

def is_valid_image_url(url):
    """Verifica se a URL é uma imagem válida"""
    if not url or url.strip() == "":
        return False
    
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif']
    valid_patterns = ['/images/', '/img/', 'cloudfront.net', 'storage.googleapis.com']
    
    url_lower = url.lower()
    
   
    if any(ext in url_lower for ext in valid_extensions):
        return True
    
 
    if any(pattern in url for pattern in valid_patterns):
        return True
    
   
    if url_lower.startswith('data:image'):
        return True
    
    return False

def download_image(image_url, listing_index, title):
    """Faz download da imagem e retorna o nome do arquivo"""
    if not image_url:
        return None
    
    try:
      
        safe_title = "".join(c for c in title[:50] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')
        
        extension = '.jpg' 
        if '.png' in image_url.lower():
            extension = '.png'
        elif '.webp' in image_url.lower():
            extension = '.webp'
        elif '.gif' in image_url.lower():
            extension = '.gif'
        
        filename = f"{listing_index:03d}_{safe_title}{extension}"
        filepath = os.path.join(IMAGES_DIR, filename)
        
       
        if image_url.startswith('data:image'):
            import base64
            
            base64_data = image_url.split(',')[1]
            image_data = base64.b64decode(base64_data)
            with open(filepath, 'wb') as f:
                f.write(image_data)
        else:
            
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
        
        print(f"     Imagem salva: {filename}")
        return filename
        
    except Exception as e:
        print(f"     Erro ao baixar imagem: {e}")
        return None

def extract_link(element):
    """Extrai link do anúncio com múltiplas estratégias"""
    link_patterns = ["/comprar/", "/veiculo/", "/carro/", "/vehicle/"]
    
    
    try:
        links = element.find_elements(By.TAG_NAME, "a")
        for link in links:
            try:
                href = link.get_attribute("href")
                if href and any(pattern in href for pattern in link_patterns):
                    return href
            except StaleElementReferenceException:
                continue
    except:
        pass
    
    
    try:
        onclick_elements = element.find_elements(By.CSS_SELECTOR, "[onclick*='/comprar/'], [onclick*='/veiculo/'], [onclick*='/carro/']")
        for elem in onclick_elements:
            onclick = elem.get_attribute("onclick")
            for pattern in link_patterns:
                if pattern in onclick:
                    
                    import re
                    url_match = re.search(r"'(https?://[^']+)'", onclick)
                    if url_match:
                        return url_match.group(1)
    except:
        pass
    
    
    try:
        if element.tag_name.lower() == 'a':
            href = element.get_attribute("href")
            if href and any(pattern in href for pattern in link_patterns):
                return href
    except:
        pass
    
   
    try:
        link_selectors = [
            "a[href*='/comprar/']",
            "a[href*='/veiculo/']", 
            "a[href*='/carro/']",
            ".card-link",
            ".vehicle-link",
            ".listing-link"
        ]
        for selector in link_selectors:
            try:
                link_elem = element.find_element(By.CSS_SELECTOR, selector)
                href = link_elem.get_attribute("href")
                if href:
                    return href
            except:
                continue
    except:
        pass
    
    return None

def parse_listing(element, index, download_images=False):
    """Extrai dados de um anúncio individual"""
    data = {
        "title": None, 
        "price": None, 
        "details": None, 
        "link": None,
        "image_url": None,
        "image_file": None,
        "year": None,
        "mileage": None,
        "location": None
    }
    
    try:
       
        title_selectors = [
            ".card-title", ".title", "h3", ".vehicle-title",
            ".car-title", "[data-testid*='title']", "h2", "h4"
        ]
        for selector in title_selectors:
            try:
                title_elem = element.find_element(By.CSS_SELECTOR, selector)
                data["title"] = title_elem.text.strip()
                if data["title"]:
                    break
            except:
                continue
        
       
        price_selectors = [
            ".price", ".card-price", ".vehicle-price", ".valor",
            ".car-price", "[data-testid*='price']", ".preco"
        ]
        for selector in price_selectors:
            try:
                price_elem = element.find_element(By.CSS_SELECTOR, selector)
                data["price"] = price_elem.text.strip()
                if data["price"]:
                    break
            except:
                continue
        
        
        detail_selectors = [
            ".card-subtitle", ".details", ".vehicle-info", ".info",
            ".car-details", ".specs", "[data-testid*='details']"
        ]
        for selector in detail_selectors:
            try:
                detail_elem = element.find_element(By.CSS_SELECTOR, selector)
                data["details"] = detail_elem.text.strip()
                if data["details"]:
                    break
            except:
                continue
        
       
        data["link"] = extract_link(element)
        
       
        data["image_url"] = extract_image_url(element, driver)
        
       
        if download_images and data["image_url"] and data["title"]:
            data["image_file"] = download_image(data["image_url"], index, data["title"] or f"carro_{index}")
        
      
        if data["details"]:
            details_text = data["details"]
           
            import re
            year_match = re.search(r'\b(19|20)\d{2}\b', details_text)
            if year_match:
                data["year"] = year_match.group()
            
            
            km_match = re.search(r'(\d{1,3}(?:\.\d{3})*)\s*km', details_text, re.IGNORECASE)
            if km_match:
                data["mileage"] = km_match.group(1)
            
           
            locations = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'DF', 'ES', 'GO']
            for loc in locations:
                if loc in details_text:
                    data["location"] = loc
                    break

    except Exception as e:
        print(f"Erro no parse_listing: {e}")
    
    return data

def find_listing_elements(driver):
    """Encontra elementos de anúncio usando múltiplas estratégias"""
    print("Procurando elementos de anúncio...")
    
    listing_selectors = [
       
        "[data-testid*='vehicle']",
        ".vehicle-card",
        ".car-card", 
        ".listing-card",
        ".product-item",
       
        ".card",
        "article",
        "a[href*='/comprar/']",
        "a[href*='/veiculo/']",
        "a[href*='/carro/']",
       
        ".MuiCard-root", 
        ".card-body",
        ".listing-item"
    ]
    
    all_listings = []
    
    for selector in listing_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"Selector '{selector}': {len(elements)} elementos")
               
                filtered_elements = []
                for elem in elements:
                    try:
                        text = elem.text.strip()
                        
                        if len(text) > 20 and any(keyword in text.lower() for keyword in 
                                                 ['r$', 'km', 'ano', 'carro', 'veículo', 'automóvel']):
                            filtered_elements.append(elem)
                    except:
                        continue
                
                if filtered_elements:
                    print(f"  -> {len(filtered_elements)} parecem ser anúncios")
                    all_listings.extend(filtered_elements)
                    
        except Exception as e:
            print(f"Erro com selector {selector}: {e}")
    
  
    unique_listings = []
    seen_elements = set()
    
    for listing in all_listings:
        try:
            element_id = listing.id
            if element_id not in seen_elements:
                seen_elements.add(element_id)
                unique_listings.append(listing)
        except:
            unique_listings.append(listing)
    
    print(f"Total de anúncios únicos encontrados: {len(unique_listings)}")
    return unique_listings

def scrape_carflix(driver, download_images=True):
    print(f"Acessando {URL}")
    driver.get(URL)
    

    if download_images:
        setup_images_directory()
    
   
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Página carregada")
    except TimeoutException:
        print("Timeout ao carregar página")
        return []
    
    
    time.sleep(3)
    
    
    scroll_to_load_all(driver)
    
   
    listing_elements = find_listing_elements(driver)
    
    if not listing_elements:
        print("Nenhum anúncio encontrado. Tentando estratégia alternativa...")
       
        all_links = driver.find_elements(By.TAG_NAME, "a")
        car_links = []
        for link in all_links:
            try:
                href = link.get_attribute("href")
                if href and any(pattern in href for pattern in ["/comprar/", "/veiculo/", "/carro/"]):
                    car_links.append(link)
            except:
                continue
        print(f"Encontrados {len(car_links)} links de carros")
        listing_elements = car_links
    
    
    results = []
    seen_links = set()
    
    print(f"Processando {len(listing_elements)} anúncios...")
    for i, element in enumerate(listing_elements):
        try:
            print(f"Processando anúncio {i+1}/{len(listing_elements)}")
            data = parse_listing(element, i, download_images)
            
           
            if data.get("title") or data.get("price") or data.get("link"):
                link = data.get("link")
                if link and link not in seen_links:
                    seen_links.add(link)
                    results.append(data)
                    print(f"  ✓ {data.get('title', 'Sem título')} - {data.get('price', 'Sem preço')}")
                    if data.get("image_url"):
                        print(f"     Imagem encontrada")
                    else:
                        print(f"     Sem imagem")
                elif not link:
                    results.append(data)
                    print(f"  ? {data.get('title', 'Sem título')} - SEM LINK")
            else:
                print(f"   Anúncio inválido ou incompleto")
                
        except Exception as e:
            print(f"Erro ao processar anúncio {i+1}: {e}")
    
    print(f"Extraídos {len(results)} anúncios válidos")
    return results

def save_csv(rows, filename=OUT_CSV):
    if not rows:
        print("Nenhum dado para salvar")
        return
    
    keys = ["title", "price", "details", "link", "image_url", "image_file", "year", "mileage", "location"]
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in keys})
    print(f"Salvo {len(rows)} anúncios em {filename}")

def print_summary(data):
    """Imprime um resumo dos dados coletados"""
    if not data:
        print("Nenhum dado coletado")
        return
    
    print("\n" + "="*50)
    print("RESUMO DA COLETA")
    print("="*50)
    print(f"Total de anúncios: {len(data)}")
    
    with_links = sum(1 for item in data if item.get('link'))
    with_images = sum(1 for item in data if item.get('image_url'))
    downloaded_images = sum(1 for item in data if item.get('image_file'))
    
    print(f"Anúncios com links: {with_links}")
    print(f"Anúncios com imagens: {with_images}")
    print(f"Imagens baixadas: {downloaded_images}")
    
    print("\nPrimeiros 5 anúncios:")
    for i, item in enumerate(data[:5]):
        print(f"{i+1}. {item.get('title', 'Sem título')}")
        print(f"   Preço: {item.get('price', 'Sem preço')}")
        print(f"   Link: {item.get('link', 'Sem link')}")
        print(f"   Imagem: {item.get('image_url', 'Sem imagem')}")
        if item.get('image_file'):
            print(f"   Arquivo: {item.get('image_file')}")
        print()

if __name__ == "__main__":
    driver = create_driver(headless=False)  
    try:
        data = scrape_carflix(driver, download_images=True)
        print_summary(data)
        save_csv(data)
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        driver.quit()