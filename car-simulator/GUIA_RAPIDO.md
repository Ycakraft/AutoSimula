# 🚀 Guia Rápido - CarMatch

## Como executar o projeto

### Opção 1: Usando o script automático (Recomendado)
```bash
# Basta dar duplo clique no arquivo:
run.bat
```

### Opção 2: Manualmente
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar o servidor
python app.py

# 3. Abrir no navegador
http://localhost:5000
```

## 📱 Como usar o site

### 1. Página Inicial
- Clique em "Iniciar Simulação" para começar

### 2. Formulário de Simulação
Responda as perguntas:
- **Possui carro?** Se sim, informe se está quitado e o modelo
- **Forma de pagamento:** À vista ou financiado
  - **Financiado:** Informe valor da parcela e quantidade de meses
  - **À vista:** Informe o valor máximo disponível
- **Preferências:**
  - Tipo de carro (SUV, Hatch, Sedan, etc.)
  - Prioridade (economia, conforto, potência, etc.)
  - Tipo de câmbio
  - Tipo de motor

### 3. Resultados
O sistema mostrará os **3 melhores carros** baseados em:
- ✅ Suas preferências
- ✅ Seu orçamento
- ✅ Melhor custo-benefício

Cada resultado inclui:
- 📸 Foto do carro
- 💰 Preço
- 💳 Valor da parcela (se financiado)
- 🏷️ Tags (marca, tipo, câmbio, motor)
- 🔗 Link para ver mais detalhes

## 🎯 Dicas

1. **Seja específico:** Quanto mais detalhes você fornecer, melhores serão as recomendações
2. **Experimente filtros diferentes:** Teste várias combinações para encontrar o carro ideal
3. **Compare os 3 resultados:** Analise as diferenças entre as opções apresentadas
4. **Verifique as parcelas:** Se for financiar, veja se o valor cabe no seu orçamento

## 🔧 Solução de Problemas

### Erro: "Módulo não encontrado"
```bash
pip install -r requirements.txt
```

### Erro: "CSV não encontrado"
Certifique-se de que o arquivo `carflix_listings.csv` está na pasta pai (`Selenium/`)

### Erro: "Porta já em uso"
Outro programa está usando a porta 5000. Feche-o ou altere a porta no `app.py`: 
```python
app.run(debug=True, port=5001)  # Mude para outra porta
```

### Imagens não aparecem
Verifique se a pasta `static/car_images/` contém as imagens dos carros

## 📊 Dados

O sistema processa automaticamente:
- **Marcas:** Extraídas do CSV
- **Tipos:** SUV, Hatch, Sedan (classificação automática)
- **Câmbio:** Manual/Automático (detectado no título)
- **Motor:** Combustão/Híbrido/Elétrico (detectado no título)
- **Preços:** Convertidos para cálculos

## 💡 Funcionalidades

✅ Formulário dinâmico (perguntas mudam conforme respostas)
✅ Barra de progresso visual
✅ Cálculo de parcelas com juros (1,2% a.m.)
✅ Filtros inteligentes
✅ Design responsivo (funciona em celular)
✅ Animações suaves
✅ Integração com CSV real

## 🎨 Personalização

Para alterar cores, edite os arquivos em `templates/`:
- `base.html` - Cores principais e navbar
- `index.html` - Página inicial
- `simulacao.html` - Formulário
- `resultado.html` - Resultados

Cores atuais:
- Primária: `#667eea` (azul)
- Secundária: `#764ba2` (roxo)
- Fundo: Gradiente azul-roxo

Enjoy! 🚗💨
