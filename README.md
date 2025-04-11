# 🕹️ Jogo Kalah - Projeto de Análise e Projetos de Sistemas

Este é um projeto acadêmico desenvolvido para a disciplina de **Análise e Projetos de Sistemas**, com foco na modelagem de software e desenvolvimento de aplicações interativas. O jogo implementado foi o **Kalah**, uma variação do tradicional Mancala.

## 🎯 Objetivo

O objetivo deste projeto é aplicar os conceitos de **Engenharia de Software**, como **especificação de requisitos**, **modelagem UML** e **padrões de projeto**, no desenvolvimento de um jogo funcional com interface gráfica e integração web.

---

## 🧰 Tecnologias Utilizadas

- **Python 3.x** – Linguagem principal do projeto
- **Tkinter** – Biblioteca para construção da interface gráfica
- **DOG (Deploying Over the Grid)** – Ferramenta que permite rodar aplicações Python na web de forma simples
- **UML (Visual Paradigm)** – Para criação dos diagramas de modelagem do sistema

---

## 👨‍💻 Autores
Desenvolvido por Aline Cristina Meyer, Camila Prim e Fabio Fernandes da Silva Junior
Disciplina: Análise e Projetos de Sistemas
Curso: Sistemas de Informação
Instituição: Universidade Federal de Santa Catarina (UFSC)

---

## 🛠️ Estrutura do Projeto

📦 kalah-game/  
├── controller/ 
├── model/ 
|--utils/
├── view/
├── main.py   
├── dogfile.py 
└── README.md


- `model/` – Lógica do jogo e regras
- `view/` – Interface gráfica com Tkinter
- `controller/` – Comunicação entre model e view
- `dogfile.py` – Arquivo para execução via DOG


---

## 🔌 Como Executar

### ✅ Localmente

1. Tenha o Python 3 instalado.
2. Execute o arquivo principal:

```bash
python src/main.py