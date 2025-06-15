@echo off
REM Pega o diretório onde está este .bat
set "PROJECT_DIR=%~dp0"

REM Cria venv 'dog' se não existir
if not exist "%PROJECT_DIR%dog\Scripts\activate.bat" (
    py -3 -m venv "%PROJECT_DIR%dog"
)

REM Ativa o ambiente virtual
call "%PROJECT_DIR%dog\Scripts\activate.bat"

REM Atualiza pip e instala dependências sem cache
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r "%PROJECT_DIR%requirements.txt"

REM Move para a pasta src e executa o jogo
cd /d "%PROJECT_DIR%src"
python main.py

pause
