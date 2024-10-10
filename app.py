import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import sys
import time
import random
import threading
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
from datetime import datetime
import functions


stop_flag = False

def perform_downloading(df, xlsx_file):
    global stop_flag     
    for i, img in enumerate(df["Image"]):
        if stop_flag:
            break 
        try:
            dwd_image = functions.download_image(img)
            df.at[i, "Image"] = dwd_image
            df.to_excel(xlsx_file, index=False)
            print(f"{functions.date_now()} --> ✓ Image downloaded")
        except Exception as e:
            print(e)
            continue
    print(f"{functions.date_now()} --> Travail terminé")
    

class RedirectOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def flush(self):
        pass  # Required method for compatibility

# Function to open a new window with the log box
def open_log_window(df, xlsx_file):

    global stop_flag
    stop_flag = False

    log_window = tk.Toplevel(root)
    log_window.title("Output")
    log_window.geometry("600x450")

    def on_closee():
        global stop_flag
        stop_flag = True
        try:
            sys.stdout = original_stdout
            log_window.destroy()
        except:
            log_window.destroy()

    def stop_work():
        global stop_flag
        stop_flag = True  
        sys.stdout = original_stdout
        log_window.destroy()


    log_window.protocol("WM_DELETE_WINDOW", on_closee)

    log_label = tk.Label(log_window, text="Output", font=("Arial", 16))
    log_label.pack(pady=10)

    log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=80, height=20, font=("Arial", 10))
    log_text.config(state=tk.DISABLED)
    log_text.pack(pady=10)

    stop_button = ttk.Button(log_window, text="Stop", command=stop_work)
    stop_button.pack(pady=10)

    sys.stdout = RedirectOutput(log_text)
    threading.Thread(target=perform_downloading, args=(df, xlsx_file)).start()
    print(f"{functions.date_now()} --> Start Working .....")

def on_start():
    print("L'application a démarré !")

def on_close():
    global stop_flag
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment fermer l'application?"):
        stop_flag = True
        print("Fermeture de l'application")
        root.destroy()

def select_file():
    filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def start_work():
    xlsx_file = file_entry.get()
    
    if not xlsx_file:
        messagebox.showwarning("Attention", "Veuillez sélectionner un fichier Excel.")
    else:
        print(f"{functions.date_now()} --> Travail commencé")
        df = pd.read_excel(xlsx_file)
        open_log_window(df,xlsx_file)

# Main application window
original_stdout = sys.stdout

# GUI Layout
root = tk.Tk()
root.title("Application")

on_start()

root.protocol("WM_DELETE_WINDOW", on_close)



main_frame = ttk.Frame(root)
main_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Configuration des colonnes pour centrer le contenu
main_frame.columnconfigure(0, weight=1)  # Espace avant
main_frame.columnconfigure(1, weight=0)  # Colonne avec widgets
main_frame.columnconfigure(2, weight=1)  # Espace après

# Label du fichier
file_label = ttk.Label(main_frame, text="Fichier Excel (.xlsx):")
file_label.grid(row=0, column=1, sticky="ew", pady=5)

# Champ d'entrée du fichier
file_entry = ttk.Entry(main_frame, width=30)
file_entry.grid(row=1, column=1, sticky="ew", pady=5)

# Bouton "Parcourir"
file_button = ttk.Button(main_frame, text="Parcourir", command=select_file)
file_button.grid(row=2, column=1, sticky="ew", pady=5)

# Espacement supplémentaire pour mettre les boutons en bas
main_frame.rowconfigure(3, weight=1)

# Bouton "Start"
start_button = ttk.Button(main_frame, text="Start", command=start_work)
start_button.grid(row=4, column=1, sticky="ew", pady=5)

root.mainloop()
