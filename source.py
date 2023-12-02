import os
import sys
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class ImageRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Renamer")
        self.root.geometry("400x300")
        self.root.iconbitmap(default='icon.ico')  # Coloque o caminho do ícone desejado

        # Configurando o tema escuro
        self.root.tk_setPalette(background='#2E2E2E', foreground='#FFFFFF')

        self.create_widgets()

    def create_widgets(self):
        self.label_directory = tk.Label(self.root, text="Digite o caminho do diretório raiz:")
        self.label_directory.pack(pady=10)

        self.entry_directory = tk.Entry(self.root, width=40)
        self.entry_directory.pack(pady=10)

        self.button_select_directory = tk.Button(self.root, text="Selecionar Diretório", command=self.select_directory)
        self.button_select_directory.pack(pady=10)

        self.label_format = tk.Label(self.root, text="Selecione o formato desejado:")
        self.label_format.pack(pady=5)

        self.format_var = tk.StringVar()
        self.format_var.set(".jpg")

        format_options = [".jpg", ".png", ".webp"]
        self.format_combobox = ttk.Combobox(self.root, textvariable=self.format_var, values=format_options, state="readonly")
        self.format_combobox.pack(pady=5)

        self.button_process = tk.Button(self.root, text="Processar", command=self.process_directory)
        self.button_process.pack(pady=10)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

        self.label_credits = tk.Label(self.root, text="Esse programa foi feito por Wang Tianming.")
        self.label_credits.pack(pady=20)

    def select_directory(self):
        root_folder = filedialog.askdirectory(title="Selecionar Diretório Raiz")
        self.entry_directory.delete(0, tk.END)
        self.entry_directory.insert(0, root_folder)

    def process_directory(self):
        root_folder = self.entry_directory.get()

        if not root_folder:
            self.status_label.config(text="Por favor, digite ou selecione um diretório.")
            return

        try:
            self.process_subdirectories(root_folder)
            self.status_label.config(text="Renomeação concluída!")
        except Exception as e:
            self.status_label.config(text=f"Erro ao renomear: {e}")

    def process_subdirectories(self, root_folder):
        for subdir in os.listdir(root_folder):
            full_path = os.path.join(root_folder, subdir)

            if os.path.isdir(full_path):
                self.status_label.config(text=f"Processando subdiretório: {full_path}")
                self.convert_and_rename_files(full_path)

    def convert_and_rename_files(self, directory):
        selected_format = self.format_var.get()

        for subdir, _, files in os.walk(directory):
            for file in files:
                if not file.lower().endswith(selected_format):
                    image_path = os.path.join(subdir, file)
                    output_path = os.path.join(subdir, f"{os.path.splitext(file)[0]}{selected_format}")

                    try:
                        img = Image.open(image_path)
                        img.convert("RGB").save(output_path, "JPEG")
                        os.remove(image_path)
                    except Exception as e:
                        print(f"Erro ao converter {image_path} para {selected_format}: {e}")

if __name__ == "__main__":
    # Oculta a janela de terminal quando executado como um arquivo executável
    if hasattr(sys, 'frozen'):
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.path.join(os.path.dirname(sys.executable), 'error.log'), 'a')
    
    root = tk.Tk()
    app = ImageRenamerApp(root)
    root.mainloop()
