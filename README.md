# Jogo Kalah

Jogo de tabuleiro tradicional africano com interface gráfica e multiplayer online.

## Como rodar

### Windows (Mais Fácil)
1. Tenha Python 3.8+ instalado
2. **Duplo clique em `start.bat`** - É só isso!

### Linux/Mac (Também Fácil)
1. Tenha Python 3.8+ instalado
2. **Duplo clique em `start.sh`** (ou execute: `./start.sh`)

Os scripts automaticamente:
- Criam o ambiente virtual
- Instalam dependências  
- Executam o jogo

### Servidor Dog (Necessário para multiplayer)
```bash
# Em terminal separado
pip install dog-server
dog-server
```

## Como jogar
1. Digite seu nome quando solicitado
2. Menu → Iniciar Partida
3. Aguarde outro jogador
4. Clique nas casas do seu lado para jogar

### Regras básicas
- Objetivo: capturar mais sementes que o oponente
- Distribua sementes no sentido anti-horário
- Se a última semente cair no seu armazém, jogue novamente
- Capture sementes quando última semente cair em casa vazia sua

## Problemas comuns
- **Erro de conexão**: Verifique se o servidor Dog está rodando
- **ModuleNotFoundError**: Ative o ambiente virtual e reinstale dependências
- **Tkinter não encontrado**: Reinstale Python com interface gráfica

---
*Projeto acadêmico usando framework Dog para multiplayer*
