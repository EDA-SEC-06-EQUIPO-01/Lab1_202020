"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista.
"""

from time import process_time
import csv
import sys
import config as cf
from collections import Counter
details_csv_name = "SmallMoviesDetailsCleaned.csv"
casting_csv_name = "MoviesCastingRaw-small.csv"


def loadCSVFile(file, lst, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file 
            Archivo de texto del cual se cargaran los datos requeridos.
        lst :: []
            Lista a la cual quedaran cargados los elementos despues de la lectura del archivo.
        sep :: str
            Separador escodigo para diferenciar a los distintos elementos dentro del archivo.
    Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None   
    """
    del lst[:]
    print("Cargando archivo ....")
    t1_start = process_time()  # tiempo inicial
    dialect = csv.excel()
    dialect.delimiter = sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader:
                lst.append(row)
    except:
        del lst[:]
        print("Se presento un error en la carga del archivo")

    t1_stop = process_time()  # tiempo final
    print("Tiempo de ejecución ", t1_stop-t1_start, " segundos")


def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Contar los elementos de la Lista")
    print("3- Contar elementos filtrados por palabra clave")
    print("4- Consultar elementos a partir de dos listas")
    print("5- Conocer las buenas películas")
    print("0- Salir")


def countElementsFilteredByColumn(criteria, column, lst):
    """
    Retorna cuantos elementos coinciden con un criterio para una columna dada  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    if len(lst) == 0:
        print("La lista esta vacía")
        return 0
    else:
        t1_start = process_time()  # tiempo inicial
        counter = 0  # Cantidad de repeticiones
        for element in lst:
            # filtrar por palabra clave
            if criteria.lower() in element[column].lower():
                counter += 1
        t1_stop = process_time()  # tiempo final
        print("Tiempo de ejecución ", t1_stop-t1_start, " segundos")
    return counter


def countElementsByCriteria(criteria, column, lst):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    return 0


def buenasPeliculas(name: str, casting: dict, details: dict) -> tuple:
    average = False
    director = False
    prom = 0
    contprom = 0
    cont = 0
    id1 = False
    id2 = False
    for i in casting.keys():
        staff = casting[i]
        if staff["director_name"] == name:
            director = True
            id1 = True
        for a in details.keys():
            votos = details[a]
            if votos["vote_average"] >= 6:
                average = True
                id2 = True
                if average == True and director == True and id1 == id2:
                    contprom += (votos["vote_average"])
                    cont += 1
    prom = contprom/cont
    return (cont, prom)


def conocerActor(name: str, casting: list, details: list) -> tuple:
    listaDirector = []
    directorColab = 0
    pelis = []
    cont = 0
    contprom = 0
    prom = 0
    for i in casting.keys():
        for a in details.keys():
            votos = details[a]
            staff = casting[i]
            if (staff["actor1_name"] == name) or (staff["actor2_name"] == name) or (staff["actor3_name"] == name) or (staff["actor4_name"] == name) or (staff["actor5_name"] == name):
                listaDirector.append(staff["director_name"])
                pelis.append(votos["original_title"])
                cont += 1
                contprom += (votos["vote_average"])
    prom = contprom/cont
    c = Counter(listaDirector)
    directorColab = (max(c, key=c.get))
    return (pelis, cont, prom, directorColab)


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    lista_details = []  # instanciar una lista vacia
    lista_casting = []  # nueva lista
    while True:
        printMenu()  # imprimir el menu de opciones en consola
        # leer opción ingresada
        inputs = input('Seleccione una opción para continuar\n')
        if len(inputs) > 0:
            if int(inputs[0]) == 1:  # opcion 1
                # llamar funcion cargar datos (lista de detalles)
                loadCSVFile(f"Data/{details_csv_name}", lista_details)
                print("Datos cargados, "+str(len(lista_details)) +
                      " elementos cargados")

                # cargar datos (lista de casting)
                loadCSVFile(f"Data/{casting_csv_name}", lista_casting)
                print(
                    f"Datos cargados, {len(lista_casting)} elementos cargados")
            elif int(inputs[0]) == 2:  # opcion 2
                if len(lista_details) == 0:  # obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    print("La lista tiene "+str(len(lista_details))+" elementos")
            elif int(inputs[0]) == 3:  # opcion 3
                criteria = input('Ingrese el criterio de búsqueda\n')
                counter = countElementsFilteredByColumn(
                    criteria, "nombre", lista_details)  # filtrar una columna por criterio
                print("Coinciden ", counter,
                      " elementos con el crtierio: ", criteria)
            elif int(inputs[0]) == 4:  # opcion 4
                criteria = input('Ingrese el criterio de búsqueda\n')
                counter = countElementsByCriteria(criteria, 0, lista_details)
                print("Coinciden ", counter, " elementos con el crtierio: '",
                      criteria, "' (en construcción ...)")
            elif int(inputs[0]) == 5:  # opcion 5
                director = input('Ingrese el nombre del director\n')
                buenaspelis = buenasPeliculas(
                    director, lista_casting, lista_details)
                print(
                    f"Se encontraron {buenaspelis[0]} buenas películas con los parámetros dados.")
                print(
                    f"El promedio de la votación por dichas películas es de {buenaspelis[1]}.")
            elif int(inputs[0]) == 0:  # opcion 0, salir
                sys.exit(0)


if __name__ == "__main__":
    main()
