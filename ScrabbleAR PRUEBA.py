import PySimpleGUI as sg
from random import choice
import m_buscador
import m_tablero
from m_fichas import valores_letras

puntos_jugador = 0
puntos_maquina = 0
AN = 4 # Este es el ancho de los botones
AL = 2 # Este es el alto de los botones
INICIO = (7,7)
filas = 15
cant_letras = 7
creando_letras = [['A']*11,['B']*3,['C']*4,['D']*4,['E']*11,['F']*2,['G']*2,['H']*2,['I']*6,['J']*2,['K']*2,['L']*4,['M']*3,['N']*5,
            ['Ñ']*2,['O']*8,['P']*2,['Q']*2,['R']*4,['S']*7,['T']*4,['U']*6,['V']*2,['W']*2,'X',['Y']*2,'Z']

Letras = [elem for sublist in creando_letras for elem in sublist] #hace que creando_letras sea una sola lista.

# El primer elemento de key es 999 para identificar que es una ficha de la maquina y que no pase nada si el jugador aprieta ahí
tablero = [[sg.Button(size=(AN, AL), key=(999,j), pad=(21.5,18)) for j in range(cant_letras)]]
tablero.extend([[m_tablero.crear_boton(i,j,AN,AL) for j in range(filas)] for i in range(filas)])
tablero.extend([[sg.Text("Seleccione una letra de abajo",pad=(200,5))],
    [sg.Button(m_tablero.tomar_y_borrar(Letras), key = j, size=(AN, AL), pad=(21.5,0)) for j in range(cant_letras)],
    [sg.Button('Ingresar Palabra!', size= (7,3), pad=(112,20)),sg.Button('Terminar', size=(7, 3), pad=(112,20))]])

# \n pone lo que sigue un renglón más abajo  
zona_puntos_jugador = [[sg.Button("PUNTOS\n"+str(puntos_jugador), size=(8, 4), key=(888,0), pad=(0,340))]]
zona_puntos_maquina = [[sg.Button("PUNTOS\n"+str(puntos_maquina), size=(8, 4), key=(888,1), pad=(0,340))]]

pal_y_pun_jug_en_pantalla = [[m_tablero.palabras_por_turno_pantalla(444,j) for j in range(20)]] # Puede mostrar hasta 20 palabras
pal_y_pun_maq_en_pantalla = [[m_tablero.palabras_por_turno_pantalla(445,j) for j in range(20)]] # Puede mostrar hasta 20 palabras

layout = [[sg.Column(pal_y_pun_maq_en_pantalla),sg.Column(zona_puntos_maquina),sg.Column(tablero),sg.Column(zona_puntos_jugador),sg.Column(pal_y_pun_jug_en_pantalla)]]

window = sg.Window('ScrabbleAR',layout)
cambiar = False
lugares_usados_temp = []
lugares_usados_total = []
vertical = False
horizontal = False
letras_ingresadas = 0
backup_text = [] #lista con texto de botones p/ restablecer en caso de palabra erronea.
palabra = [] # borre letras usadas y solo queda palabra. mande a las funciones que usaban letras_usadas palabras y funcionan igual.
pos_atril_usadas = [] # lista con las posiciones usadas del atril. Sirve en caso de reponer y para que no se vuelvan a usar.
# reponer, además,  cuando se usa una letra se guarda acá y si está acá ya no se puede usar otra vez

while True:
    event, values = window.read()
    #print(pos_atril_usadas)
    #print(backup_text)
    #print(event)
    if event in (None, 'Terminar'):
        break
    if m_tablero.puedo_cambiar(cambiar,event,lugares_usados_total):  
        
    #INGRESAR PRIMERA LETRA
        if not lugares_usados_total: # Si lugares usados es vacio, solo permito ingresar en inicio.
            if event == INICIO:
                m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)  
                cambiar = False
                letras_ingresadas += 1
        else:
            #DETERMINAR SI SE INGRESA HORIZONTAL O VERTICAL
            #print(horizontal)
            if not lugares_usados_temp:
                m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)
                cambiar = False
                letras_ingresadas += 1
            else:
                if not horizontal:
                    if m_tablero.es_vertical(letras_ingresadas,event,lugares_usados_temp):
                        vertical = True # Si suma o resta 1 a las columnas, vertical = true
                        m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)                
                        cambiar = False
                        letras_ingresadas += 1
                if not vertical:
                    if m_tablero.es_horizontal(letras_ingresadas,event,lugares_usados_temp):
                        horizontal = True
                        m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)
                        cambiar = False
                        letras_ingresadas += 1
        
            # SE BORRA LA LETRA USADA
        if not cambiar: # si cambiar pasa a false, es porque ya puso una letra en el atril.
            #print(boton_de_la_letra)
            window[boton_de_la_letra].update("---")
    
    #AGARRO DEL ATRIL
    if m_tablero.es_letra_atril(event):
        #escribir = event[0] # ahora no puedo agarrar directamente de event el texto del boton. 
        if event not in pos_atril_usadas: # para que no se puedan agarrar los "---"
            escribir = window.Element(event).GetText()
            cambiar = True
            boton_de_la_letra = event # Con esto puedo acceder al botón de la letra usada // ahora es un integer.

    #CHEQUEO DE PALABRA
    if m_tablero.ingreso_palabra(letras_ingresadas,event):
        to_string = ''.join(palabra) # paso lista palabra a string
        if not m_buscador.buscar_palabra(to_string):
            m_tablero.quitar_letras(lugares_usados_temp,backup_text,window)
            m_tablero.devolver_letras_atril(palabra,pos_atril_usadas,window)
            
            # reset de variables:
            pos_atril_usadas = []
            horizontal = False
            vertical = False
            backup_text = []
            letras_ingresadas = 0
            for tupla in lugares_usados_temp:
                lugares_usados_total.remove(tupla) # quito valores de temp que estan en total.
            lugares_usados_temp = []
            palabra = []
            cambiar = False
        else:
            puntos_actuales = m_tablero.calcular_puntos(palabra,lugares_usados_temp,valores_letras)
            puntos_jugador = puntos_jugador + puntos_actuales
            m_tablero.agregar_pal_y_pun_a_pantalla(to_string,0,puntos_actuales,window)
            m_tablero.actualizar_puntos(0,window,puntos_jugador)
            m_tablero.dar_nuevas_letras(Letras,pos_atril_usadas,window)
            pos_atril_usadas = []
            horizontal = False
            vertical = False
            backup_text = []
            letras_ingresadas = 0
            lugares_usados_temp = []
            palabra = []
            cambiar = False
    #print(palabra) 
window.close()
