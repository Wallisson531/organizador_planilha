import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

class LimpadorPlanilha:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title('Organizador de Planilha')
        self.janela.geometry("600x350")
        self.janela.resizable(False, False)

        self.arquivo = ''

        titulo = tk.Label(
            janela,
            text='Organizador de Planilha Excel',
            font=('Arial', 16, 'bold')
        )
        titulo.pack(pady=10)

        self.label_arquivo = tk.Label(
            janela,
            text='Nenhum arquivo selecionado',
            wraplength=500
        )
        self.label_arquivo.pack(pady=5)

        btn_selecionar = tk.Button(
            janela,
            text='Selecionar Arquivo',
            width=25,
            command=self.selecionar_arquivo
        )
        btn_selecionar.pack(pady=5)

        btn_processar = tk.Button(
            janela,
            text='Processar Planilha',
            width=25,
            bg='green',
            fg='white',
            command=self.processar
        )
        btn_processar.pack(pady=5)

        self.progresso = ttk.Progressbar(
            janela,
            orient='horizontal',
            length=400,
            mode='determinate'
       )
        self.progresso.pack(pady=5)

        self.log = tk.Text(
            janela,
            height=8,
            width=70
        )
        self.log.pack(pady=10)

        