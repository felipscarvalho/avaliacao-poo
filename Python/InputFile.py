import tkinter as tk
from tkinter import filedialog, scrolledtext
import pdfplumber
import pprint


def chooseFile():
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if path:
        with pdfplumber.open(path) as pdf:
            tables = []

            for page_num, page in enumerate(pdf.pages, start=1):
                tabelas = page.extract_tables()
                if tabelas:
                    for tabela in tabelas:
                        tables.append(tabela)

        # Debug no console (print bonito)
        pprint.pprint(tables)

        # Mostra no TextBox formatado
        textBox.delete(1.0, tk.END)
        for i, tabela in enumerate(tables, start=1):
            textBox.insert(tk.END, f"--- Tabela {i} ---\n")
            for linha in tabela:
                textBox.insert(tk.END, " | ".join(str(c) for c in linha if c) + "\n")
            textBox.insert(tk.END, "\n")


window = tk.Tk()
window.title("PDF Reader")
window.geometry("900x600")

button = tk.Button(window, text="Selecionar PDF", command=chooseFile)
button.pack(pady=10)

textBox = scrolledtext.ScrolledText(window, wrap=tk.WORD)
textBox.pack(expand=True, fill="both")

window.mainloop()
