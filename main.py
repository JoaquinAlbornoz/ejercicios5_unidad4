import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = "6bd5e7fdf1de00d2f53c7a10a37ae32f&language=es"
API_URL = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}'

class CinemafilosApp:
    def __init__(self):
        self.__ventana = tk.Tk()
        self.__ventana.title('Cinéfilos Argentinos')
        
        self.__listbox = tk.Listbox(self.__ventana, width=50)
        self.__listbox.pack(pady=10)
        self.__listbox.bind('<Double-Button-1>', self.mostrarDetallePelicula)
        
        self.obtenerPeliculas()

        self.__ventana.mainloop()

    def obtenerPeliculas(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                peliculas = data['results']
                for pelicula in peliculas:
                    self.__listbox.insert(tk.END, pelicula['title'])
            else:
                messagebox.showerror('Error', 'Error al obtener las películas')
        except requests.exceptions.RequestException:
            messagebox.showerror('Error', 'Error al conectarse a la API')

    def mostrarDetallePelicula(self, event):
        seleccion = self.__listbox.curselection()
        if seleccion:
            pelicula_index = seleccion[0]
            try:
                response = requests.get(API_URL)
                if response.status_code == 200:
                    data = response.json()
                    pelicula = data['results'][pelicula_index]
                    detalle = f'Título: {pelicula["title"]}\n'
                    detalle += f'Resumen: {pelicula["overview"]}\n'
                    detalle += f'Lenguaje Original: {pelicula["original_language"]}\n'
                    detalle += f'Fecha de Lanzamiento: {pelicula["release_date"]}\n'
                    detalle += f'Géneros: {self.obtenerNombresGeneros(pelicula["genre_ids"])}'
                    messagebox.showinfo('Detalle de la Película', detalle)
                else:
                    messagebox.showerror('Error', 'Error al obtener el detalle de la película')
            except requests.exceptions.RequestException:
                messagebox.showerror('Error', 'Error al conectarse a la API')

    def obtenerNombresGeneros(self, genre_ids):
        generos = {
            28: 'Action', 12: 'Adventure', 16: 'Animation', 35: 'Comedy', 80: 'Crime',
            99: 'Documentary', 18: 'Drama', 10751: 'Family', 14: 'Fantasy', 36: 'History',
            27: 'Horror', 10402: 'Music', 9648: 'Mystery', 10749: 'Romance', 878: 'Science Fiction',
            10770: 'TV Movie', 53: 'Thriller', 10752: 'War', 37: 'Western'
        }
        nombres_generos = []
        for genre_id in genre_ids:
            if genre_id in generos:
                nombres_generos.append(generos[genre_id])
        return ', '.join(nombres_generos)

# Crear una instancia de la aplicación
if __name__=='__main__':
    app = CinemafilosApp()
