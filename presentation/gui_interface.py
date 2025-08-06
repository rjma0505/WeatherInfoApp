import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta

# --- As suas importações originais, para carregar todas as cidades ---
from logic.controller import fetch_forecast_by_city_name
from data_access.ipma_api import listar_cidades
# ---------------------------------------------------------------------

# Mapeamento de descrição para nomes de ficheiros de ícones
ICON_MAP = {
    "Clear sky": "clear.png",
    "Partly cloudy": "partly_cloudy.png",
    "Cloudy": "cloudy.png",
    "Rain": "rain.png",
    "Heavy rain": "heavy_rain.png",
    "Showers": "showers.png",
    "Thunderstorm": "storm.png"
}

ICON_FOLDER = os.path.join("assets", "weather_icons")

DIAS_SEMANA = ("Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo")

# Definição das paletas de cores para os temas
THEMES = {
    "light": {
        "bg": "#F0F0F0",
        "fg": "#000000",
        "fg_muted": "#505050", # Cinzento para texto menos importante
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
        "fg_muted": "#A0A0A0", # Cinzento claro para texto menos importante
        "btn_bg": "#555555",
        "btn_fg": "#FFFFFF",
        "special_btn_bg": "#2A722A",
        "special_btn_fg": "white",
        "combo_bg": "#3C3C3C",
        "combo_fg": "#FFFFFF",
        "slider_trough": "#444444"
    }
}

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

def run_gui():
    root = tk.Tk()
    root.title("Previsão do Tempo")
    root.geometry("400x500")
    root.minsize(400, 500) # Evita que a janela fique pequena demais

    style = ttk.Style(root)
    
    global current_theme_name
    current_theme_name = "light"

    title_label = tk.Label(root, text="Previsão do Tempo", font=("Helvetica", 16, "bold"))
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

    def atualizar_previsao():
        nonlocal forecast_data
        cidade = selected_city.get()
        try:
            forecast_data = fetch_forecast_by_city_name(cidade)
        except Exception as e:
            messagebox.showerror("Erro de Rede", f"Não foi possível contactar o servidor: {e}")
            forecast_data = []
            return

        if not forecast_data:
            messagebox.showerror("Erro", "Não foi possível obter a previsão.")
            return

        day_index.set(0)
        mostrar_dia()

    def mostrar_dia():
        if not forecast_data: return
        index = day_index.get()
        if index >= len(forecast_data): return

        dia = forecast_data[index]
        data_formatada = dia["date"]
        hoje = datetime.now().date()
        data_dia = datetime.strptime(data_formatada, "%Y-%m-%d").date()

        if data_dia == hoje: prefixo = "Hoje"
        elif data_dia == hoje + timedelta(days=1): prefixo = "Amanhã"
        else:
            dia_da_semana_idx = data_dia.weekday()
            prefixo = DIAS_SEMANA[dia_da_semana_idx]

        texto = f"{prefixo} ({data_formatada}):\n{dia['weather_description']} - Min: {dia['tMin']}°C | Max: {dia['tMax']}°C"
        forecast_label.config(text=texto)

        icon = get_icon_image(dia["weather_description"])
        if icon:
            icon_label.config(image=icon)
            icon_label.image = icon

    nav_frame = tk.Frame(root)
    nav_frame.pack(pady=10)

    btn_anterior = tk.Button(nav_frame, text="← Dia anterior", command=lambda: (day_index.set(day_index.get() - 1), mostrar_dia()) if day_index.get() > 0 else None)
    btn_anterior.grid(row=0, column=0, padx=5)

    btn_seguinte = tk.Button(nav_frame, text="Dia seguinte →", command=lambda: (day_index.set(day_index.get() + 1), mostrar_dia()) if forecast_data and day_index.get() < len(forecast_data) - 1 else None)
    btn_seguinte.grid(row=0, column=1, padx=5)

    botao = tk.Button(root, text="Ver Previsão", command=atualizar_previsao, padx=10, pady=5)
    botao.pack(pady=10)

    # --- NOVO: Rótulo de Copyright ---
    # O f-string com o símbolo © e o ano automático dá um ar mais profissional
    copyright_text = f"WeatherInfoApp © {datetime.now().year}"
    copyright_label = tk.Label(root, text=copyright_text, font=("Segoe UI", 8))
    copyright_label.pack(side=tk.BOTTOM, pady=5)

    # --- NOVO: Frame para o slider de tema ---
    theme_frame = tk.LabelFrame(root, text="Tema", font=("Segoe UI", 8))
    theme_frame.place(relx=0.97, rely=0.97, anchor="se") # Canto inferior direito

    theme_slider = tk.Scale(
        theme_frame, # Colocado dentro da nova frame
        from_=0, to=1,
        orient=tk.HORIZONTAL,
        showvalue=0, length=50,
        command=lambda val: toggle_theme_by_slider(val),
        sliderrelief=tk.FLAT
    )
    theme_slider.pack(padx=5, pady=2)
    
    def apply_theme(theme):
        root.config(bg=theme["bg"])
        nav_frame.config(bg=theme["bg"])
        title_label.config(bg=theme["bg"], fg=theme["fg"])
        forecast_label.config(bg=theme["bg"], fg=theme["fg"])
        icon_label.config(bg=theme["bg"])
        
        style.configure("TCombobox", fieldbackground=theme["combo_bg"], foreground=theme["combo_fg"])
        
        btn_anterior.config(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_bg"], activeforeground=theme["btn_fg"], highlightbackground=theme["bg"])
        btn_seguinte.config(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_bg"], activeforeground=theme["btn_fg"], highlightbackground=theme["bg"])
        botao.config(bg=theme["special_btn_bg"], fg=theme["special_btn_fg"], activebackground=theme["special_btn_bg"], activeforeground=theme["special_btn_fg"], highlightbackground=theme["bg"])

        # Aplicar tema aos novos widgets
        copyright_label.config(bg=theme["bg"], fg=theme["fg_muted"])
        theme_frame.config(bg=theme["bg"], fg=theme["fg"])
        theme_slider.config(bg=theme["bg"], troughcolor=theme["slider_trough"])

    def toggle_theme_by_slider(slider_value):
        global current_theme_name
        value = int(float(slider_value))
        target_theme = "dark" if value == 1 else "light"
        
        if target_theme != current_theme_name:
            current_theme_name = target_theme
            apply_theme(THEMES[current_theme_name])

    apply_theme(THEMES["light"])
    atualizar_previsao()
    root.mainloop()

if __name__ == "__main__":
    try:
        run_gui()
    except Exception as e:
        print(f"Ocorreu um erro fatal: {e}")