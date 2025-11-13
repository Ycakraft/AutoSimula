# 🚗 CarMatch - Simulador de Carros

Site interativo para ajudar usuários a escolher o melhor carro com base em suas preferências e situação financeira.

## 🎯 Funcionalidades

- **Página Inicial**: Apresentação do site com call-to-action
- **Página Sobre**: Informações sobre a plataforma e equipe
- **Simulação Inteligente**: Formulário dinâmico que adapta perguntas baseadas nas respostas
- **Resultados Personalizados**: Exibe os 3 melhores carros com base nos critérios do usuário
- **Cálculo de Parcelas**: Simulação financeira com juros compostos
- **Filtros Avançados**: Por tipo, marca, câmbio, motor e orçamento

## 🛠️ Tecnologias

- **Backend**: Python Flask
- **Frontend**: HTML5 + CSS3 (Flexbox)
- **Dados**: Pandas para processamento do CSV
- **Design**: Responsivo e moderno

## 📦 Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Crie um link simbólico para as imagens dos carros:
```bash
# No Windows (PowerShell como Administrador):
New-Item -ItemType SymbolicLink -Path "car-simulator\static\car_images" -Target "..\car_images"

# Ou simplesmente copie a pasta:
xcopy ..\car_images car-simulator\static\car_images\ /E /I
```

3. Execute o servidor:
```bash
python app.py
```

4. Acesse no navegador:
```
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
car-simulator/
├── app.py                      # Aplicação Flask principal
├── requirements.txt            # Dependências Python
├── README.md                   # Este arquivo
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── index.html             # Página inicial
│   ├── sobre.html             # Página sobre
│   ├── simulacao.html         # Formulário de simulação
│   └── resultado.html         # Página de resultados
└── static/                     # Arquivos estáticos
    └── car_images/            # Imagens dos carros (link simbólico)
```

## 🎨 Características do Design

- **Cores**: Gradiente azul-roxo (#667eea → #764ba2)
- **Layout**: Flexbox para responsividade
- **Animações**: Transições suaves e fade-ins
- **UX**: Formulário progressivo com barra de progresso
- **Mobile-First**: Totalmente responsivo

## 📊 Dados

O sistema utiliza o arquivo `carflix_listings.csv` com as seguintes colunas:
- title: Nome do carro
- price: Preço formatado
- link: URL para mais detalhes
- image_url: URL da imagem online
- image_file: Nome do arquivo de imagem local

## 🧮 Cálculo de Parcelas

Fórmula de juros compostos:
```
parcela = preço × [(1 + i)^n × i] / [(1 + i)^n - 1]
```
Onde:
- i = taxa de juros mensal (1,2% = 0,012)
- n = número de parcelas

## 🚀 Próximas Melhorias

- [ ] Exportar relatório em PDF
- [ ] Salvar histórico de simulações
- [ ] Comparação lado a lado detalhada
- [ ] Filtros adicionais (ano, quilometragem)
- [ ] Sistema de favoritos
- [ ] Integração com APIs de financiamento

## 📝 Licença

Projeto desenvolvido para fins educacionais.
