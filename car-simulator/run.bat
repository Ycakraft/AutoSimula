@echo off
echo ========================================
echo   CarMatch - Simulador de Carros
echo ========================================
echo.

REM Verificar se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado! Instale o Python 3.8 ou superior.
    pause
    exit /b 1
)

echo [1/3] Verificando dependencias...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Instalando dependencias...
    pip install -r requirements.txt
) else (
    echo [OK] Dependencias ja instaladas
)

echo.
echo [2/3] Verificando arquivo CSV...
if not exist "..\carflix_listings.csv" (
    echo [AVISO] Arquivo carflix_listings.csv nao encontrado na pasta pai!
    echo Por favor, certifique-se de que o arquivo existe.
)

echo.
echo [3/3] Iniciando servidor Flask...
echo.
echo ========================================
echo   Servidor rodando em:
echo   http://localhost:5000
echo ========================================
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python app.py

pause
