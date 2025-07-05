#!/bin/bash

echo "=== Iniciando Jogo Kalah ==="

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não encontrado. Instale Python 3.8+ primeiro."
    exit 1
fi

# Criar ambiente virtual se não existir
if [ ! -d "dog" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv dog
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source dog/bin/activate

# Atualizar pip e instalar dependências
echo "Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Executar o jogo
echo "Iniciando o jogo..."
cd src
python main.py

echo "Jogo finalizado."
read -p "Pressione Enter para sair..."
