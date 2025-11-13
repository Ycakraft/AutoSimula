# config_example.py
# Rename this file to config.py and update the values below

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'AutoSimula_db'
}

def conexao_banco():
    """
    Estabelece conexão com o banco de dados MySQL.
    Retorna um objeto de conexão ou None em caso de falha.
    """
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

def criar_banco_se_nao_existir():
    """
    Cria o banco de dados e as tabelas necessárias se não existirem.
    """
    try:
        import mysql.connector
        from mysql.connector import Error
        
        # Conecta sem especificar o banco de dados
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        cursor = conn.cursor()
        
        # Cria o banco de dados se não existir
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Cria as tabelas necessárias
        tabelas = ["""
        CREATE TABLE IF NOT EXISTS Fabricante (
            id_fabricante INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            pais_origem VARCHAR(100)
        )
        """, """
        CREATE TABLE IF NOT EXISTS Combustivel (
            id_combustivel INT AUTO_INCREMENT PRIMARY KEY,
            descricao VARCHAR(50) NOT NULL
        )
        """, """
        CREATE TABLE IF NOT EXISTS Carros (
            id_carro INT AUTO_INCREMENT PRIMARY KEY,
            id_fabricante INT,
            id_combustivel INT,
            modelo VARCHAR(100) NOT NULL,
            ano_modelo INT,
            preco DECIMAL(10,2),
            FOREIGN KEY (id_fabricante) REFERENCES Fabricante(id_fabricante),
            FOREIGN KEY (id_combustivel) REFERENCES Combustivel(id_combustivel)
        )
        """]
        
        for tabela in tabelas:
            cursor.execute(tabela)
        
        # Insere alguns dados iniciais se as tabelas estiverem vazias
        cursor.execute("SELECT COUNT(*) FROM Fabricante")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO Fabricante (nome, pais_origem) VALUES
                ('Volkswagen', 'Alemanha'),
                ('Fiat', 'Itália'),
                ('Chevrolet', 'Estados Unidos'),
                ('Ford', 'Estados Unidos'),
                ('Hyundai', 'Coreia do Sul')
            """)
            
        cursor.execute("SELECT COUNT(*) FROM Combustivel")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO Combustivel (descricao) VALUES
                ('Gasolina'),
                ('Álcool'),
                ('Diesel'),
                ('Flex'),
                ('Elétrico'),
                ('Híbrido')
            """)
        
        conn.commit()
        print("Banco de dados e tabelas criados com sucesso!")
        
    except Error as e:
        print(f"Erro ao criar banco de dados: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Se este arquivo for executado diretamente, cria o banco de dados
if __name__ == '__main__':
    criar_banco_se_nao_existir()
