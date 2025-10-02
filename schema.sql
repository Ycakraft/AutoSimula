-- Cria Database
CREATE DATABASE IF NOT EXISTS AutoSimula 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_0900_ai_ci;

-- Usa Database
USE AutoSimula;

-- Cria Tabela Fabricante
CREATE TABLE IF NOT EXISTS Fabricante (
    id_fabricante INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL
);

-- Cria Tabela Localizacao
CREATE TABLE IF NOT EXISTS Localizacao (
    id_localizacao INT AUTO_INCREMENT PRIMARY KEY,
    estado CHAR(2) NOT NULL,
    cidade VARCHAR(100) NOT NULL
);

-- Cria Tabela Combustivel
CREATE TABLE IF NOT EXISTS Combustivel (
    id_combustivel INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL  -- gasolina, alcool, flex, diesel, eletrico
);

-- Cria Tabela Carros
CREATE TABLE IF NOT EXISTS Carros (
    id_carro INT AUTO_INCREMENT PRIMARY KEY,
    id_combustivel INT,
    id_localizacao INT,
    id_fabricante INT,
    preco FLOAT NOT NULL,
    cilindradas FLOAT,
    usado BOOLEAN NOT NULL DEFAULT FALSE,
    quilometragem INT DEFAULT 0,
    ano_modelo YEAR NOT NULL,
    automatico BOOLEAN,
    versao VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_combustivel) REFERENCES Combustivel(id_combustivel),
    FOREIGN KEY (id_localizacao) REFERENCES Localizacao(id_localizacao),
    FOREIGN KEY (id_fabricante) REFERENCES Fabricante(id_fabricante)
);

-- Insere dados básicos na tabela Combustivel
INSERT INTO Combustivel (descricao) VALUES 
('Gasolina'),
('Álcool'),
('Flex'),
('Diesel'),
('Elétrico'),
('Híbrido');

-- Insere dados básicos na tabela Fabricante
INSERT INTO Fabricante (nome) VALUES 
('Volkswagen'),
('Fiat'),
('Ford'),
('Chevrolet'),
('Toyota'),
('Honda'),
('Hyundai'),
('Renault'),
('Nissan'),
('BMW'),
('Mercedes-Benz'),
('Audi');

-- Insere dados básicos na tabela Localizacao
INSERT INTO Localizacao (estado, cidade) VALUES 
('SP', 'São Paulo'),
('SP', 'Campinas'),
('RJ', 'Rio de Janeiro'),
('MG', 'Belo Horizonte'),
('RS', 'Porto Alegre'),
('PR', 'Curitiba'),
('SC', 'Florianópolis'),
('BA', 'Salvador'),
('PE', 'Recife'),
('DF', 'Brasília');

-- Insere dados de exemplo na tabela Carros
INSERT INTO Carros (id_combustivel, id_localizacao, id_fabricante, preco, cilindradas, usado, quilometragem, ano_modelo, automatico, versao, modelo) VALUES 
(3, 1, 1, 85000.00, 1.6, TRUE, 45000, 2022, FALSE, 'Comfortline', 'Golf'),
(3, 2, 2, 55000.00, 1.4, TRUE, 60000, 2021, FALSE, 'Attractive', 'Mobi'),
(1, 3, 3, 120000.00, 2.0, FALSE, 0, 2024, TRUE, 'Titanium', 'Focus'),
(3, 4, 4, 95000.00, 1.8, TRUE, 30000, 2023, TRUE, 'Premier', 'Onix'),
(3, 5, 5, 150000.00, 2.0, FALSE, 0, 2024, TRUE, 'XR', 'Corolla'),
(3, 6, 6, 110000.00, 1.5, TRUE, 20000, 2023, TRUE, 'EXL', 'Civic'),
(3, 7, 7, 80000.00, 1.6, TRUE, 35000, 2022, FALSE, 'Comfort', 'HB20'),
(3, 8, 8, 70000.00, 1.0, TRUE, 50000, 2021, FALSE, 'Zen', 'Kwid'),
(4, 9, 9, 180000.00, 2.3, FALSE, 0, 2024, TRUE, 'SL', 'Kicks'),
(5, 10, 10, 350000.00, 0.0, FALSE, 0, 2024, TRUE, 'M Sport', 'i4'),
(4, 1, 11, 450000.00, 2.0, FALSE, 0, 2024, TRUE, 'AMG Line', 'Classe A'),
(1, 2, 12, 280000.00, 2.0, TRUE, 15000, 2023, TRUE, 'S Line', 'A3');

-- Queries para análise de dados (para os gráficos)

-- Quantidade de carros por fabricante (gráfico de barras):
SELECT f.nome AS fabricante, COUNT(*) AS quantidade
FROM Carros c
JOIN Fabricante f ON c.id_fabricante = f.id_fabricante
GROUP BY f.nome
ORDER BY quantidade DESC;

-- Média de quilometragem por ano de modelo (gráfico de linhas):
SELECT ano_modelo, AVG(quilometragem) AS media_km
FROM Carros
WHERE usado = TRUE
GROUP BY ano_modelo
ORDER BY ano_modelo;

-- Média de preço por fabricante (gráfico de barras):
SELECT f.nome AS fabricante, AVG(c.preco) AS media_preco
FROM Carros c
JOIN Fabricante f ON c.id_fabricante = f.id_fabricante
GROUP BY f.nome
ORDER BY media_preco DESC;

-- Média de preço por tipo de combustível (gráfico de barras):
SELECT co.descricao AS combustivel, AVG(c.preco) AS media_preco
FROM Carros c
JOIN Combustivel co ON c.id_combustivel = co.id_combustivel
GROUP BY co.descricao
ORDER BY media_preco DESC;

-- Média de preço por ano de modelo (gráfico de linhas):
SELECT ano_modelo, AVG(preco) AS media_preco
FROM Carros
GROUP BY ano_modelo
ORDER BY ano_modelo;

-- Distribuição de carros usados vs novos (gráfico de pizza):
SELECT 
    CASE WHEN usado = TRUE THEN 'Usado' ELSE 'Novo' END AS condicao,
    COUNT(*) AS quantidade
FROM Carros
GROUP BY usado;

-- Carros por estado (gráfico de barras horizontais):
SELECT l.estado, COUNT(*) AS quantidade
FROM Carros c
JOIN Localizacao l ON c.id_localizacao = l.id_localizacao
GROUP BY l.estado
ORDER BY quantidade DESC;

-- Preço médio por tipo de transmissão (gráfico de barras):
SELECT 
    CASE WHEN automatico = TRUE THEN 'Automático' ELSE 'Manual' END AS transmissao,
    AVG(preco) AS media_preco
FROM Carros
GROUP BY automatico;

-- View para relatório geral
CREATE VIEW relatorio_geral AS
SELECT 
    c.id_carro,
    f.nome AS fabricante,
    c.modelo,
    c.versao,
    c.ano_modelo,
    co.descricao AS combustivel,
    l.estado,
    l.cidade,
    c.preco,
    CASE WHEN c.usado = TRUE THEN 'Usado' ELSE 'Novo' END AS condicao,
    c.quilometragem,
    CASE WHEN c.automatico = TRUE THEN 'Automático' ELSE 'Manual' END AS transmissao,
    c.cilindradas
FROM Carros c
JOIN Fabricante f ON c.id_fabricante = f.id_fabricante
JOIN Combustivel co ON c.id_combustivel = co.id_combustivel
JOIN Localizacao l ON c.id_localizacao = l.id_localizacao;

-- Consulta da view
SELECT * FROM relatorio_geral;

-- Estatísticas resumidas
SELECT 
    COUNT(*) AS total_carros,
    AVG(preco) AS preco_medio_geral,
    MIN(preco) AS menor_preco,
    MAX(preco) AS maior_preco,
    SUM(CASE WHEN usado = TRUE THEN 1 ELSE 0 END) AS total_usados,
    SUM(CASE WHEN usado = FALSE THEN 1 ELSE 0 END) AS total_novos
FROM Carros;