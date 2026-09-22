import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Canvas
from tkinter import messagebox

janela = Tk()
janela.geometry("500x400")
janela.config(bg="aliceblue")
janela.title("Calculadora de resistor")
janela.resizable(False, False)

estilo = ttk.Style()
estilo.theme_use('clam')

# ---------------------------------------------------------
#Dicionarios
# ---------------------------------------------------------

# Listas simples com os nomes para preencher as Comboboxes
NOMES_DIGITO = ["Preto", "Marrom", "Vermelho", "Laranja", "Amarelo", "Verde", "Azul", "Violeta", "Cinza", "Branco"]
NOMES_MULTI = ["Preto", "Marrom", "Vermelho", "Laranja", "Amarelo", "Verde", "Azul", "Violeta", "Ouro", "Prata"]
NOMES_TOLERANCIA = ["Marrom", "Vermelho", "Ouro", "Prata"]

# Dicionário 1: Para achar o número do dígito através da cor
valor_do_digito = {
    "Preto": 0, "Marrom": 1, "Vermelho": 2, "Laranja": 3, "Amarelo": 4, 
    "Verde": 5, "Azul": 6, "Violeta": 7, "Cinza": 8, "Branco": 9
}

# Dicionário 2: Para achar o multiplicador através da cor
valor_do_multiplicador = {
    "Preto": 1, "Marrom": 10, "Vermelho": 100, "Laranja": 1000, 
    "Amarelo": 10000, "Verde": 100000, "Azul": 1000000, "Violeta": 10000000, 
    "Ouro": 0.1, "Prata": 0.01
}

# Dicionários Inversos: Para achar a cor através do número
cor_do_digito = {
    0: "Preto", 1: "Marrom", 2: "Vermelho", 3: "Laranja", 4: "Amarelo", 
    5: "Verde", 6: "Azul", 7: "Violeta", 8: "Cinza", 9: "Branco"
}
cor_do_multiplicador = {
    1: "Preto", 10: "Marrom", 100: "Vermelho", 1000: "Laranja", 
    10000: "Amarelo", 100000: "Verde", 1000000: "Azul", 10000000: "Violeta",
    0.1: "Ouro", 0.01: "Prata"
}

# Dicionários de Textos e Cores (Visual)
texto_da_tolerancia = {"Marrom": "±1%", "Vermelho": "±2%", "Ouro": "±5%", "Prata": "±10%"}
cor_hexadecimal = {
    "Preto": "#000000", "Marrom": "#A52A2A", "Vermelho": "#FF0000", "Laranja": "#FF8C00", 
    "Amarelo": "#FFA500", "Verde": "#008000", "Azul": "#0000FF", "Violeta": "#8A2BE2", 
    "Cinza": "#808080", "Branco": "#FFFFFF", "Ouro": "#D4AF37", "Prata": "#C0C0C0"
}


# ---------------------------------------------------------
# 2. FUNÇÕES COM LÓGICA PASSO A PASSO
# ---------------------------------------------------------

def formatacao_valor(ohms):
    if ohms >= 1_000_000:
        conta = ohms / 1_000_000
        return f"{conta:.2f} MΩ"
    elif ohms >= 1_000:
        conta = ohms / 1_000
        return f"{conta:.2f} kΩ"
    else:
        return f"{ohms:.2f} Ω"


def troca_de_opcao():

    opcao = modo_var.get()
    #comando abaixo serve para limpar o texto do resultado toda vez q trocar de opção
    label_resultado.config(text="")
    
    if opcao == "cores":
        frame_valor_cor.pack_forget()
        frame_cor_valor.pack(after=frame_modo, pady=10)
        # Mostra o frame_cor_valor exatamente DEPOIS do frame_modo
    elif opcao == "valor":
         # Esconde o frame de cores
        frame_cor_valor.pack_forget()
        frame_valor_cor.pack(after=frame_modo, pady=10)


def cores_valor():
    # Pega os textos das caixinhas
    faixa1 = faixa1_combo.get()
    faixa2 = faixa2_combo.get()
    faixa3 = faixa3_combo.get()
    faixa4 = faixa4_combo.get()

    if not (faixa1 and faixa2 and faixa3 and faixa4):
        messagebox.showerror("Erro", "Por favor, selecione todas as cores.")
        return

    # Transforma texto em número usando os dicionários simples
    digito1 = valor_do_digito[faixa1]
    digito2 = valor_do_digito[faixa2]
    multiplicador = valor_do_multiplicador[faixa3]
    tolerancia = texto_da_tolerancia[faixa4]

    # Formula para calcular
    dezena = digito1 * 10
    numero_junto = dezena + digito2
    resistencia = numero_junto * multiplicador
    
    resistencia_formatada = formatacao_valor(resistencia)

    texto_final = f"Resultado:{resistencia_formatada} \ Tolerância: {tolerancia}"
    label_resultado.config(texto_final)
    # 5. Pinta o desenho
    canvas.itemconfig(desenho_faixa1, fill=cor_hexadecimal[faixa1])
    canvas.itemconfig(desenho_faixa2, fill=cor_hexadecimal[faixa2])
    canvas.itemconfig(desenho_faixa3, fill=cor_hexadecimal[faixa3])
    canvas.itemconfig(desenho_faixa4, fill=cor_hexadecimal[faixa4])

    # Esconde a caixa de espera e mostra o resistor pronto
    frame_espera.pack_forget()
    canvas.pack(pady=5)


def valor_cores():
    valor_str = entry_resis.get()
    tolerancia = toler_combo.get()
    
    if not valor_str or not tolerancia:
        messagebox.showerror("Erro", "Por favor, insira o valor da resistência e selecione a tolerância.")
        return

    try:
        valor_numero = float(valor_str)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        return

    # Transformar o número em texto para pegar as letras separadas
    numero_inteiro = int(valor_numero)
    texto_numero = str(numero_inteiro)

    # Pegando a primeira e segunda letra (dígitos)
    texto_d1 = texto_numero[0]
    texto_d2 = "0"
    if len(texto_numero) > 1:
        texto_d2 = texto_numero[1]

    digito1 = int(texto_d1)
    digito2 = int(texto_d2)

    # Calculando os zeros para o multiplicador
    if valor_numero < 10:
        multiplicador = 1
    else:
        quantidade_de_zeros = len(texto_numero) - 2
        multiplicador = 10 ** quantidade_de_zeros

    # Acha os nomes das cores usando os dicionários inversos
    faixa1_cor = cor_do_digito[digito1]
    faixa2_cor = cor_do_digito[digito2]
    faixa3_cor = cor_do_multiplicador[multiplicador]
    
    # Mensagem final
    texto_final = f"Cores: {faixa1_cor} - {faixa2_cor} - {faixa3_cor} \ Tolerância: {tolerancia}"
    label_resultado.config(text=texto_final)
    # Pinta o desenho
    canvas.itemconfig(desenho_faixa1, fill=cor_hexadecimal[faixa1_cor])
    canvas.itemconfig(desenho_faixa2, fill=cor_hexadecimal[faixa2_cor])
    canvas.itemconfig(desenho_faixa3, fill=cor_hexadecimal[faixa3_cor])
    canvas.itemconfig(desenho_faixa4, fill=cor_hexadecimal[tolerancia])

    # Esconde a caixa de espera e mostra o resistor pronto
    frame_espera.pack_forget()
    canvas.pack(pady=5)

#
def botao_calcular():
    opcao = modo_var.get()
    if opcao == "cores":
        cores_valor()
    elif opcao == "valor":
        valor_cores()


# ---------------------------------------------------------
# INTERFACE
# ---------------------------------------------------------

#  Título Principal
label_titulo = tk.Label(
    janela, 
    text="Calculadora de Resistor", 
    anchor="n",
    bg="aliceblue", 
    fg="#1a3b5c", 
    font=("Arial", 15, "bold")
)
label_titulo.pack(anchor= "w", padx=15, pady=10)

#   Frame Branco fundo
frame_principal = tk.Frame(
    janela, 
    bg="white", 
    padx=20, pady=5
)
frame_principal.pack(padx=10, pady=(0, 15))

#   Texto
tk.Label(
    frame_principal, 
    text="Como deseja informar o resistor?", 
    bg="white", 
    font=("Arial", 10,"bold")
).pack(anchor="w")

#   Opções de modos
frame_modo = tk.Frame(
    frame_principal,
      bg="white"
)
frame_modo.pack(fill="x", pady=5)

modo_var = tk.StringVar(value="cores") 

#   Botões das opções
cores_rdbtn = tk.Radiobutton(
    frame_modo, 
    text="Cores do resistor", 
    variable=modo_var, 
    value="cores", 
    bg="#e8e8e8", 
    font=("Arial", 9),
    command=troca_de_opcao).pack(side="left", padx=(0,10))
valor_rdbtn = tk.Radiobutton(
    frame_modo, 
    text="Valor da resistência", 
    variable=modo_var, 
    value="valor", 
    bg="#e8e8e8", 
    font=("Arial", 9),
    command=troca_de_opcao).pack(side="left", padx=5)

#   Frame para seleção de cores
frame_cor_valor = tk.Frame(frame_principal, bg="White")

#   Faixa 1
faixa1_txt = tk.Label(
    frame_cor_valor,
    text="Faixa 1:", 
    bg="white"
    )
faixa1_txt.grid(row=0, column=0, padx=5, sticky="w")
faixa1_combo = ttk.Combobox(
    frame_cor_valor, 
    values=NOMES_DIGITO, 
    state="readonly", 
    width=13
)
faixa1_combo.grid(row=1, column=0, padx=5, pady=5)

#   Faixa 2
faixa2_txt = tk.Label(
    frame_cor_valor, 
    text="Faixa 2:", 
    bg="white"
)
faixa2_txt.grid(row=0, column=1, padx=5, sticky="w")
faixa2_combo = ttk.Combobox(
    frame_cor_valor, 
    values=NOMES_DIGITO, 
    state="readonly",
    width=13
)
faixa2_combo.grid(row=1, column=1, padx=5, pady=5)

#   Multiplicador
faixa3_txt = tk.Label(
    frame_cor_valor, 
    text="Multiplicador:", 
    bg="white"
)
faixa3_txt.grid(row=0, column=2, padx=5, sticky="w")

faixa3_combo = ttk.Combobox(
    frame_cor_valor, 
    values=NOMES_MULTI, 
    state="readonly", 
    width=13
)
faixa3_combo.grid(row=1, column=2, padx=5, pady=5)

#   Tolerância
faixa4_txt = tk.Label(
    frame_cor_valor, 
    text="Tolerância:", 
    bg="white"
)
faixa4_txt.grid(row=0, column=3, padx=5, sticky="w")
faixa4_combo = ttk.Combobox(
    frame_cor_valor, 
    values=NOMES_TOLERANCIA, 
    state="readonly", 
    width=13
)
faixa4_combo.grid(row=1, column=3, padx=5, pady=5)

#       Frame Valor Resistência
frame_valor_cor = tk.Frame(frame_principal, bg="white")

valor_lbl = tk.Label(frame_valor_cor, text="Valor da Resistência (Ω)", bg="white")
valor_lbl.grid(row=0, column=0, padx=(0,5), sticky="w")

#entry onde o usuario vai por o número da resistência
entry_resis = tk.Entry(frame_valor_cor, width=15)
entry_resis.grid(row=1, column=0, padx=(0, 5), pady=5)


#opções de tolerância
toler_lbl = tk.Label(frame_valor_cor, text="Tolerância:", bg="white").grid(row=0, column=1, padx=5, sticky="w")
toler_combo = ttk.Combobox(frame_valor_cor, values=NOMES_TOLERANCIA,state="readonly", width=13)
toler_combo.grid(row=1, column=1, padx=5, pady=5)


#   Botão para calcular (Note que troquei o command para botao_calcular)
botton_calcular = tk.Button(
    frame_principal,
    text="Calcular resistência", 
    bg="gray", 
    fg="White", 
    font=("Arial", 9, "bold"),
    relief="groove",
    padx=10,
    pady=5,
    command=botao_calcular)
botton_calcular.pack(anchor="w", pady=5)

#label onde pede para o usuario digitar o valor
label_valor = tk.Label(
    frame_principal, 
    text="Digite o valor da resistência ou selecione as cores.", 
    font=("Arial", 9, "bold"), 
    bg="White").pack(anchor="w",pady=5)

# novo label
label_resultado = tk.Label(
    frame_principal, text="", font=("Arial", 11, "bold"), fg="#2e8b57", bg="White"
)
label_resultado.pack(anchor="w", pady=2)

# --- CAIXA DE ESPERA (ADICIONADA AQUI!) ---
frame_espera = tk.Frame(frame_principal, bg="white", highlightbackground="#d3d3d3", highlightthickness=1, width=400, height=130)
frame_espera.pack_propagate(False) 
texto_espera = tk.Label(frame_espera, text="Aguarde a seleção do modo", bg="white", fg="gray", font=("Arial", 10))
texto_espera.pack(expand=True)
frame_espera.pack(pady=5) # Ela começa visível na tela


#   Canvas onde o resistor vai ser desenhado
canvas = Canvas(frame_principal, width=400, height=150, bg="light gray")

base_resistor = canvas.create_rectangle(
    80,30, 300, 80,
    fill="#D2B48C",  # Cor do resistor
    outline="black",  # Cor da borda
)

#   Fios do resistor
fio_esquerdo = canvas.create_rectangle(20, 55, 80, 60, fill="gray")
fio_direito = canvas.create_rectangle(300, 55, 360, 60, fill="gray")

#   Faixas (Note que mudei os nomes para desenho_faixa1, etc.)
desenho_faixa1 = canvas.create_rectangle(120, 30, 135, 80, fill="#FF0000")
desenho_faixa2 = canvas.create_rectangle(150, 30, 165, 80, fill="#FF0000")
desenho_faixa3 = canvas.create_rectangle(180, 30, 195, 80, fill="#FF0000")
desenho_faixa4 = canvas.create_rectangle(220, 30, 238, 80, fill="#FF0000")

# Força a janela a iniciar arrumada
troca_de_opcao()
janela.mainloop()