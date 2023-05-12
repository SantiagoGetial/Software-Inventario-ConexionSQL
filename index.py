from tkinter import ttk 
from tkinter import *
import sqlite3

class Product:
    #Vamos a crear funcion para que la base de datos interactue sola y se actualice con el programa 
     db_name = 'database.db'

    #Inicio 
     def __init__(self, window):
        # ...

        self.wind = window
        self.wind.title('Productos')

        #En esta parte se crea el contenedor vacio de input 
        frame = LabelFrame(self.wind, text= 'Registra un nuevo producto') #Elemento nuevo almacenado en una variable
        frame.grid(row= 0, column= 0, columnspan= 3, pady= 20)  #Donde vamos a posicionar el elemento nuevo creado anteriormente 
        
        #En la siguientes lineas se llena el contenedor con lo necesario 
        Label(frame, text= 'Nombre: ').grid(row= 1, column= 0)
        self.name = Entry(frame) #Es lo mismo que un input o escribir donde el usuario va a colocar los datos y los va a almacenar 
        self.name.focus()
        self.name.grid(row = 1, column= 1)

        #Input de entrada de precios 
        Label(frame, text= 'Precio: ').grid(row=2, column= 0) #Se crea el contenedor en la pantalla principal 
        self.precio = Entry(frame) #Se almacena lo ingresado
        self.precio.grid(row= 2, column=1)

        #Botton 
        ttk.Button(frame, text= 'Guardar producto', command = self.add_product).grid(row=3, columnspan=2, sticky= W + E) #Se crea el botton con el mismo patron anterio Sticky es para ubicar el botton en toda la pantalla y ejecuta la funcion add product 
          
        #Mensajes o avisos 
        self.message = Label(text= '', fg= 'red')  #Etiqueta sin texto al inicio de color rojo 
        self.message.grid(row = 3, column = 0, columnspan=2, sticky= W + E)

        #Tabla 
        self.tree = ttk.Treeview(height= 10, columns=2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre del proucto', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio del producto', anchor = CENTER)

        #Botones borrar y editar
        ttk.Button(text= 'Delete', command= self.delete_product).grid(row = 5, column = 0, sticky= W + E)
        ttk.Button(text= 'Editar').grid(row = 5, column = 1, sticky= W + E)

       #Llenando las filas de la tabla 
        self.get_products()
      
      #Consulta SQL
     def run_query(self, query, parameters = ()):
      with sqlite3.connect(self.db_name) as conn:  #Establece una conexion a la base de datos SQLite utilizando el nombre de archivo 
        cursor = conn.cursor()
        result = cursor.execute(query, parameters) #Ejecuta la consultaSQL especificada en 'query'
        conn.commit() 
      return result #En esta linea devuelve el objeto resultante de la ejecucion de la consulta 
    
     def get_products(self):
      #Limpiando datos 
      records = self.tree.get_children() #Se guarda los elementos en una variable llamada records 
      for element in records:
        self.tree.delete(element) #Rectifica si la tabla esta vacia o sino la limpia 

      #Consultando datos 
      query = 'SELECT * FROM product ORDER BY "Nombre" DESC' #De la base de datos producto ordena en orden descendente de la fila nombre
      db_rows = self.run_query(query)

      #Llenando los datos 
      for row in db_rows: #Para cada fila in db filas 
        self.tree.insert('', 0, text = row[1], values = row[2]) #Coloca el nombre o precio del producto de la fila dependiendo del indice o psocicion donde se encuentre 

     def validation(self):
       return len(self .name.get()) != 0 and len(self .precio.get()) != 0 #Toma la longitud de lo que el usuario ingreso comparando si es distinto a 0
    
     def add_product(self):
       if self.validation(): #Si al ejecutar la validacion es verdaderio entonces 
          query = 'INSERT INTO product VALUES(NULL, ?, ? )'  #Dentro de la tabla producto voy a insertar los siguientes valores 
          parameters = (self.name.get(), self.precio.get())  #Obengo el nombre del elemento que el ususario esta tipeando 
          self.run_query(query, parameters)  #Ejecuta la query y los parametros 
          self.message['text'] = 'El producto {} ha sido agregado'.format(self.name.get()) #Se mostrara que el producto ha sido guardado
          self.name.delete(0, END)
          self.precio.delete(0, END) #Vuelve al dato inicial

       else:
         self.message['text'] = 'El nombre y el precio son requeridos' 
       self.get_products() #Ejecuta nuevamente el comando para que la base de datos se actualice 

     #Eliminar productos 
     def delete_product(self):
      self.message['text'] = ''
      try: #Si el usuario selecciono algun producto, continua 
        self.tree.item(self.tree.selection())['text'][0] #Selecciona el tipo del producto añadido, quisiera obtener el texto del elemento en el indice 0 
      except IndexError as e: #De lo contrario 
        self.message['text'] = 'Por favor selecciona un registro'
        return #Retornamos para que no continue  
      self.message['text'] = ''  
      Nombre = self.tree.item(self.tree.selection())['text']
      query = 'DELETE FROM product WHERE Nombre = ?'
      self.run_query(query,(Nombre, )) #El parametro que le pasa para eliminar es el nombre 
      self.message['text'] = 'El producto {} ha sido eliminado satisfactoriamente'.format(Nombre) #El producto ha sido eliminado satisfactoriamente
      self.get_products()


if __name__ == '__main__':
    window = Tk()   
    application = Product(window)
    window.mainloop()
