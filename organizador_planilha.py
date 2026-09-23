import os
import tkinter as tk
from datetime import datetime
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

    def escrever_log(self,menssagem):
        self.log.insert(tk.END, menssagem + "\n")
        self.log.see(tk.END)

    def selecionar_arquivo(self):
        self.arquivo = filedialog.askopenfilename(
            title='Selecione a Planilha',
            filetypes=[('Excel', '*.xlsx *.xls')]
        )
        if self.arquivo:
            self.label_arquivo.config(text=self.arquivo)
            self.escrever_log("Arquivo selecionado com sucesso.")

    def processar(self):
        if not self.arquivo:
            messagebox.showwarning(
                'Atenção',
                'Selecione uma planilha primeiro!'
            )
            return
        try:
            self.progresso['value'] = 20

            self.escrever_log('Lendo planilha...')
            df = pd.read_excel(self.arquivo)
            self.progresso['value'] = 40

            colunas_desejadas = [
                'FZ',
                'MODELO',
                'FM',
                'CLIENTE',
                'Carro',
                'DATA DE CÁSULO',
                'QTD'
            ]

            self.escrever_log('Filtrando colunas...')
            df_filtrando = df[colunas_desejadas]

            self.progresso['value'] = 70

            downloads = os.path.join(
                os.path.expanduser('~'),
                'Downloads'
            )

            nome_arquivo = (
                f'Planilha_limpa_'
                f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
            )

            arquivo_saida = os.path.join(
                downloads,
                nome_arquivo
            )

            self.escrever_log('Salvando arquivo...')

            df_filtrando.to_excel(
                arquivo_saida,
                index=False
            )

            self.progresso['value'] = 100

            self.escrever_log(
                f'Arquivo salvo com sucesso: {arquivo_saida}'
            )

            messagebox.showinfo(
                'Sucesso',
                f'Planilha gerada com sucesso!\n\n{arquivo_saida}'
            )

        except Exception as erro:
            messagebox.showerror(
                'Erro',
                str(erro)
            )

janela = tk.Tk()
app =LimpadorPlanilha(janela)

janela.mainloop()