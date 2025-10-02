# app.py
from flask import Flask, render_template, request, jsonify
# Importa as funções do banco de dados do arquivo config.py
from config import conexao_banco, criar_banco_se_nao_existir 
import mysql.connector
import math # Importa a biblioteca matemática para cálculos financeiros

# --- Configuração da Aplicação ---
app = Flask(__name__)

# --- Rotas de Páginas (Views) ---

@app.route('/')
def index():
    """Renderiza a página inicial (Home), que deve ser o ponto de entrada."""
    # Renderiza o template que usa o layout.html
    return render_template('index.html')

@app.route('/questionnaire')
def questionnaire_page():
    """Renderiza a página do questionário de simulação."""
    return render_template('questionnaire.html')

@app.route('/results')
def results_page():
    """Renderiza a página de resultados (idealmente com dados já carregados)."""
    return render_template('results.html')

@app.route('/about')
def about_page():
    """Renderiza a página 'Sobre Nós'."""
    return render_template('about.html')


# --- Rotas de API ---

@app.route('/api/carros')
def api_carros():
    """
    API para buscar dados agregados de carros (fabricante, preço por ano/combustível).
    Retorna dados para gráficos no frontend.
    """
    conn = conexao_banco()
    if not conn:
        return jsonify({'error': 'Erro de conexão com o banco de dados. Verifique o config.py.'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # 1. Carros por Fabricante
        cursor.execute('''
            SELECT f.nome AS fabricante, COUNT(*) AS quantidade
            FROM Carros c
            JOIN Fabricante f ON c.id_fabricante = f.id_fabricante
            GROUP BY f.nome
        ''')
        carros_por_fabricante = cursor.fetchall()
        
        # 2. Preço Médio por Ano
        cursor.execute('''
            SELECT ano_modelo, AVG(preco) AS media_preco
            FROM Carros
            GROUP BY ano_modelo
            ORDER BY ano_modelo
        ''')
        preco_por_ano = cursor.fetchall()
        
        # 3. Preço Médio por Combustível
        cursor.execute('''
            SELECT co.descricao AS combustivel, AVG(c.preco) AS media_preco
            FROM Carros c
            JOIN Combustivel co ON c.id_combustivel = co.id_combustivel
            GROUP BY co.descricao
        ''')
        preco_por_combustivel = cursor.fetchall()
        
        return jsonify({
            'carros_por_fabricante': carros_por_fabricante,
            'preco_por_ano': preco_por_ano,
            'preco_por_combustivel': preco_por_combustivel
        })
        
    except mysql.connector.Error as err:
        print(f"Erro no MySQL durante consulta de carros: {err}")
        return jsonify({'error': f'Erro ao executar consulta no banco: {err}'}), 500
        
    except Exception as e:
        print(f"Erro inesperado na API de carros: {e}")
        return jsonify({'error': f'Erro inesperado no servidor: {e}'}), 500
        
    finally:
        # Garante que a conexão seja fechada
        if 'conn' in locals() and conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/api/simular', methods=['POST'])
def simular_financiamento():
    """
    API para simulação de financiamento de veículo (Cálculo AMORTIZAÇÃO PRICE).
    Espera JSON com: valor_veiculo, entrada (opcional), prazo (meses), taxa_juros (opcional).
    """
    try:
        dados = request.json
        
        # 1. Obter e validar dados essenciais
        valor_veiculo = float(dados.get('valor_veiculo'))
        
        # Valores opcionais com defaults
        entrada = float(dados.get('entrada', 0))
        prazo = int(dados.get('prazo', 48))
        taxa_juros = float(dados.get('taxa_juros', 0.012)) # Padrão: 1.2% ao mês
        
        if valor_veiculo <= 0 or prazo <= 0 or taxa_juros <= 0:
            return jsonify({'error': 'Parâmetros de simulação inválidos (valor do veículo, prazo ou taxa devem ser positivos).'}), 400
            
        valor_financiado = valor_veiculo - entrada
        
        if valor_financiado <= 0:
            return jsonify({
                'valor_veiculo': round(valor_veiculo, 2),
                'entrada': round(entrada, 2),
                'parcelas': 0,
                'valor_parcela': 0.0,
                'total_pago': round(valor_veiculo, 2),
                'juros_total': 0.0,
                'mensagem': 'Valor à vista ou entrada superior/igual ao valor do veículo.'
            })

        # 2. Cálculo da Parcela (PMT - Tabela Price)
        # Formula: PMT = [PV * i] / [1 - (1 + i)^(-n)]
        parcela = (valor_financiado * taxa_juros) / (1 - math.pow(1 + taxa_juros, -prazo))
        
        total_pago_financiamento = parcela * prazo
        total_pago = total_pago_financiamento + entrada 
        juros_total = total_pago_financiamento - valor_financiado
        
        # 3. Montar Resultado (Idealmente, carro sugerido viria de outra consulta ao banco)
        resultado = {
            'valor_veiculo': round(valor_veiculo, 2),
            'entrada': round(entrada, 2),
            'prazo': prazo,
            'valor_financiado': round(valor_financiado, 2),
            'valor_parcela': round(parcela, 2),
            'total_pago': round(total_pago, 2),
            'juros_total': round(juros_total, 2),
            'taxa_juros': f"{taxa_juros * 100:.2f}% ao mês",
            
            # Dados Sugeridos (Mock)
            'carro_sugerido': 'Volkswagen Golf Comfortline 2022',
            'opcionais': 'Automático, Ar-condicionado, Multimídia'
        }
        
        return jsonify(resultado)
        
    except ValueError:
        return jsonify({'error': 'Dados de entrada inválidos. Certifique-se de que valores numéricos estão corretos.'}), 400
        
    except Exception as e:
        print(f"Erro na simulação: {e}")
        return jsonify({'error': f'Erro interno no servidor: {e}'}), 500

# --- Execução da Aplicação ---

if __name__ == '__main__':
    print("🚀 Iniciando AutoSimulate...")
    
    # Prepara o ambiente de banco de dados
    try:
        criar_banco_se_nao_existir()
        print("✅ Banco de dados verificado/criado com sucesso.")
    except Exception as db_error:
        print(f"❌ ERRO ao criar ou verificar o banco: {db_error}")
        # O aplicativo pode continuar, mas as APIs de banco falharão
    
    # Inicia o servidor Flask
    print("✅ Servidor Flask iniciando na porta 5000 (Modo Debug)")
    print("🌐 Acesse: http://localhost:5000")
    app.run(debug=True, port=5000)