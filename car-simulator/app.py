from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui_123'

# Caminho para o CSV
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'carflix_listings.csv')
IMAGES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'car_images')

def load_cars():
    """Carrega os dados do CSV"""
    try:
        df = pd.read_csv(CSV_PATH, encoding='utf-8')
        # Limpar dados vazios
        df = df.dropna(subset=['title'])
        return df
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return pd.DataFrame()

def extract_brand(title):
    """Extrai a marca do título do carro"""
    brands = ['VOLKSWAGEN', 'FORD', 'CHEVROLET', 'FIAT', 'HONDA', 'TOYOTA', 
              'HYUNDAI', 'JEEP', 'RENAULT', 'NISSAN', 'KIA', 'CITROEN', 
              'PEUGEOT', 'MERCEDES-BENZ', 'BMW', 'AUDI', 'VOLVO', 'SUBARU',
              'JAC', 'CAOA CHERY', 'GWM', 'HAVAL']
    
    title_upper = title.upper()
    for brand in brands:
        if brand in title_upper:
            return brand
    
    # Tentar extrair a primeira palavra como marca
    first_word = title.split()[0].upper()
    return first_word

def classify_car_type(title: str) -> str:
    """
    Classifica o tipo de carro com base no título e, se possível, na marca.
    Suporta principais marcas e modelos populares do mercado.
    """

    if not isinstance(title, str) or title.strip() == "":
        return "Desconhecido"

    title_upper = title.upper()

    # 🔹 SUV
    if any(word in title_upper for word in [
        'TIGUAN', 'SPORTAGE', 'TUCSON', 'COMPASS', 'TRACKER', 'ECOSPORT',
        'HAVAL', 'TIGGO', 'CRETA', 'HR-V', 'DUSTER', 'RENEGADE',
        'KICKS', 'CAPTUR', 'COROLLA CROSS', 'PULSE', '2008', '3008', '5008',
        'XV', 'OUTLANDER', 'EQUINOX'
    ]):
        return 'SUV'

    # 🔹 Hatch
    elif any(word in title_upper for word in [
        'GOL', 'KA', 'CLIO', 'FIT', 'FOX', 'UNO', 'ONIX', 'MARCH',
        'HB20', 'SANDERO', '208', 'C3', 'FIESTA', 'POLO', 'YARIS HATCH'
    ]):
        return 'Hatch'

    # 🔹 Sedan
    elif any(word in title_upper for word in [
        'CITY', 'FUSION', 'VIRTUS', 'JETTA', 'COROLLA', 'CIVIC', 'SENTRA',
        'VERSA', 'ARGO SEDAN', 'HB20S', 'LOGAN', 'SIENA', 'A3 SEDAN',
        'C4 LOUNGE', 'PASSAT'
    ]):
        return 'Sedan'

    # 🔹 Picape
    elif any(word in title_upper for word in [
        'STRADA', 'TORO', 'HILUX', 'AMAROK', 'FRONTIER', 'S10', 'RANGER',
        'MAVERICK', 'SAVEIRO', 'MONTANA', 'L200', 'NAVARA'
    ]):
        return 'Picape'

    # 🔹 Esportivo
    elif any(word in title_upper for word in [
        'MUSTANG', 'CAMARO', 'A45', 'RS', 'M3', 'M4', 'Z4', '718', 'BOXSTER',
        'CAYMAN', '911', 'TT', 'A35', 'BRZ'
    ]):
        return 'Esportivo'

    # 🔹 Elétrico / Híbrido
    elif any(word in title_upper for word in [
        'E-TRON', 'iX', 'i3', 'LEAF', 'BOLT', 'COROLLA HYBRID', 'PRIUS',
        'BYD', 'TESLA', 'ID.4', 'HAVAL H6', 'TIGGO 8 PRO', 'VOLVO XC40 RECHARGE'
    ]):
        return 'Elétrico / Híbrido'

    # 🔹 Off-road / Luxo (casos especiais)
    elif any(word in title_upper for word in [
        'GRAND CHEROKEE', 'DISCOVERY', 'DEFENDER', 'GLC', 'GLE', 'X5', 'X6'
    ]):
        return 'SUV Luxo'

    # 🔹 Fallback por marca (caso título não contenha modelo específico)
    elif any(word in title_upper for word in [
        'JEEP', 'HAVAL', 'CAOA CHERY', 'GWM', 'VOLVO'
    ]):
        return 'SUV'

    elif any(word in title_upper for word in [
        'FIAT', 'CHEVROLET', 'FORD', 'VOLKSWAGEN', 'RENAULT', 'PEUGEOT', 'CITROEN'
    ]):
        return 'Hatch'

    elif any(word in title_upper for word in [
        'TOYOTA', 'HONDA', 'NISSAN'
    ]):
        return 'Sedan'

    # 🔹 Default
    return 'Hatch'


def classify_transmission(title):
    """Classifica o tipo de câmbio"""
    title_upper = title.upper()
    if 'AUTOMÁTICO' in title_upper or 'AUTOMATICO' in title_upper:
        return 'Automático'
    elif 'MANUAL' in title_upper:
        return 'Manual'
    return 'Automático'  # Default

def classify_motor_type(title):
    """Classifica o tipo de motor"""
    title_upper = title.upper()
    if 'HYBRID' in title_upper or 'HIBRIDO' in title_upper or 'HEV' in title_upper or 'PHEV' in title_upper:
        return 'Híbrido'
    elif 'ELECTRIC' in title_upper or 'ELÉTRICO' in title_upper or 'ELETRICO' in title_upper or 'EV' in title_upper:
        return 'Elétrico'
    else:
        return 'Combustão'

def parse_price(price_str):
    """Converte string de preço para float"""
    if pd.isna(price_str) or price_str == '':
        return 0
    # Remove "R$", pontos e substitui vírgula por ponto
    price_clean = price_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(price_clean)
    except:
        return 0

def calculate_installment(price, months, interest_rate=0.012):
    """Calcula o valor da parcela com juros compostos"""
    if months <= 0:
        return 0
    # Fórmula: parcela = preço * [(1 + i)^n * i] / [(1 + i)^n - 1]
    factor = (1 + interest_rate) ** months
    installment = price * (factor * interest_rate) / (factor - 1)
    return installment

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    """Página sobre"""
    return render_template('sobre.html')

@app.route('/simulacao', methods=['GET', 'POST'])
def simulacao():
    """Página de simulação com formulário dinâmico"""
    if request.method == 'POST':
        # Salvar dados na sessão
        session['possui_carro'] = request.form.get('possui_carro')
        session['carro_quitado'] = request.form.get('carro_quitado')
        session['valor_restante'] = request.form.get('valor_restante', '0')
        session['modelo_atual'] = request.form.get('modelo_atual', '')
        session['forma_pagamento'] = request.form.get('forma_pagamento')
        session['valor_parcela'] = request.form.get('valor_parcela', '0')
        session['num_parcelas'] = request.form.get('num_parcelas', '0')
        session['valor_vista'] = request.form.get('valor_vista', '0')
        session['tipo_carro'] = request.form.get('tipo_carro')
        session['prioridade'] = request.form.get('prioridade')
        session['marca_preferida'] = request.form.get('marca_preferida', '')
        session['cambio'] = request.form.get('cambio')
        session['tipo_motor'] = request.form.get('tipo_motor')
        
        return redirect(url_for('resultado'))
    
    # Carregar marcas disponíveis do CSV
    df = load_cars()
    marcas = set()
    for title in df['title']:
        marca = extract_brand(str(title))
        if marca:
            marcas.add(marca)
    marcas = sorted(list(marcas))
    
    return render_template('simulacao.html', marcas=marcas)

@app.route('/resultado')
def resultado():
    """Página de resultados com os 3 melhores carros"""
    # Recuperar dados da sessão
    possui_carro = session.get('possui_carro')
    forma_pagamento = session.get('forma_pagamento')
    tipo_carro = session.get('tipo_carro')
    marca_preferida = session.get('marca_preferida', '')
    cambio = session.get('cambio')
    tipo_motor = session.get('tipo_motor')
    
    # Carregar dados do CSV
    df = load_cars()
    
    if df.empty:
        return render_template('resultado.html', carros=[], erro="Erro ao carregar dados do CSV")
    
    # Adicionar colunas de classificação
    df['brand'] = df['title'].apply(extract_brand)
    df['car_type'] = df['title'].apply(classify_car_type)
    df['transmission'] = df['title'].apply(classify_transmission)
    df['motor_type'] = df['title'].apply(classify_motor_type)
    df['price_float'] = df['price'].apply(parse_price)
    
    # Filtrar carros com preço válido
    df = df[df['price_float'] > 0]
    
    # Aplicar filtros baseados nas preferências
    filtered_df = df.copy()
    
    # Filtro por tipo de carro
    if tipo_carro:
        filtered_df = filtered_df[filtered_df['car_type'] == tipo_carro]
    
    # Filtro por marca
    if marca_preferida and marca_preferida != 'Qualquer':
        filtered_df = filtered_df[filtered_df['brand'] == marca_preferida]
    
    # Filtro por câmbio
    if cambio:
        filtered_df = filtered_df[filtered_df['transmission'] == cambio]
    
    # Filtro por tipo de motor
    if tipo_motor:
        filtered_df = filtered_df[filtered_df['motor_type'] == tipo_motor]
    
    # Filtro por orçamento
    if forma_pagamento == 'vista':
        valor_vista = float(session.get('valor_vista', 0))
        if valor_vista > 0:
            filtered_df = filtered_df[filtered_df['price_float'] <= valor_vista]
    elif forma_pagamento == 'financiado':
        valor_parcela = float(session.get('valor_parcela', 0))
        num_parcelas = int(session.get('num_parcelas', 0))
        if valor_parcela > 0 and num_parcelas > 0:
            # Calcular preço máximo baseado na parcela
            max_price = valor_parcela * num_parcelas / 1.5  # Aproximação considerando juros
            filtered_df = filtered_df[filtered_df['price_float'] <= max_price]
    
    # Se não houver resultados, relaxar os filtros
    if filtered_df.empty:
        filtered_df = df[df['car_type'] == tipo_carro] if tipo_carro else df
    
    # Ordenar por melhor custo-benefício (preço)
    filtered_df = filtered_df.sort_values('price_float')
    
    # Selecionar os 3 melhores
    top_3 = filtered_df.head(3)
    
    # Preparar dados para exibição
    carros = []
    for _, row in top_3.iterrows():
        price = row['price_float']
        
        # Calcular parcela se for financiamento
        parcela = None
        if forma_pagamento == 'financiado':
            num_parcelas = int(session.get('num_parcelas', 48))
            parcela = calculate_installment(price, num_parcelas)
        
        # Usar imagem local se disponível
        image_file = row.get('image_file', '')
        if image_file and os.path.exists(os.path.join(IMAGES_PATH, image_file)):
            image_url = f'/static/car_images/{image_file}'
        else:
            image_url = row.get('image_url', '')
        
        carro = {
            'title': row['title'],
            'price': row['price'],
            'price_float': price,
            'link': row.get('link', '#'),
            'image_url': image_url,
            'parcela': parcela,
            'brand': row['brand'],
            'car_type': row['car_type'],
            'transmission': row['transmission'],
            'motor_type': row['motor_type']
        }
        carros.append(carro)
    
    # Dados da simulação
    simulacao_data = {
        'possui_carro': possui_carro,
        'forma_pagamento': forma_pagamento,
        'tipo_carro': tipo_carro,
        'marca_preferida': marca_preferida,
        'cambio': cambio,
        'tipo_motor': tipo_motor,
        'num_parcelas': session.get('num_parcelas', 0),
        'data_hora': datetime.now().strftime('%d/%m/%Y às %H:%M')
    }
    
    return render_template('resultado.html', carros=carros, simulacao=simulacao_data, erro=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
