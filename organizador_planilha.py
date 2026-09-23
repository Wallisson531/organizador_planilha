import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

import pandas as pd


class OrganizadorPlanilha:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Organizador de Planilhas")
        self.janela.geometry("700x600")

        self.arquivo = None
        self.df = None
        self.checkboxes = {}

        titulo = tk.Label(
            janela,
            text="Organizador de Planilhas Excel",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        self.lbl_arquivo = tk.Label(
            janela,
            text="Nenhuma planilha selecionada",
            wraplength=650
        )
        self.lbl_arquivo.pack(pady=5)

        btn_selecionar = tk.Button(
            janela,
            text="Selecionar Planilha",
            command=self.selecionar_planilha,
            width=25
        )
        btn_selecionar.pack(pady=5)

        frame_colunas = tk.LabelFrame(
            janela,
            text="Selecione as colunas que deseja manter"
        )

        frame_colunas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.canvas = tk.Canvas(frame_colunas)

        scrollbar = ttk.Scrollbar(
            frame_colunas,
            orient="vertical",
            command=self.canvas.yview
        )

        self.frame_checks = tk.Frame(self.canvas)

        self.frame_checks.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.frame_checks,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.progresso = ttk.Progressbar(
            janela,
            length=500,
            mode="determinate"
        )

        self.progresso.pack(pady=10)

        btn_processar = tk.Button(
            janela,
            text="Gerar Planilha",
            bg="green",
            fg="white",
            width=25,
            command=self.processar
        )

        btn_processar.pack(pady=5)

        self.log = tk.Text(
            janela,
            height=8
        )

        self.log.pack(
            fill="x",
            padx=10,
            pady=10
        )

    def escrever_log(self, texto):
        self.log.insert(tk.END, texto + "\n")
        self.log.see(tk.END)

    def selecionar_planilha(self):

        self.arquivo = filedialog.askopenfilename(
            title="Selecione uma planilha",
            filetypes=[
                ("Excel", "*.xlsx *.xls")
            ]
        )

        if not self.arquivo:
            return

        self.lbl_arquivo.config(
            text=self.arquivo
        )

        try:

            self.df = pd.read_excel(self.arquivo)

            self.escrever_log(
                "Planilha carregada com sucesso."
            )

            for widget in self.frame_checks.winfo_children():
                widget.destroy()

            self.checkboxes.clear()

            for coluna in self.df.columns:

                var = tk.BooleanVar(value=True)

                chk = tk.Checkbutton(
                    self.frame_checks,
                    text=coluna,
                    variable=var
                )

                chk.pack(
                    anchor="w",
                    padx=10
                )

                self.checkboxes[coluna] = var

            self.escrever_log(
                f"{len(self.df.columns)} colunas encontradas."
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )

    def processar(self):

        if self.df is None:
            messagebox.showwarning(
                "Aviso",
                "Selecione uma planilha primeiro."
            )
            return

        colunas_selecionadas = []

        for coluna, var in self.checkboxes.items():

            if var.get():
                colunas_selecionadas.append(coluna)

        if not colunas_selecionadas:

            messagebox.showwarning(
                "Aviso",
                "Selecione ao menos uma coluna."
            )

            return

        try:

            self.progresso["value"] = 20

            self.escrever_log(
                "Filtrando colunas..."
            )

            df_filtrado = self.df[
                colunas_selecionadas
            ]

            self.progresso["value"] = 60

            downloads = os.path.join(
                os.path.expanduser("~"),
                "Downloads"
            )

            nome_arquivo = (
                f"planilha_filtrada_"
                f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
            )

            arquivo_saida = os.path.join(
                downloads,
                nome_arquivo
            )

            self.escrever_log(
                "Salvando arquivo..."
            )

            df_filtrado.to_excel(
                arquivo_saida,
                index=False
            )

            self.progresso["value"] = 100

            self.escrever_log(
                "Arquivo criado com sucesso."
            )

            messagebox.showinfo(
                "Sucesso",
                f"Arquivo salvo em:\n\n{arquivo_saida}"
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )


if __name__ == "__main__":

    janela = tk.Tk()

    app = OrganizadorPlanilha(janela)

    janela.mainloop()