import PySimpleGUI as sg
import telebot
from datetime import datetime, timedelta
import base64
import json

#Campo imagens
imaged_base64 = "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"
image_data = base64.b64decode(imaged_base64)

#bot utilizado para enviar informações @poyrgonBot
bot = telebot.TeleBot("6753364989:AAExMXbBXOw_ndp8Qqay_MExyo45k3Atjzw")
print(f'Rodando..{bot}')
#chat_id = '5899515567' #meu chat id
#para mais um id, faça uma lista com os ids para fazer o envio


#função para achar o último dia utio do mês.
def obter_dia_util_anterior():
    data_atual = datetime.now()
    um_dia = timedelta(days=1)
    
    # Subtrair um dia inicialmente
    data_anterior = data_atual - um_dia
    
    # Verificar se o dia anterior é sábado (5) ou domingo (6)
    while data_anterior.weekday() >= 5:  # 5 = sábado, 6 = domingo
        data_anterior -= um_dia  # Subtrair mais um dia
    
    return data_anterior

#Verificar se dentro das caixas de texto contem apenas números
def verificar_somente_numeros(string):
    for char in string:
        if not char.isdigit():
            raise ValueError(f"Caractere inválido detectado: '{char}'")

#calcular quantidade de unidades com somatorio
def calcular_soma(valores):
    try:
        
        if '-' in valores:
            partes2 = valores.split('-')
            resultado = float(partes2[0])
            for parte in partes2[1:]:
                resultado -= float(parte)
            return resultado

        # Divide os valores pelo sinal '+'
        partes = valores.split('+')
  
        # Converte para float e soma os valores
        resultado = sum(float(parte) for parte in partes)
        return resultado
    except ValueError:
        return 'Expressão inválida!!!'

#Criar os dados no banco de dados em json, sendo assim salvando o id do usuario 
def load_data(filename='data.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

#área de salvamento de ID, outro layout para salvamentoo
def salvando_id():
    def save_data(data, filename='data.json'):
        with open(filename, 'w') as file:
            json.dump(data, file)

    sg.theme('DarkBlue1')
    layout4 = [
        [sg.Text(size=(0,1))],
        #[sg.Text('ID Telegram'), sg.InputText(size=(12,2),key='ID',text_color='white',background_color='brown')],
        [sg.Column([[sg.Text('ID Telegram'), sg.InputText(size=(12,2),key='ID',text_color='white',background_color='brown')]],justification='center')],
        [sg.Text(size=(0,1))],
        [sg.Column([[sg.Button('Salvar'), sg.Button('Carregar'), sg.Button('Sair')]],justification='center')]]

    window = sg.Window('Meu ID', layout4,size=(235,154))
    window.finalize()
    
    #Carregar dados existentes ao iniciar o programa
    data = load_data()
    if data:
        window['ID'].update(data.get('id', ''))
        

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if event == 'Salvar':
            # Salvar os dados inseridos
            data = {
                'id': values['ID']
            }
            save_data(data)
            sg.popup_no_buttons('\nDados salvos com sucesso!\n',no_titlebar=True,auto_close=True,auto_close_duration=0.5,background_color='blue')
            
        if event == 'Carregar':
            # Carregar os dados salvos
            data = load_data()
            window['ID'].update(data.get('id', ''))
            sg.popup_no_buttons('\nDados carregados com sucesso!\n',no_titlebar=True,auto_close=True,auto_close_duration=0.5,background_color='green',)

    window.close()

sg.theme('DarkBlue1')
#layout 1
layout1 = [
    [sg.Text('')],
    [sg.Text('Matriz de Produtividade FARMA',size=(0,0))],
    [sg.Text('QTD Unidade:',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='unidade1',)],
    [sg.Text('QTD Caixa Fechada:',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='caixa1')],
    [sg.Text('GAP Faturamento:',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='gap1')],
    [sg.Text('Recebimento (volumes):',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='volume1')],
    [sg.Text('Recebimento (unidades):',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='recebimento_unidade1')],
    [sg.Text('SKUs excluidos:',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='sku1')],
    [sg.Text('% Fracionado:')], 
    [sg.Text('')]]

#Layout 2
layout2 = [
    [sg.Text('')],
    [sg.Text('Matriz de Produtividade HB',size=(0,0))],
    [sg.Text('QTD Unidade:',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='unidade2')],
    [sg.Text('QTD Caixa Fechada:',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='caixa2')],
    [sg.Text('GAP Faturamento:',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='gap2')],
    [sg.Text('Recebimento (volumes):',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='volume2')],
    [sg.Text('Recebimento (unidades):',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='recebimento_unidade2')],
    [sg.Text('SKUs excluidos:',size=(18,0)), sg.InputText('',text_color='white',background_color='brown',size=(12,2),key='sku2')],
    [sg.Text('% Fracionado:')], 
    [sg.Text('')]]

#interface bot-comands

menu_def = [['&Sobre', ['QTD Unidade?','QTD Caixa Fechada?','GAP de Faturamento?','Recebimento Volumes?','Recebimento Unidades?','SKUs excluidos?','% Fracionado?']],['Meu ID',['ID']]]
#Layout 3, principal
layout3 = [
    [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
    [sg.Column(layout1),sg.Column(layout2)],
    [sg.Button('Matriz',font='Arial',size=(10,1),button_color=('white', 'blue'),key='enter')]
]


# Crie a janela
window = sg.Window('MATRIZ', layout3)
window.finalize()
kays_texto = ['unidade1','unidade2','caixa1','caixa2','gap1','gap2','volume1','volume2','recebimento_unidade1','recebimento_unidade2','sku1','sku2']
#mudar cursor para branco,.
for keys in kays_texto:
    input_element = window[keys].Widget
    input_element.config(insertbackground='white')

#Loop de eventos para processar eventos e obter os valores das entradas
while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED:  # Correção de sg.WIN_CLOSED() para sg.WIN_CLOSED
        break
    #popups do aba Menu
    if event == 'QTD Unidade?':
        sg.popup_no_border('Quantidade de unidades faturadas que passaram pela conferência.\n',background_color='red',font=('Segoe UI',12))
    if event == 'QTD Caixa Fechada?':
        sg.popup_no_border('Quantidade de unidades faturadas (caixa fechada).\n',background_color='red',font=('Segoe UI',12))
    if event == 'Recebimento Volumes?':
        sg.popup_no_border('Quantidade de volumes que chegaram ao recebimento no dia em questão.\nSolicitar ao setor do recebimento a quantidade correta.\n',background_color='red',font=('Segoe UI',12))
    if event == 'GAP de Faturamento?':
        sg.popup_no_border('Unidades que não foram faturadas no dia anterior.\n',background_color='red',font=('Segoe UI',12))
    if event == 'Recebimento Unidades?':
        sg.popup_no_border('Consultar no sistema a quantidade de unidades.\nObs.: O campo "Recebimento (unidades)" aceita operações matemáticas (+) e (-).\nEx = 1+1\n',background_color='red',font=('Segoe UI',12))
    if event == '% Fracionado?':
        sg.popup_no_border('', image=image_data,background_color='red' )
    if event == 'SKUs excluidos?':
        sg.popup_no_border('Produtos "zerados" durante a conferência.\n',background_color='red',font=('Segoe UI',12))
    
    #Em desenvolvimento
    if event =='ID':
        salvando_id()
        
    #evento principal mediante a entrada de valores dentro co compo unidades 
    if event == 'enter':
        try:
            verificar_somente_numeros(values['unidade1'])
            verificar_somente_numeros(values['unidade2'])
            verificar_somente_numeros(values['caixa1'])
            verificar_somente_numeros(values['caixa2'])
            verificar_somente_numeros(values['gap1'])
            verificar_somente_numeros(values['gap2'])
            verificar_somente_numeros(values['volume1'])
            verificar_somente_numeros(values['volume2'])
            #verificar_somente_numeros(values['recebimento_unidade1'])
            #verificar_somente_numeros(values['recebimento_unidade2'])
            verificar_somente_numeros(values['sku1'])
            verificar_somente_numeros(values['sku2'])
            
            
            if values['unidade1'] > '0':
                    
                    resultado = calcular_soma(values['recebimento_unidade1'])
                    resultado2 = calcular_soma(values['recebimento_unidade2'])
                    dia_util_anterior = obter_dia_util_anterior()
                    
                    dia_anterior = dia_util_anterior.day
                    mes_anterior = dia_util_anterior.month

                    # Formatando para dois dígitos com preenchimento de zero à esquerda se necessário
                    dia_formatado = f"{dia_anterior:02}"  # Formato "02" garante dois dígitos
                    mes_formatado = f"{mes_anterior:02}"
                    
                    # Função para enviar mensagem de texto
                    def send_message(text):
                        
                        #O bot vai enviar msg para meu chat id mesmo não inserindo o valor do id do usuario
                        alecio_id = '5899515567'
                        ddte = load_data()
                        transs = [alecio_id,f'{ddte.get('id','')}']
                        
                        if len(transs) > 1 and  transs[1]:
                            print('Valor_ID_válido!')
                            for chet in transs:
                                bot.send_message(chet, text)
                        else:
                            bot.send_message(alecio_id,text)
                            print('Valor_do_ID_inválido!!')
                            pass

                    def formatar_numero(numero):
                        return f"{int(numero):,}".replace(",", ".")
               
                    mensagem_codif = (f"*CD NAZÁRIA IMPERATRIZ FARMA - DIA {dia_formatado}/{mes_formatado}*\n"
                                f"- Unidades Faturadas: {formatar_numero(int(values['unidade1'])+int(values['caixa1']))}\n"
                                f"- GAP de faturamento: {formatar_numero(values['gap1'])}\n"
                                f"- Recebimento (volumes): {formatar_numero(values['volume1'])}\n"
                                f"- Recebimento (unidades): {formatar_numero(resultado)}\n"
                                f"- SKUs excluidos: {formatar_numero(values['sku1'])}\n"
                                f"- % Fracionado: {((int(values['unidade1'])) / (int(values['unidade1']) + int(values['caixa1']))):.2f}"
                                "\n\n"
                                "*MATRIZ DE PRODUTIVIDADE*"
                                "\n\n"
                                f"*CD NAZÁRIA IMPERATRIZ HB - DIA {dia_formatado}/{mes_formatado}*\n"
                                f"- Unidades Faturadas: {formatar_numero(int(values['unidade2'])+int(values['caixa2']))}\n"
                                f"- GAP de faturamento: {formatar_numero(values['gap2'])}\n"
                                f"- Recebimento (volumes): {formatar_numero(values['volume2'])}\n"
                                f"- Recebimento (unidades): {formatar_numero(resultado2)}\n"
                                f"- SKUs excluidos: {formatar_numero(values['sku2'])}\n"
                                f"- % Fracionado: {((int(values['unidade2'])) / (int(values['unidade2']) + int(values['caixa2']))):.2f}")

                    send_message(mensagem_codif)
                    sg.popup_scrolled((mensagem_codif), title='Relatório CD Nazária', size=(60, 20), font=('Courier', 13),background_color='black',text_color='white')
        except ValueError as e:
            sg.popup_error(f'{e}')
                            
    
       
window.close()







