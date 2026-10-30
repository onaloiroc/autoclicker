# autoclicker

Auto clicker para desktop com interface gráfica, escrito em Python.

Intervalo configurável, escolha do botão do mouse, modo de repetição e tecla de
atalho global para ligar e desligar sem voltar para a janela.

## Uso

```bash
pip install -r requirements.txt
python autoclick.py
```

## Como funciona

**O clique roda em outra thread.** Se o laço de clique rodasse na thread da
interface, o Tkinter congelaria — a janela pararia de responder e nem o botão de
parar funcionaria. A thread de clique é controlada por um `threading.Event`,
que serve ao mesmo tempo de flag de estado e de ponto de parada.

**Atalho global com `pynput`.** O atalho precisa funcionar com a janela em
segundo plano: o sentido de um auto clicker é clicar em *outro* programa. O
binding normal do Tkinter só captura tecla com a janela em foco, por isso o
listener de teclado é separado.

**Interface com `ttkbootstrap`** em vez do Tk puro, que tem aparência de
Windows 95.

## Requisitos

Python 3.10 ou superior.

## Licença

MIT
