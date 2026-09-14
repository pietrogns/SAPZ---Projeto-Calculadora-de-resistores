import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

janela = tk.Tk()
janela.geometry("550x450")
janela.config(bg="aliceblue") # Fundo azul claro da janela
janela.title("Calculadora de Resistor")

estilo = ttk.Style()
estilo.theme_use('clam')

CORES = {
    "Preto":    {"digito":0, "multi": 1, "cor":"#000000"},
    "Marrom":   {"digito":1, "multi":10, "cor":"#A52A2A"},
    "Vermelho": {"digito":2, "multi":100, "cor":"#FF0000"},
    "Laranja":  {"digito":3, "multi":1000, "cor":"#FF8C00"},
    "Amarelo":  {"digito":4, "multi":10000, "cor":"#FFA500"},
    "Verde":    {"digito":5, "multi":100000, "cor":"#008000"},    
    "Azul":     {"digito":6, "multi":1000000, "cor":"#0000FF" },
    "Violeta":  {"digito":7, "multi":10000000, "cor":"#8A2BE2"},
    "Cinza":    {"digito":8, "multi":None, "cor":"#808080"},
    "Branco":   {"digito":9, "multi":None, "cor":"#FFFFFF"},
    "Ouro":     {"digito":None,"multi":0.1,"cor":"#D4AF37" },
    "Prata":    {"digito":None,"multi":0.01,"cor":"#C0C0C0"}
}
TOLERANCIA = {
    "Marrom": ("#A52A2A", "±1%"),
    "Vermelho":("#FF0000","±2%"),
    "Ouro": ("#D4AF37","±5%"),
    "Prata": ("#C0C0C0","±10%")
}

# Listas de valores para as Comboboxes
NOMES_DIGITO = [nome for nome, info in CORES.items() if info["digito"] is not None]
NOMES_MULTI = [nome for nome, info in CORES.items() if info["multi"] is not None]
NOMES_TOLERANCIA = list(TOLERANCIA.keys())

def modo_cores():
    opcao = modo_var.get()
    
    if opcao == "cores":
        frame_valor_cor.pack_forget()
        # fill="x" faz o frame se esticar para preencher o espaço horizontal
        frame_cor_valor.pack(after=frame_modo, pady=10, fill="x") 
        
    elif opcao == "valor":
        frame_cor_valor.pack_forget()
        frame_valor_cor.pack(after=frame_modo, pady=10, fill="x")

def botao_calcular():
    messagebox.showinfo("Informação", "Você clicou no botão!")

# --------- Título Principal ---------
# Aplicamos a mesma cor do fundo da janela (aliceblue) para ele se mesclar
label_titulo = tk.Label(janela, text="Calculadora de Resistor", anchor="n", bg="aliceblue", fg="#1a3b5c", font=("Arial", 16, "bold"))
label_titulo.pack(pady=(15, 10), anchor="w", padx=20)

# --------- Container Branco Central ---------
# Este Frame branco simula o quadro que existe na imagem
frame_principal = tk.Frame(janela, bg="white", padx=20, pady=20)
frame_principal.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# Texto guia
tk.Label(frame_principal, text="Como deseja informar o resistor?", bg="white", font=("Arial", 10, "bold"), fg="#111111").pack(anchor="w", pady=(0, 5))

# Opções de modos
frame_modo = tk.Frame(frame_principal, bg="white")
frame_modo.pack(fill="x", pady=5)
modo_var = tk.StringVar(value="cores") 

tk.Radiobutton(frame_modo, text="Valor da resistência", variable=modo_var, value="valor", bg="#e8e8e8", font=("Arial", 9), command=modo_cores).pack(side="left", padx=(0, 10))
tk.Radiobutton(frame_modo, text="Cores do resistor", variable=modo_var, value="cores", bg="#e8e8e8", font=("Arial", 9), command=modo_cores).pack(side="left", padx=5)


# --------- Frame: Seleção de Cores ---------
frame_cor_valor = tk.Frame(frame_principal, bg="white")

# Faixa 1
tk.Label(frame_cor_valor, text="Banda 1:", bg="white").grid(row=0, column=0, padx=(0, 5), sticky="w")
faixa1_combo = ttk.Combobox(frame_cor_valor, values=NOMES_DIGITO, state="readonly", width=12)
faixa1_combo.grid(row=1, column=0, padx=(0, 5), pady=5)

# Faixa 2
tk.Label(frame_cor_valor, text="Banda 2:", bg="white").grid(row=0, column=1, padx=5, sticky="w")
faixa2_combo = ttk.Combobox(frame_cor_valor, values=NOMES_DIGITO, state="readonly", width=12)
faixa2_combo.grid(row=1, column=1, padx=5, pady=5)

# Multiplicador
tk.Label(frame_cor_valor, text="Multiplicador:", bg="white").grid(row=0, column=2, padx=5, sticky="w")
faixa3_combo = ttk.Combobox(frame_cor_valor, values=NOMES_MULTI, state="readonly", width=12)
faixa3_combo.grid(row=1, column=2, padx=5, pady=5)

# Tolerância
tk.Label(frame_cor_valor, text="Tolerância:", bg="white").grid(row=0, column=3, padx=5, sticky="w")
faixa4_combo = ttk.Combobox(frame_cor_valor, values=NOMES_TOLERANCIA, state="readonly", width=12)
faixa4_combo.grid(row=1, column=3, padx=5, pady=5)


# --------- Frame: Valor da Resistência ---------
frame_valor_cor = tk.Frame(frame_principal, bg="white")

tk.Label(frame_valor_cor, text="Valor da Resistência (Ω):", bg="white").grid(row=0, column=0, padx=(0, 5), sticky="w")
entry_resis = tk.Entry(frame_valor_cor, width=15)
entry_resis.grid(row=1, column=0, padx=(0, 5), pady=5)

tk.Label(frame_valor_cor, text="Tolerância:", bg="white").grid(row=0, column=1, padx=5, sticky="w")
toler_combo = ttk.Combobox(frame_valor_cor, values=NOMES_TOLERANCIA, state="readonly", width=13)
toler_combo.grid(row=1, column=1, padx=5, pady=5)


# --------- Botão para calcular ---------
botton_calcular = tk.Button(
    frame_principal, 
    text="Calcular resistência", 
    bg="#359f8b", # Verde-água da imagem
    fg="white", 
    font=("Arial", 10, "bold"), 
    relief="flat", 
    padx=10, 
    pady=5, 
    command=botao_calcular
)
botton_calcular.pack(anchor="w", pady=(15, 0))

# Força o programa a organizar a tela e mostrar apenas a opção que está pré-selecionada no início
modo_cores()

janela.mainloop()