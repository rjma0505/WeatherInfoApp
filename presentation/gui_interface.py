import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta

from logic.controller import fetch_forecast_by_city_name
from data_access.ipma_api import listar_cidades

# --- Traduções e Globais ---
# Mapeamento de descrição em inglês para ficheiros de ícone
ICON_MAP = {
    "Clear sky": "clear.png",
    "Partly cloudy": "partly_cloudy.png",
    "Cloudy": "cloudy.png",
    "Overcast": "overcast.png",
    "Rain": "rain.png",
    "Heavy rain": "heavy_rain.png",
    "Showers": "showers.png",
    "Thunderstorm": "storm.png"
}

ICON_FOLDER = os.path.join("assets", "weather_icons")

# Estrutura para traduções
TRANSLATIONS = {
    "pt": {
        "app_title": "Previsão do Tempo",
        "fetch_button": "Ver Previsão",
        "prev_day_button": "← Dia anterior",
        "next_day_button": "Dia seguinte →",
        "weather_error": "Não foi possível obter a previsão.",
        "network_error": "Não foi possível contactar o servidor:",
        "today": "Hoje",
        "tomorrow": "Amanhã",
        "theme_label": "Tema",
        "language_label": "Idioma",
        "lang_labels": "PT - EN",
        "days_of_week": ("Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"),
        "descriptions": {
            "Clear sky": "Céu limpo",
            "Partly cloudy": "Parcialmente nublado",
            "Cloudy": "Nublado",
            "Overcast": "Encoberto",
            "Rain": "Chuva",
            "Heavy rain": "Chuva forte",
            "Showers": "Aguaceiros",
            "Thunderstorm": "Trovoada"
        }
    },
    "en": {
        "app_title": "Weather Forecast",
        "fetch_button": "View Forecast",
        "prev_day_button": "← Previous day",
        "next_day_button": "Next day →",
        "weather_error": "Could not get the forecast.",
        "network_error": "Could not contact the server:",
        "today": "Today",
        "tomorrow": "Tomorrow",
        "theme_label": "Theme",
        "language_label": "Language",
        "lang_labels": "PT - EN",
        "days_of_week": ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"),
        "descriptions": {
            "Clear sky": "Clear sky",
            "Partly cloudy": "Partly cloudy",
            "Cloudy": "Cloudy",
            "Overcast": "Overcast",
            "Rain": "Rain",
            "Heavy rain": "Heavy rain",
            "Showers": "Showers",
            "Thunderstorm": "Thunderstorm"
        }
    }
}

# Temas da aplicação
THEMES = {
    "light": {
        "bg": "#F0F0F0",
        "fg": "#000000",
        "fg_muted": "#505050",
        "btn_bg": "#E1E1E1",
        "btn_fg": "#000000",
        "special_btn_bg": "green",
        "special_btn_fg": "white",
        "combo_bg": "#FFFFFF",
        "combo_fg": "#000000",
        "slider_trough": "#CCCCCC"
    },
    "dark": {
        "bg": "#2E2E2E",
        "fg": "#FFFFFF",
        "fg_muted": "#A0A0A0",
        "btn_bg": "#555555",
        "btn_fg": "#FFFFFF",
        "special_btn_bg": "#2A722A",
        "special_btn_fg": "white",
        "combo_bg": "#3C3C3C",
        "combo_fg": "#FFFFFF",
        "slider_trough": "#444444"
    }
}

# Declaração das variáveis globais
current_language = "pt"
current_theme_name = "light"

# Variáveis globais para os widgets
root = None
style = None
title_label = None
dropdown = None
icon_label = None
forecast_label = None
nav_frame = None
btn_anterior = None
btn_seguinte = None
botao = None
copyright_label = None
theme_frame = None
theme_slider = None
language_frame = None
language_slider = None
day_index = None
forecast_data = []

def get_icon_image(description):
    filename = ICON_MAP.get(description, "unknown.png")
    path = os.path.join(ICON_FOLDER, filename)
    try:
        img = Image.open(path)
        img = img.resize((80, 80), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Erro ao carregar ícone: {e}")
        placeholder = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
        return ImageTk.PhotoImage(placeholder)

def atualizar_previsao():
    global forecast_data, day_index, dropdown
    cidade = dropdown.get()
    try:
        forecast_data = fetch_forecast_by_city_name(cidade)
    except Exception as e:
        messagebox.showerror("Erro de Rede", f"{TRANSLATIONS[current_language]['network_error']} {e}")
        forecast_data = []
        return
    if not forecast_data:
        messagebox.showerror("Erro", TRANSLATIONS[current_language]['weather_error'])
        return
    day_index.set(0)
    mostrar_dia()

def mostrar_dia():
    global current_language, forecast_data, day_index, forecast_label, icon_label
    if not forecast_data: return
    index = day_index.get()
    if index >= len(forecast_data): return

    dia = forecast_data[index]
    data_formatada = dia["date"]
    hoje = datetime.now().date()
    data_dia = datetime.strptime(data_formatada, "%Y-%m-%d").date()
    
    if data_dia == hoje:
        prefixo = TRANSLATIONS[current_language]["today"]
    elif data_dia == hoje + timedelta(days=1):
        prefixo = TRANSLATIONS[current_language]["tomorrow"]
    else:
        prefixo = TRANSLATIONS[current_language]["days_of_week"][data_dia.weekday()]

    descricao_en = dia["weather_description"]
    descricao_traduzida = TRANSLATIONS[current_language]["descriptions"].get(descricao_en, descricao_en)

    texto = f"{prefixo} ({data_formatada}):\n{descricao_traduzida} - Min: {dia['tMin']}°C | Max: {dia['tMax']}°C"
    forecast_label.config(text=texto)

    icon = get_icon_image(descricao_en)
    if icon:
        icon_label.config(image=icon)
        icon_label.image = icon

def apply_theme(theme):
    global root, style, title_label, nav_frame, forecast_label, icon_label, btn_anterior, btn_seguinte, botao, copyright_label, theme_frame, theme_slider, language_frame, language_slider
    
    if not root: return
    
    root.config(bg=theme["bg"])
    nav_frame.config(bg=theme["bg"])
    title_label.config(bg=theme["bg"], fg=theme["fg"])
    forecast_label.config(bg=theme["bg"], fg=theme["fg"])
    icon_label.config(bg=theme["bg"])
    style.configure("TCombobox", fieldbackground=theme["combo_bg"], foreground=theme["combo_fg"])
    btn_anterior.config(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_bg"], activeforeground=theme["btn_fg"], highlightbackground=theme["bg"])
    btn_seguinte.config(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_bg"], activeforeground=theme["btn_fg"], highlightbackground=theme["bg"])
    botao.config(bg=theme["special_btn_bg"], fg=theme["special_btn_fg"], activebackground=theme["special_btn_bg"], activeforeground=theme["special_btn_fg"], highlightbackground=theme["bg"])
    copyright_label.config(bg=theme["bg"], fg=theme["fg_muted"])
    theme_frame.config(bg=theme["bg"], fg=theme["fg"])
    theme_slider.config(bg=theme["bg"], troughcolor=theme["slider_trough"])
    language_frame.config(bg=theme["bg"], fg=theme["fg"])
    if language_slider: # Verifica se o slider já existe
        language_slider.config(bg=theme["bg"], troughcolor=theme["slider_trough"])

def toggle_theme_by_slider(slider_value):
    global current_theme_name
    value = int(float(slider_value))
    target_theme = "dark" if value == 1 else "light"
    if target_theme != current_theme_name:
        current_theme_name = target_theme
        apply_theme(THEMES[current_theme_name])

def update_ui_texts():
    global root, title_label, btn_anterior, btn_seguinte, botao, theme_frame, language_frame
    if not root: return
    
    root.title(TRANSLATIONS[current_language]["app_title"])
    title_label.config(text=TRANSLATIONS[current_language]["app_title"])
    btn_anterior.config(text=TRANSLATIONS[current_language]["prev_day_button"])
    btn_seguinte.config(text=TRANSLATIONS[current_language]["next_day_button"])
    botao.config(text=TRANSLATIONS[current_language]["fetch_button"])
    theme_frame.config(text=TRANSLATIONS[current_language]["theme_label"])
    language_frame.config(text=TRANSLATIONS[current_language]["language_label"])
    mostrar_dia()

def toggle_language_by_slider(slider_value):
    global current_language
    value = int(float(slider_value))
    target_lang = "en" if value == 1 else "pt"
    if target_lang != current_language:
        current_language = target_lang
        update_ui_texts()
        
def run_gui():
    global root, style, title_label, dropdown, icon_label, forecast_label, nav_frame, btn_anterior, btn_seguinte, botao, copyright_label, theme_frame, theme_slider, language_frame, language_slider, day_index, forecast_data

    root = tk.Tk()
    root.title(TRANSLATIONS[current_language]["app_title"])
    root.geometry("400x500")
    root.minsize(400, 500)

    style = ttk.Style(root)

    title_label = tk.Label(root, text=TRANSLATIONS[current_language]["app_title"], font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    cidades = listar_cidades()
    nomes_cidades = [c["local"] for c in cidades]
    selected_city = tk.StringVar(value=nomes_cidades[0])

    dropdown = ttk.Combobox(root, textvariable=selected_city, values=nomes_cidades, state="readonly")
    dropdown.pack(pady=5)

    icon_label = tk.Label(root)
    icon_label.pack(pady=10)

    forecast_label = tk.Label(root, text="", font=("Helvetica", 11), justify=tk.CENTER)
    forecast_label.pack()

    day_index = tk.IntVar(value=0)
    forecast_data = []

    nav_frame = tk.Frame(root)
    nav_frame.pack(pady=10)

    btn_anterior = tk.Button(nav_frame, text=TRANSLATIONS[current_language]["prev_day_button"], command=lambda: (day_index.set(day_index.get() - 1), mostrar_dia()) if day_index.get() > 0 else None)
    btn_anterior.grid(row=0, column=0, padx=5)

    btn_seguinte = tk.Button(nav_frame, text=TRANSLATIONS[current_language]["next_day_button"], command=lambda: (day_index.set(day_index.get() + 1), mostrar_dia()) if forecast_data and day_index.get() < len(forecast_data) - 1 else None)
    btn_seguinte.grid(row=0, column=1, padx=5)

    botao = tk.Button(root, text=TRANSLATIONS[current_language]["fetch_button"], command=atualizar_previsao, padx=10, pady=5)
    botao.pack(pady=10)

    copyright_text = f"WeatherInfoApp © {datetime.now().year}"
    copyright_label = tk.Label(root, text=copyright_text, font=("Segoe UI", 8))
    copyright_label.pack(side=tk.BOTTOM, pady=5)
    
    theme_frame = tk.LabelFrame(root, text=TRANSLATIONS[current_language]["theme_label"], font=("Segoe UI", 8))
    theme_frame.place(relx=0.97, rely=0.97, anchor="se")

    theme_slider = tk.Scale(
        theme_frame,
        from_=0, to=1,
        orient=tk.HORIZONTAL,
        showvalue=0, length=50,
        command=lambda val: toggle_theme_by_slider(val),
        sliderrelief=tk.FLAT
    )
    theme_slider.pack(padx=5, pady=2)
    
    language_frame = tk.LabelFrame(root, text=TRANSLATIONS[current_language]["language_label"], font=("Segoe UI", 8))
    language_frame.place(relx=0.03, rely=0.97, anchor="sw")

    lang_labels = tk.Label(language_frame, text=TRANSLATIONS[current_language]["lang_labels"])
    lang_labels.pack()

    language_slider = tk.Scale(
        language_frame,
        from_=0, to=1,
        orient=tk.HORIZONTAL,
        showvalue=0, length=50,
        command=lambda val: toggle_language_by_slider(val),
        sliderrelief=tk.FLAT
    )
    language_slider.set(0) # Inicializa o slider para 'pt'
    language_slider.pack(padx=5, pady=2)

    apply_theme(THEMES["light"])
    atualizar_previsao()
    root.mainloop()

if __name__ == "__main__":
    try:
        run_gui()
    except Exception as e:
        print(f"Ocorreu um erro fatal: {e}")