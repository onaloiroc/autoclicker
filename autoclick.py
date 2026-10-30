import threading
import time
import tkinter as tk
from tkinter import messagebox
import pyautogui
from pynput import keyboard
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker Moderno")
        self.root.geometry("430x350")

        self.running = threading.Event()
        self.listener = None

        # tecla padrão
        self.hotkey = keyboard.Key.f8
        self.hotkey_text = tk.StringVar(value="F8")

        self.waiting_key = False  # modo de captura de tecla

        self.build_ui()
        self.start_hotkey_listener()

    # ------------------------- UI ------------------------------------
    def build_ui(self):
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="AutoClicker Moderno",
                  font=("Segoe UI", 16, "bold")).pack(pady=8)

        frame = ttk.Frame(container)
        frame.pack(fill="both", expand=True)

        # Intervalo
        ttk.Label(frame, text="Intervalo (s):").grid(row=0, column=0, sticky="w")
        self.interval_var = tk.StringVar(value="0.1")
        ttk.Entry(frame, textvariable=self.interval_var, width=10).grid(row=0, column=1, sticky="w", pady=5)

        # Botão
        ttk.Label(frame, text="Botão:").grid(row=1, column=0, sticky="w")
        self.button_var = tk.StringVar(value="left")
        bframe = ttk.Frame(frame)
        bframe.grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(bframe, text="Esquerdo", value="left", variable=self.button_var).pack(side="left", padx=4)
        ttk.Radiobutton(bframe, text="Direito", value="right", variable=self.button_var).pack(side="left")

        # Tipo de clique
        self.mode_var = tk.StringVar(value="infinite")
        ttk.Radiobutton(frame, text="Infinito", value="infinite", variable=self.mode_var)\
            .grid(row=2, column=0, sticky="w", pady=4)

        f = ttk.Frame(frame)
        f.grid(row=3, column=0, columnspan=2, sticky="w")
        ttk.Radiobutton(f, text="Fixos:", value="fixed", variable=self.mode_var).pack(side="left")
        self.clicks_var = tk.StringVar(value="100")
        ttk.Entry(f, textvariable=self.clicks_var, width=10).pack(side="left", padx=6)

        # Delay
        ttk.Label(frame, text="Delay inicial (s):").grid(row=4, column=0, sticky="w")
        self.delay_var = tk.StringVar(value="3")
        ttk.Entry(frame, textvariable=self.delay_var, width=10).grid(row=4, column=1, sticky="w", pady=5)

        # Hotkey personalizada
        ttk.Label(frame, text="Tecla de Ativação:").grid(row=5, column=0, sticky="w", pady=4)
        ttk.Label(frame, textvariable=self.hotkey_text,
                  font=("Segoe UI", 12, "bold")).grid(row=5, column=1, sticky="w")

        ttk.Button(frame, text="Selecionar Tecla", bootstyle=INFO,
                   command=self.enable_hotkey_selection).grid(row=6, column=0, columnspan=2, pady=5)

        # Botões iniciar/parar
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="Iniciar",
                                    bootstyle=SUCCESS, width=12, command=self.start_clicking)
        self.start_btn.pack(side="left", padx=8)

        self.stop_btn = ttk.Button(btn_frame, text="Parar",
                                   bootstyle=DANGER, width=12, state="disabled", command=self.stop_clicking)
        self.stop_btn.pack(side="left", padx=8)

        frame.grid_columnconfigure(1, weight=1)

    # ------------------------- HOTKEY PERSONALIZADA -------------------------
    def enable_hotkey_selection(self):
        messagebox.showinfo("Selecionar tecla",
                            "Pressione a tecla desejada para ser a nova hotkey.")
        self.waiting_key = True

    def set_new_hotkey(self, key):
        """Salva a nova tecla como hotkey."""
        self.hotkey = key

        # Converte a tecla para texto legível
        try:
            if hasattr(key, "char") and key.char is not None:
                text = key.char.upper()
            else:
                text = str(key).replace("Key.", "").upper()
        except:
            text = "DESCONHECIDA"

        self.hotkey_text.set(text)

        self.waiting_key = False

    # ------------------------- CLICK LOOP -------------------------
    def click_loop(self):
        try:
            interval = float(self.interval_var.get())
            delay = float(self.delay_var.get())
        except:
            messagebox.showerror("Erro", "Intervalo ou delay inválidos.")
            return

        time.sleep(delay)

        total = None
        if self.mode_var.get() == "fixed":
            try:
                total = int(self.clicks_var.get())
            except:
                messagebox.showerror("Erro", "Número de cliques inválido.")
                return

        count = 0
        while self.running.is_set():
            pyautogui.click(button=self.button_var.get())
            count += 1

            if total and count >= total:
                break

            time.sleep(interval)

        self.running.clear()
        self.update_buttons()

    # ------------------------- START / STOP -------------------------
    def start_clicking(self):
        if not self.running.is_set():
            self.running.set()
            self.update_buttons()
            threading.Thread(target=self.click_loop, daemon=True).start()

    def stop_clicking(self):
        self.running.clear()
        self.update_buttons()

    def update_buttons(self):
        if self.running.is_set():
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
        else:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")

    # ------------------------- HOTKEY GLOBAL -------------------------
    def on_press(self, key):
        if self.waiting_key:  # capturar nova tecla
            self.set_new_hotkey(key)
            return

        if key == self.hotkey:
            if self.running.is_set():
                self.stop_clicking()
            else:
                self.start_clicking()

    def start_hotkey_listener(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.daemon = True
        listener.start()


# Iniciar
app = ttk.Window(themename="darkly")
AutoClickerApp(app)
app.mainloop()
