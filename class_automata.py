import os

# 1- Definición de clase Autómata.

class Automata:
    def __init__(self, alfabeto = [], estados = [], f_transicion = {}, inicial = "", estados_finales = []):
        self.alfabeto = alfabeto
        self.estados = estados
        self.f_transicion = f_transicion
        self.inicial = inicial
        self.estados_finales = estados_finales
        self.tipo_automata = "Determinista" # Autómata considerado por defecto Determinista.
        self.cadena_vacia = False # Autómata considerado por defecto sin e-transiciones.
    
    def leer_archivo(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r') as archivo:
                linea_estados = archivo.readline().strip("\n").split(sep=" "); linea_estados.pop(0)
                self.estados = linea_estados
                self.inicial = linea_estados[0] #Asunción de que el estado inicial es el primero que aparece.
                
                linea_estados_finales = archivo.readline().strip("\n").split(sep=" "); linea_estados_finales.pop(0)
                if len(linea_estados_finales) != len(list(filter((lambda x: x in self.estados), linea_estados_finales))):
                    print("\n¡ERROR!. Ha declarado estados finales que no se encuentran en la primera definición de estados.")
                    return False
                self.estados_finales = linea_estados_finales
                
                linea_alfabeto = archivo.readline().strip("\n").split(sep=" "); linea_alfabeto.pop(0)
                linea_alfabeto.append("λ")
                self.alfabeto = linea_alfabeto
                
                self.f_transicion = {i:{j:[] for j in self.alfabeto} for i in self.estados}
                lineas_transicion = archivo.readlines(); lineas_transicion.pop(0)
                if len(lineas_transicion) != len(self.estados):
                    print(f"\n¡ERROR!. Inicializados {len(self.estados)} estados en el autómata. Encontrados {len(lineas_transicion)} en la función de transición.")
                    return False
                
                for (indice, transicion_estado) in enumerate(lineas_transicion):
                    transiciones = transicion_estado.strip("\n").split("#"); transiciones.pop()
                    for indice_alfabeto in range(len(transiciones)):
                        a = transiciones[indice_alfabeto].strip(" ").split(" ")
                        if a == ['']:
                            self.f_transicion[self.estados[indice]][self.alfabeto[indice_alfabeto]] = []
                        else:
                            self.f_transicion[self.estados[indice]][self.alfabeto[indice_alfabeto]] = a
                            if len(a) > 1: # Clasificación del autómata en No-Determinista.
                                self.tipo_automata = 'No Determinista'
                            if self.alfabeto[indice_alfabeto] == "λ":
                                self.tipo_automata = 'No Determinista'
                                self.cadena_vacia = True
                            
        except FileNotFoundError:
            print(f"\nEl archivo '{ruta_archivo}' no existe.")
            return False
        except Exception as e:
            print(f"\nError al leer el archivo: {e}")
            return False            
        
        print(f"\nLectura correcta del archivo. Autómata caracterizado como [{self.tipo_automata}]")
        if self.cadena_vacia:
            print("Detectadas TRANSICIONES CON CADENA VACÍA (AFN-e)\n")
        return True
    
    def __claus__(self, estados): # Cálculo de la clausura para una lista de estados.
        for estado in estados:
            estados += self.f_transicion[estado]["λ"]
        return estados
                
    def procesar_cadena(self, cadena:str, verbose=False):
        cadena = cadena.replace(" ", "")
        estados_actuales = set([self.inicial])
        if self.tipo_automata == "No Determinista" and self.cadena_vacia:
            clausura_actual = set(self.__claus__([self.inicial])) # Aplicacion de clausura sobre estado inicial.
        for indice in range(len(cadena)):
            if cadena[indice] not in self.alfabeto:
                print(f'\nERROR. El alfabeto del autómata no admite el caracter: {cadena[indice]}')
                return False
            
            if verbose == True:
                print("\n------------------------------------------")
                print(f"Estados actuales: {estados_actuales}")
                if self.tipo_automata == "No Determinista" and self.cadena_vacia:
                    print(f"Clausura actual: {clausura_actual}")
                print(f"Caracter de entrada [nº {indice+1}] --> {cadena[indice]}")
            
            if self.tipo_automata == "No Determinista" and self.cadena_vacia:
                estados_actuales = clausura_actual
                
            nuevos_estados = []
            for estado in estados_actuales:
                if verbose == True:
                    linea = "\n-----Estado: " + str(estado) + " | " + "Entrada: " + str(cadena[indice]) + " | " + "Estados destino: " + str(self.f_transicion[estado][cadena[indice]])
                    if self.f_transicion[estado][cadena[indice]] == []:
                        linea += " | MUERTE DEL ESTADO " + str(estado)
                    print(linea)
                nuevos_estados += self.f_transicion[estado][cadena[indice]]
                
            estados_actuales = set(nuevos_estados)
            if self.tipo_automata == "No Determinista" and self.cadena_vacia:
                clausura_actual = set(self.__claus__(nuevos_estados)) # Aplicación de clausura sobre cada estado actual.
            if len(estados_actuales) == 0:
                print("\nMUERTE. Transiciones no definidas. Cadena NO aceptada.")
                return False
         
        print("\n------------------------------------------")
        if self.tipo_automata == "No Determinista" and self.cadena_vacia:
            print("\nEstados finales del autómata: " + str(clausura_actual))
        else:
            print("\nEstados finales del autómata: " + str(estados_actuales))
            
        for i in self.estados_finales:
            if not self.cadena_vacia:
                if i in estados_actuales:
                    print("¡Cadena aceptada satisfactoriamente!")
                    return True
            else:
                if i in clausura_actual:
                    print("¡Cadena aceptada satisfactoriamente!")
                    return True
        print("Cadena NO aceptada.")
        return False
    
    def __str__(self):
        impresion = ''
        for i in self.estados:
            impresion += f"\nEstado {i} \n"
            for (clave,valor) in self.f_transicion[i].items():
                if clave != "λ":
                    impresion += f"   {i}({clave}) ---> {valor}\n"
                elif clave == "λ" and self.tipo_automata == "No Determinista" and self.cadena_vacia:
                    impresion += f"   {i}({clave}) ---> {valor}\n"
        return impresion
    
    
# 2- Función auxiliar para el menú principal.

def espera():
    '''Función que solicita "input" hasta que el usuario pulsa la tecla <ENTER>'''
    a = 0
    while a != '':
        a = input('Pulse <ENTER> para continuar: ')
    
# 3- Código principal.

def main():
    directorio_actual = os.getcwd()
    ruta_archivo = input("\nIngresa el camino relativo al archivo: ")
    ruta_completa = os.path.join(directorio_actual, ruta_archivo) # Poner ruta_archivo
    
    automata1 = Automata()
    if not automata1.leer_archivo(ruta_completa):
        return None
    espera()
    
    flag = str(input("\n¿Desea comprobar la estructura del autómata? (S/s) | (N/n): "))
    if flag in {"S", "s"}:
        print(automata1) 
        espera()
        
    fin = "N"
    while fin != "Y":
        cadena = str(input("\nIntroducir cadena: "))
        automata1.procesar_cadena(cadena, verbose=True)
        espera()
        fin = str(input("\nPulse <Y> si desea finalizar el programa. En otro caso, cualquier tecla: "))
        if fin == "Y":
            return None

if __name__ == '__main__':
    main()
    
