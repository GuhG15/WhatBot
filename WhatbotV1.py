import os
import sys
import pandas as pd
import pywhatkit
import webbrowser
import pyautogui as pg
import time
from customtkinter import *
from PIL import Image
from tkinter import filedialog

# Função para obter o caminho do recurso


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Base Janela
janela = CTk()
janela.geometry("1231x674")
set_appearance_mode('dark')
janela.title('WhatBot')

texto = ''
data_frame = ''
file_path = ''
image_path = ''
time_msg = ''
time_image = ''
menu = ''
data_file = 'data.csv'


def carregar_numeros():
    if os.path.exists(data_file):
        try:
            df = pd.read_csv(data_file)
            if 'tempo_img' in df.columns and 'tempo_msg' in df.columns:
                tempo_img = df.loc[0, 'tempo_img']
                tempo_msg = df.loc[0, 'tempo_msg']
                return tempo_img, tempo_msg
            else:
                print("Colunas 'tempo_img' e 'tempo_msg' não encontradas no CSV.")
        except Exception as e:
            print(f"Erro ao ler o arquivo CSV: {e}")


tempo_img, tempo_msg = carregar_numeros()


def boot_whats():
    webbrowser.open('https://web.whatsapp.com/')
    time.sleep(6)
    pg.hotkey('alt', 'tab')


def open_file_explorer():
    global data_frame
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            data_frame = pd.read_csv(file_path, sep=';', encoding='latin-1')
            if 'Numero' not in data_frame.columns:
                raise ValueError(
                    "O arquivo CSV deve conter as coluna 'Numero'.")
            data_frame['Numero'] = '+' + data_frame['Numero'].astype(str)
            data_clientes.insert(0.0, file_path)
        except Exception as e:
            print(f"Erro ao abrir o arquivo: {e}")


def open_file_explorer_midia():
    global image_path
    image_path = filedialog.askopenfilename()
    if image_path:
        data_images.insert(0.0, image_path)


def get_msg():
    global texto
    texto = msg.get(0.0, 'end')


def envia_msg():
    global texto
    global data_frame
    global menu
    global tempo_img
    global tempo_msg
    for index, row in data_frame.iterrows():
        nome = row['Nome']
        numero = row['Numero']
        valor = row['Valor']
        if pd.isna(nome) or pd.isna(numero):
            print(f"Dados ausentes na linha {index + 1}")
            continue

        mensagem = texto.format(nome=nome, valor=valor)

        if check_var.get() == 'on':
            try:
                pywhatkit.sendwhats_image(receiver=numero,
                                          img_path=image_path,
                                          caption=mensagem,
                                          wait_time=tempo_img)
                time.sleep(2)
                pg.hotkey('ctrl', 'w')
            except Exception as e:
                print(f"Erro ao enviar mensagem para {nome} ({numero}): {e}")
        else:
            try:
                pywhatkit.sendwhatmsg_instantly(numero, mensagem, tempo_msg)
                time.sleep(2)
                pg.hotkey('ctrl', 'w')
            except Exception as e:
                print(f"Erro ao enviar mensagem para {nome} ({numero}): {e}")


def open_menu():
    global time_msg
    global time_img
    global menu
    global tempo_img
    global tempo_msg
    menu = CTkFrame(master=janela,
                    width=300,
                    height=490,
                    fg_color='#28282B',
                    border_color='white',
                    border_width=1
                    )
    botao_save = CTkButton(master=menu,
                           width=100, height=40,
                           text='Save',
                           corner_radius=8,
                           border_width=3,
                           fg_color='transparent',
                           border_color='#FFFFFF',
                           hover_color='#224362',
                           font=('Arial', 10 * -1),
                           command=set_time)
    botao_save.place(x=100, y=440)

    time_img = CTkTextbox(master=menu, width=100, height=36,
                          fg_color="white",
                          text_color='black',
                          corner_radius=8,)
    time_img.place(x=150, y=40)

    time_msg = CTkTextbox(master=menu, width=100, height=36,
                          fg_color="white",
                          text_color='black',
                          corner_radius=8,)
    time_msg.place(x=150, y=100)

    ind_msg = CTkLabel(master=menu, text='Tempo segundos Img',
                       font=('Arial_bold', 12 * -1),
                       fg_color='transparent',
                       bg_color='transparent')
    ind_msg.place(x=17, y=44)

    ind_image = CTkLabel(master=menu, text='Tempo segundos Msg',
                         font=('Arial_bold', 12 * -1),
                         fg_color='transparent',
                         bg_color='transparent')
    ind_image.place(x=17, y=105)
    menu.pack()
    menu.place(x=872, y=120)


def combina_botoes():
    get_msg()
    envia_msg()


def set_time():
    global tempo_img
    global tempo_msg
    global time_msg
    global time_img
    global menu
    tempo_img = int(time_img.get(0.0, 'end'))
    tempo_msg = int(time_msg.get(0.0, 'end'))
    data = pd.DataFrame({'tempo_img': [tempo_img], 'tempo_msg': [tempo_msg]})
    data.to_csv(data_file, index=False)
    menu.destroy()


# Botoes
boot_img = Image.open(resource_path(
    'images/refresh_24dp_FILL0_wght400_GRAD0_opsz24.png'))
whats_boot_button = CTkButton(master=janela,
                              width=50,
                              height=50,
                              text='',
                              corner_radius=8,
                              border_width=3,
                              fg_color='transparent',
                              border_color='#FFFFFF',
                              hover_color='#224362',
                              image=CTkImage(boot_img),
                              command=boot_whats)
whats_boot_button.place(x=1050, y=55)

menu_img = Image.open(resource_path(
    'images/menu_24dp_FILL0_wght400_GRAD0_opsz24.png'))
menu_button = CTkButton(master=janela, width=50,
                        height=50,
                        text='',
                        corner_radius=8,
                        border_width=3,
                        fg_color='transparent',
                        border_color='#FFFFFF',
                        hover_color='#224362',
                        image=CTkImage(menu_img),
                        command=open_menu)
menu_button.place(x=1120, y=55)

send_msg = CTkButton(master=janela, width=572, height=50,
                     text='Enviar Mensagem',
                     corner_radius=8,
                     border_width=3,
                     fg_color='transparent',
                     border_color='#FFFFFF',
                     hover_color='#224362',
                     font=('Arial', 15 * -1),
                     command=combina_botoes)
send_msg.place(x=600, y=560)

search_button_1 = CTkButton(master=janela, width=100, height=40,
                            text='Buscar',
                            corner_radius=8,
                            border_width=3,
                            fg_color='transparent',
                            border_color='#FFFFFF',
                            hover_color='#224362',
                            font=('Arial', 10 * -1),
                            command=open_file_explorer)
search_button_1.place(x=420, y=150)

search_button_2 = CTkButton(master=janela, width=100, height=40,
                            text='Buscar',
                            corner_radius=8,
                            border_width=3,
                            fg_color='transparent',
                            border_color='#FFFFFF',
                            hover_color='#224362',
                            font=('Arial', 10 * -1),
                            command=open_file_explorer_midia)
search_button_2.place(x=420, y=230)

# Checkbox IMg
check_var = StringVar(value='off')
send_img = CTkCheckBox(master=janela,
                       text='Enviar Imagem',
                       variable=check_var,
                       onvalue='on',
                       offvalue='off')
send_img.place(x=60, y=300)

# Textos
# Logos
logo = Image.open(resource_path(
    'images/precision_manufacturing_24dp_FILL0_wght400_GRAD0_opsz24.png'))
title_app = CTkLabel(master=janela,
                     text='WhatBot',
                     font=("Arial", 64 * -1))
title_app.place(x=135, y=50)

version_app = CTkLabel(master=janela, text='Version: 1.0',
                       font=('Arial', 10 * -1),
                       fg_color='transparent')
version_app.place(x=420, y=90)

label_image = CTkLabel(master=janela, text='',
                       fg_color='transparent',
                       image=CTkImage(logo, size=(63, 63)))
label_image.place(x=60, y=55)

macaw_inc = CTkLabel(master=janela,
                     text='Powered by: Macaw_inc',
                     font=('Arial', 10 * -1),
                     fg_color='transparent',
                     text_color='#141E28')
macaw_inc.place(x=80, y=600)

# Caixa de texto
# Inserir dados
msg = CTkTextbox(master=janela, width=572, height=401,
                 corner_radius=12,
                 fg_color="white",
                 text_color='black',
                 border_spacing=10,)
msg.place(x=600, y=150)

# Dados
data_clientes = CTkTextbox(master=janela, width=328, height=36,
                           fg_color="white",
                           text_color='black',
                           corner_radius=8,)
data_clientes.place(x=60, y=152)
data_images = CTkTextbox(master=janela, width=328, height=36,
                         fg_color="white",
                         text_color='black',
                         corner_radius=8,)
data_images.place(x=60, y=232)

# manter janela aberta
janela.mainloop()
