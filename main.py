import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import json
import os

# Clé API Claude
API_KEY = "YOUR_API_KEY_ANTROPIC"
API_URL = "https://api.anthropic.com/v1/messages"
SAVE_DIR = "cours_exercices"

# Fonction pour appeler l'API Claude
def call_claude(prompt):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": "claude-3-5-sonnet-20241022",
        "system": "Vous êtes un assistant utile qui aide à générer des cours et exercices.",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        try:
            response_json = response.json()
            if "content" in response_json and response_json["content"]:
                return response_json["content"][0]["text"]
            else:
                return "Aucune réponse générée."
        except KeyError as e:
            messagebox.showerror("Erreur API", f"Erreur de clé : {e}")
            return None
    else:
        try:
            error_message = response.json()["error"]["message"]
            messagebox.showerror("Erreur API", f"Erreur : {error_message}")
        except Exception as e:
            messagebox.showerror("Erreur API", f"Erreur inattendue : {e}")
        return None

# Sauvegarde automatique en JSON
def save_to_json_automatique(course, exercises):
    """Sauvegarde automatiquement le cours et les exercices dans le dossier `cours_exercices`."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Nom du fichier basé sur le sujet
    subject = subject_entry.get().strip().replace(" ", "_").lower()
    file_path = os.path.join(SAVE_DIR, f"{subject}.json")
    
    data = {
        "course": course,
        "exercises": exercises
    }
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    messagebox.showinfo("Succès", f"Cours et exercices sauvegardés dans : {file_path}")
    refresh_course_list()

# Sauvegarde manuelle en JSON
def save_to_json_manual():
    """Enregistre manuellement le cours et les exercices dans le dossier `cours_exercices`."""
    course_content = course_text.get("1.0", tk.END).strip()
    exercises_content = exercises_text.get("1.0", tk.END).strip()
    if not course_content:
        messagebox.showerror("Erreur", "Aucun cours à sauvegarder.")
        return

    save_to_json_automatique(course_content, exercises_content)

# Récupération des cours disponibles
def refresh_course_list():
    """Met à jour la liste des cours disponibles dans l'interface."""
    course_listbox.delete(0, tk.END)
    if os.path.exists(SAVE_DIR):
        for filename in os.listdir(SAVE_DIR):
            if filename.endswith(".json"):
                course_listbox.insert(tk.END, filename)

# Importer un cours et ses exercices
def load_selected_course():
    """Charge le cours et les exercices depuis le fichier sélectionné."""
    selected_file = course_listbox.get(tk.ACTIVE)
    if not selected_file:
        messagebox.showerror("Erreur", "Aucun fichier sélectionné.")
        return

    file_path = os.path.join(SAVE_DIR, selected_file)
    with open(file_path, "r") as file:
        data = json.load(file)
    course_text.delete("1.0", tk.END)
    course_text.insert(tk.END, data.get("course", ""))
    exercises_text.delete("1.0", tk.END)
    exercises_text.insert(tk.END, data.get("exercises", ""))
    messagebox.showinfo("Succès", f"Cours et exercices chargés depuis : {file_path}")

# Fonction pour générer un cours
def generate_course():
    """Génère un cours structuré."""
    subject = subject_entry.get()
    level = level_entry.get()
    duration = duration_entry.get()
    if not subject or not level or not duration:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return

    prompt = f"Génère un cours structuré sur le sujet '{subject}' pour un niveau '{level}' avec une durée de '{duration}'. Inclut un plan avec des titres, des descriptions et des objectifs pédagogiques."
    course = call_claude(prompt)
    if course:
        course_text.delete("1.0", tk.END)
        course_text.insert(tk.END, course)

# Fonction pour générer des exercices
def generate_exercises():
    """Génère des exercices basés sur le contenu du cours."""
    course_content = course_text.get("1.0", tk.END).strip()
    if not course_content:
        messagebox.showerror("Erreur", "Veuillez d'abord générer un cours.")
        return

    prompt = f"Génère des exercices basés sur ce cours : {course_content}. Inclut des QCM, des questions ouvertes et des exercices pratiques."
    exercises = call_claude(prompt)
    if exercises:
        exercises_text.delete("1.0", tk.END)
        exercises_text.insert(tk.END, exercises)

        # Sauvegarder automatiquement après génération des exercices
        save_to_json_automatique(course_text.get("1.0", tk.END).strip(), exercises_text.get("1.0", tk.END).strip())

# Interface utilisateur avec tkinter
root = tk.Tk()
root.title("Générateur de Cours et Exercices")

# Widgets de saisie
tk.Label(root, text="Sujet :").grid(row=0, column=0, padx=10, pady=5)
subject_entry = tk.Entry(root, width=30)
subject_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Niveau :").grid(row=1, column=0, padx=10, pady=5)
level_entry = tk.Entry(root, width=30)
level_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Durée :").grid(row=2, column=0, padx=10, pady=5)
duration_entry = tk.Entry(root, width=30)
duration_entry.grid(row=2, column=1, padx=10, pady=5)

# Boutons d'action
tk.Button(root, text="Générer le cours", command=generate_course).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="Générer les exercices", command=generate_exercises).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="Enregistrer Cours/Exercices", command=save_to_json_manual).grid(row=5, column=0, columnspan=2, pady=10)

# Liste des cours
tk.Label(root, text="Cours disponibles :").grid(row=6, column=0, columnspan=2, pady=5)
course_listbox = tk.Listbox(root, width=50, height=5)
course_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
tk.Button(root, text="Récupérer le cours/exercices", command=load_selected_course).grid(row=8, column=0, columnspan=2, pady=10)

# Zones de texte
tk.Label(root, text="Cours généré :").grid(row=9, column=0, columnspan=2)
course_text = tk.Text(root, height=10, width=60)
course_text.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

tk.Label(root, text="Exercices générés :").grid(row=11, column=0, columnspan=2)
exercises_text = tk.Text(root, height=10, width=60)
exercises_text.grid(row=12, column=0, columnspan=2, padx=10, pady=5)

# Charger les cours disponibles au démarrage
refresh_course_list()

# Lancer l'application
root.mainloop()
