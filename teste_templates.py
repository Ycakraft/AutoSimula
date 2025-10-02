# teste_templates.py
import os

def verificar_estrutura():
    print("📁 Verificando estrutura de pastas...")
    
    pastas_necessarias = ['templates', 'static/css', 'static/js']
    arquivos_necessarios = ['templates/index.html', 'static/css/style.css', 'static/js/script.js']
    
    for pasta in pastas_necessarias:
        if os.path.exists(pasta):
            print(f"✅ Pasta '{pasta}' existe")
        else:
            print(f"❌ Pasta '{pasta}' NÃO existe")
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ Arquivo '{arquivo}' existe")
        else:
            print(f"❌ Arquivo '{arquivo}' NÃO existe")
    
    # Listar conteúdo das pastas
    print("\n📂 Conteúdo da pasta templates:")
    if os.path.exists('templates'):
        for item in os.listdir('templates'):
            print(f"   - {item}")

if __name__ == '__main__':
    verificar_estrutura()