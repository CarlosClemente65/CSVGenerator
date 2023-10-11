import random
import datetime
import os
import sys

# Definición de variables
caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
largo_cadena = 8
salida_txt = ""

def main(parametros):
    global largo_cadena
    
    # Comprueba los Parametros pasados y si son validos
    if not parametros:
        # Si no se pasaron Parametros, generar el archivo de salida
        pass
    elif len(parametros) == 1:
        if parametros[0] == "-h":
            limpiar_consola()
            texto_ayuda()
            return
        elif parametros[0] == "-c":
            limpiar_consola()
            print("Debe proporcionar el codigo CSV a comprobar\n")
            texto_ayuda()
            return
        else:
            limpiar_consola()
            print ("Parametros incorrectos\n")
            texto_ayuda()
            return
    elif len(parametros) == 2:
        if parametros[0] == "-c":
            # Se pasó un código a comprobar
            comprueba_csv(parametros[1])
            return
        else:
            limpiar_consola()
            print("Parametros incorrectos\n")
            texto_ayuda()
            return
    else:
        limpiar_consola()
        print("Parametros incorrectos\n")
        texto_ayuda()
        return

    # Genera el CSV con los caracteres pasados
    codigo_csv = generar_csv(largo_cadena)
    grabar_resultado(f"CSV generado: {codigo_csv}")
    
def texto_ayuda():
    print("Uso de la aplicacion")
    print("generarCSV [opciones]\n")
    print("Opciones:")
    print("\tSin parametros genera un CSV")
    print("\t-h Esta ayuda")
    print("\t-c Comprueba el CSV introducido a continuacion\n")
    #input("Pulse una tecla para salir")
    
def limpiar_consola():
    os.system('cls')
    
def grabar_resultado(mensaje):
    # Guarda el resultado en un archivo
    # Obtén la ubicación actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    nombre_archivo = os.path.join(script_dir, "codigoCSV.txt")
    try:
        with open(nombre_archivo, "w") as archivo:
            archivo.write(mensaje)
    except Exception as ex:
        print(f"Error al generar el archivo: {ex}")

def comprueba_csv(csv):
    #Verifica si la longitud es de 20 caracteres
    if len(csv) != 20:
        mensaje = "El CSV debe tener una longitud de 20 caracteres."
        grabar_resultado(mensaje)
        return
    
    #Intenta comprobar si el digito de control o la marca de tiempo hexadecimal se puede tratar
    try:
        # Obtiene el dígito de control del CSV pasando los caracteres menos los dos últimos (son el DC) y comprueba si coinciden con los dos últimos caracteres del CSV
        chk_dc = calculo_dc(csv[:-2])
        ok_dc = str(chk_dc) == csv[-2:]
        
        # Obtiene los datos de la fecha del CSV
        fecha_previa = csv[:10]
        dias = ""
        segundos = ""
        for i in range(10):
            if i % 2 == 0:
                # Los segundos están en las posiciones pares y en orden inverso, por lo que se van almacenando delante de los que ya se han ido obteniendo
                segundos = fecha_previa[i] + segundos
            else:
                # Los días están en las posiciones impares y en orden, por lo que se van almacenando uno detrás de otro según se obtienen
                dias += fecha_previa[i]

        # Convierte los segundos y los días que están en hexadecimal a números enteros
        total_segundos = int(segundos, 16)
        total_dias = int(dias, 16)

        # Calcula la fecha sumando los días al 01/01/2000
        fecha = datetime.date(2000, 1, 1) + datetime.timedelta(days=total_dias)
        fecha_str = fecha.strftime("%d/%m/%Y")

        # Calcula la hora de acuerdo con los segundos obtenidos
        h = total_segundos // 3600
        m = (total_segundos % 3600) // 60
        s = total_segundos % 60
        hora = f"{h:02d}:{m:02d}:{s:02d}"
    
        # Guarda el resultado en un archivo
        try:
            if ok_dc:
                mensaje = f"CSV: {csv}\nResultado: OK\nGenerado: {fecha_str} a las {hora}"
                grabar_resultado(mensaje)
            else:
                mensaje = f"El CSV {csv} no es correcto"
                grabar_resultado(mensaje)
        except Exception as ex:
            print(f"Error al generar el archivo: {ex}")
    except Exception as ex:
        mensaje = f"El CSV no es correcto"
        grabar_resultado(mensaje)

def generar_csv(largo):
    global salida_txt

    longitud = largo
    calculo_cadena = cadena_csv(longitud)

    calculo_tiempo = cadena_tiempo()

    csv_previo = calculo_tiempo + calculo_cadena

    dc = calculo_dc(csv_previo)

    csv_calculado = csv_previo + str(dc)

    return csv_calculado

def cadena_csv(longitud):
    # Generar cadena de n caracteres de forma aleatoria
    csv = "".join(random.choice(caracteres) for _ in range(longitud))
    return csv

def cadena_tiempo():
    # Cálculo de los días que han pasado desde el 01/01/2000
    dif_dias = datetime.date.today() - datetime.date(2000, 1, 1)
    total_dias = dif_dias.days
    total_dias = abs(total_dias) # Asegura que sea un valor no negativo
    hex_dias = format(total_dias, "05X")  # Se pasan a hexadecimal con 5 caracteres

    # Cálculo de los segundos transcurridos hoy en formato hexadecimal con 5 caracteres
    total_segundos = datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60 + datetime.datetime.now().second
    hex_segundos = format(total_segundos, "05X")

    # Se combinan los segundos y días en una sola cadena de 10 dígitos
    cadena = ""
    for i in range(5):
        cadena += hex_segundos[4 - i] + hex_dias[i]

    return cadena

def calculo_dc(cadena):
    suma = 0
    peso = 1

    # Iterar a través de los caracteres
    for i, caracter in enumerate(cadena):
        if caracter.isdigit():
            digito = int(caracter)
            suma += digito * peso
        elif caracter.isalpha():
            valor_letra = ord(caracter.upper()) - ord("A") + 10
            suma += valor_letra * peso

        # Alterna el peso (1 o 2)
        peso = 2 if peso == 1 else 1

    # Calcula el dígito de control como el resultado de restar a 98 el residuo de la suma dividida por 97 (números + letras)
    digito_control = 98 - (suma % 97)

    return digito_control

if __name__ == "__main__":
    main(sys.argv[1:])

