# config.py
import mysql.connector
from mysql.connector import Error

def conexao_banco():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='AutoSimula',
            user='root',
            password='root'
        )
        
        if connection.is_connected():
            print("✅ Conexão ao MySQL bem-sucedida")
            return connection
            
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return None

# Teste da conexão
if __name__ == "__main__":
    conn = conexao_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Carros")
        result = cursor.fetchone()
        print(f"Total de carros no banco: {result[0]}")
        cursor.close()
        conn.close()