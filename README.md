<h1 align="center">🧟‍♂️ ZombieRunner 🎮</h1>

<p align="center">
  <b>Um jogo 2D em Python + Pygame • Atividade Prática</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-completo-brightgreen?style=for-the-badge">
  <img src="https://img.shields.io/badge/python-3.12-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/pygame-2.5.2-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/plataforma-windows%20exe-lightgrey?style=for-the-badge">
</p>

---

## Sobre o Jogo

**ZombieRunner** é um jogo 2D estilo side-scroll onde você controla um sobrevivente armado enfrentando hordas de zumbis.  
O objetivo é sobreviver o máximo possível enquanto elimina inimigos, desvia dos ataques e acumula pontos.

O jogo foi criado **do zero**, seguindo boas práticas de modularização, uso de assets externos, efeitos sonoros, animações e interface inicial.

---


## Controles

| Ação | Tecla |
|------|--------|
| Mover | ⬅ ↑ ↓ ➡ setas |
| Atirar | SPACE |
| Sair | ESC |
| Iniciar jogo | ENTER |

---

## Funcionalidades

- 🧍 Movimentação completa nas quatro direções  
- 🔫 Sistema de tiros com cooldown  
- 🧟‍♂️ Inimigos zumbis com movimentação dinâmica  
- 💥 Colisões entre balas e inimigos  
- ❤️ Sistema de vidas  
- 🏆 Pontuação dinâmica  
- 🎵 Efeitos sonoros (tiro, impacto, música ambiente)  
- 🌆 Parallax no fundo (duas camadas animadas)  
- 📜 Menu inicial e tela de Game Over  
- 🔧 Arquitetura modular profissional  
- 🎨 Sprites e imagens customizadas  
- 📦 Suporte a build em EXE para Windows  

---

## Estrutura do Projeto

ZombieRunner/
│── main.py
│── requirements.txt
│── README.md
│
├── code/
│ ├── Const.py
│ ├── Game.py
│ ├── Player.py
│ ├── Zombie.py
│ ├── Bullet.py
│ ├── Score.py
│ ├── Background.py
│ ├── Parallax.py
│ ├── Menu.py
│ └── init.py
│
└── asset/
├── player.png
├── enemy.png
├── bullet.png
├── background.png
├── menu_background.png
├── shoot.wav
├── hit.wav
└── music.wav

yaml
Copiar código

---

## ▶ Como Executar (modo desenvolvimento)

### 1️⃣ Instalar dependências

```bash
pip install -r requirements.txt
Rodar o jogo
bash
Copiar código
python main.py
Como Compilar para Windows (EXE)
Instale o PyInstaller:

bash
Copiar código
pip install pyinstaller
Na pasta do projeto:

bash
Copiar código
pyinstaller --onefile main.py
Vá até dist/ e copie:

css
Copiar código
main.exe
asset/
Crie o arquivo ZIP final:

python
Copiar código
ZombieRunner.zip
Tecnologias
Python 3.x

Pygame

PyInstaller

Ferramentas online para sprites/sons


João Prates
Projeto desenvolvido para a Atividade Prática de Programação.

<p align="center"> <i>“Sobreviva. Atire. Repita.”</i> </p> ```