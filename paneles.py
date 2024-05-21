from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import psycopg2
from psycopg2 import OperationalError
import subprocess
from datetime import datetime
from PyQt5 import QtWidgets




ui, _ = loadUiType('interfaz.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        self.pushButton.clicked.connect(self.login)
        self.actionAGREGAR_3.triggered.connect(self.Agregar_cliente)
        self.actionELIMINAR_2.triggered.connect(self.Eliminar_cliente)
        self.actionELIMINAR.triggered.connect(self.Eliminar_panel)
        self.actioncerrar_sesion.triggered.connect(self.cerrar_sesion)
        self.actionVER_CLIENTES.triggered.connect(self.mostrar_cliente)
        self.actionVER_PANELES.triggered.connect(self.mostrar_panel)
        self.actionAGREGAR.triggered.connect(self.Agregar_panel)
        self.actionVer.triggered.connect(self.auditoria)
        self.pushButton_4.clicked.connect(self.realizar_insercion_cliente)
        self.pushButton_7.clicked.connect(self.insercion_eliminar_cliente)
        self.pushButton_6.clicked.connect(self.realizar_insercion_panel)
        self.pushButton_8.clicked.connect(self.insercion_eliminar_panel)
        self.actionAGREGAR_2.triggered.connect(self.Agregar_proyecto)
        self.pushButton_9.clicked.connect(self.realizar_insercion_proyecto)
        self.actionCANCELAR.triggered.connect(self.Eliminar_proyecto)
        self.pushButton_10.clicked.connect(self.insercion_eliminar_proyecto)
        self.actionVER_PROYECTOS.triggered.connect(self.mostrar_proyecto)
        self.actionrespaldarBD.triggered.connect(self.respaldo)
        


        self.usuario = ""
        self.contraseña = ""

    def login(self):
        self.usuario = self.lineEdit.text()
        self.contraseña = self.lineEdit_2.text()
        self.menubar.setVisible(False)

        try:
            # Intentar la conexión a la base de datos
            connection = psycopg2.connect(
                user=self.usuario,
                password=self.contraseña,
                host="localhost",
                port="5432",
                database="postgres"  
            )
            
            # Si la conexión es exitosa, realizar las acciones deseadas
           
            self.menubar.setVisible(True)
            self.tabWidget.setCurrentIndex(1)

            QMessageBox.information(self, "Conexión Exitosa", "Conexión a la base de datos exitosa.")

        except OperationalError as e:
            # En caso de error al conectar, mostrar mensaje y no realizar acciones adicionales
            print("Error al conectar a la base de datos:", e)
            QMessageBox.information(self, "Error de Conexión", "No se pudo conectar a la base de datos. Verifica tus credenciales.")
            self.l01.setText("Datos inválidos. Intenta de nuevo.")

        finally:
            # Cerrar conexión si se abrió
            if 'connection' in locals():
                connection.close()
            
    def Agregar_cliente(self):
        
        self.tabWidget.setCurrentIndex(1)   
    def Eliminar_cliente(self):
        
        self.tabWidget.setCurrentIndex(4)   
       
    def realizar_insercion_cliente(self):
        # Obtener referencias a los QLineEdit 
        id_cliente = self.lineEdit_8.text()
        nombre_cliente = self.lineEdit_7.text()
        direccion_cliente = self.lineEdit_9.text()
        telefono_cliente = self.lineEdit_10.text()
        correo_cliente = self.lineEdit_11.text()

        try:
            connection = psycopg2.connect(
                user=self.usuario,
                password=self.contraseña,
                host="localhost",
                port="5432",
                database="postgres" 
            )

            cursor = connection.cursor()

            # Consulta de inserción
            insert_query = """
                INSERT INTO public.cliente (
                    id,
                    nombre,
                    direccion,
                    telefono,
                    correo
                ) VALUES (
                    %s, %s, %s, %s, %s
                )
            """

            data = (
                id_cliente,
                nombre_cliente,
                direccion_cliente,
                telefono_cliente,
                correo_cliente
            )

            cursor.execute(insert_query, data)
            connection.commit()

            QMessageBox.information(self, "Éxito", "Cliente agregado correctamente.")

        except (Exception, psycopg2.Error) as error:
            print("Error al conectar o insertar datos:", error)
            QMessageBox.critical(self, "Error", "No se pudo agregar cliente.")

        finally:
            # Cerrar conexión
            if connection:
                cursor.close()
                connection.close()

    def insercion_eliminar_cliente(self):
        # Obtener el ID del cliente a eliminar desde el QLineEdit
        id_cliente_a_eliminar = self.lineEdit_22.text()

        try:
            connection = psycopg2.connect(
                user=self.usuario,
                password=self.contraseña,
                host="localhost",
                port="5432",
                database="postgres"  
            )

            cursor = connection.cursor()

            # Consulta de eliminación
            delete_query = "DELETE FROM public.cliente WHERE id = %s"

            # Pasar el ID del cliente como parámetro a la consulta
            cursor.execute(delete_query, (id_cliente_a_eliminar,))
            connection.commit()

            # Verificar si se eliminó algún registro
            if cursor.rowcount > 0:
                QMessageBox.information(self, "Éxito", f"Cliente con ID {id_cliente_a_eliminar} eliminado correctamente.")
            else:
                QMessageBox.warning(self, "Advertencia", f"No se encontró un cliente con ID {id_cliente_a_eliminar}.")

        except (Exception, psycopg2.Error) as error:
            print("Error al conectar o eliminar datos:", error)
            QMessageBox.critical(self, "Error", "No se pudo eliminar cliente.")

        finally:
            # Cerrar conexión
            if connection:
                cursor.close()
                connection.close()

    def cerrar_sesion(self):
        self.menubar.setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        
    def mostrar_cliente(self):
        self.tabWidget.setCurrentIndex(8)
        try:
            connection = psycopg2.connect(
                user=self.usuario,
                password=self.contraseña,
                host="localhost",
                port="5432",
                database="postgres"
            )

            cursor = connection.cursor()

            select_query = "SELECT * FROM public.cliente"
            cursor.execute(select_query)

            # Obtener resultados
            resultados = cursor.fetchall()

            # Configurar el número de filas y columnas en el QTableWidget
            self.tableWidget.setRowCount(len(resultados))
            self.tableWidget.setColumnCount(len(cursor.description))

            # Configurar las etiquetas de las columnas en el QTableWidget
            columnas = [desc[0] for desc in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(columnas)

            # Llenar el QTableWidget con los resultados
            for i, row in enumerate(resultados):
                for j, valor in enumerate(row):
                    item = QTableWidgetItem(str(valor))
                    self.tableWidget.setItem(i, j, item)

        except (Exception, psycopg2.Error) as error:
            print("Error al conectar o realizar la consulta:", error)
            QMessageBox.critical(self, "Error", "No se pudo obtener la información de los pedidos.")

        finally:
            # Cerrar conexión
            if connection:
                cursor.close()
                connection.close()



    def Agregar_panel(self):
        
        self.tabWidget.setCurrentIndex(3)   
    def Eliminar_panel(self):
        
        self.tabWidget.setCurrentIndex(5)   
       
    def realizar_insercion_panel(self):
        # Obtener referencias a los QLineEdit 
        tipo = self.lineEdit_18.text()
        proveedor = self.lineEdit_17.text()
        costo = self.lineEdit_19.text()
        id_panel = self.lineEdit_21.text()
        

        try:
            connection = psycopg2.connect(
                user=self.usuario,
                password=self.contraseña,
                host="localhost",
                port="5432",
                database="postgres" 
            )

            cursor = connection.cursor()

            # Consulta de inserción
            insert_query = """
                INSERT INTO public.producto (
                    id,
                    tipopanel,
                    proveedor,
                    costounitario
                ) VALUES (
                    %s, %s, %s, %s
                )
            """

            data = (
                id_panel,
                tipo,
                proveedor,
                costo
            )

            cursor.execute(insert_query, data)
            connection.commit()

            QMessageBox.information(self, "Éxito", "Panel agregado correctamente.")

        except (Exception, psycopg2.Error) as error:
            print("Error al conectar o insertar datos:", error)
            QMessageBox.critical(self, "Error", "No se pudo agregar Panel.")

        finally:
            # Cerrar conexión
            if connection:
                cursor.close()
                connection.close()

    def insercion_eliminar_panel(self):
        # Obtener el ID del cliente a eliminar desde el QLineEdit
        id_panel_a_eliminar = self.lineEdit_23.text()

        try:
            connection = psycopg2.connect(
                user=self.usuario,
                password=self.contraseña,
                host="localhost",
                port="5432",
                database="postgres"  
            )

            cursor = connection.cursor()

            # Consulta de eliminación
            delete_query = "DELETE FROM public.producto WHERE id = %s"

            # Pasar el ID del cliente como parámetro a la consulta
            cursor.execute(delete_query, (id_panel_a_eliminar,))
            connection.commit()

            # Verificar si se eliminó algún registro
            if cursor.rowcount > 0:
                QMessageBox.information(self, "Éxito", f"Cliente con ID {id_panel_a_eliminar} eliminado correctamente.")
            else:
                QMessageBox.warning(self, "Advertencia", f"No se encontró un cliente con ID {id_panel_a_eliminar}.")

        except (Exception, psycopg2.Error) as error:
            print("Error al conectar o eliminar datos:", error)
            QMessageBox.critical(self, "Error", "No se pudo eliminar cliente.")

        finally:
            # Cerrar conexión
            if connection:
                cursor.close()
                connection.close()

    def mostrar_panel(self):
        self.tabWidget.setCurrentIndex(8)
        try:
            connection = psycopg2.connect(
                user=self.usuario,
                password=self.contraseña,
                host="localhost",
                port="5432",
                database="postgres"
            )

            cursor = connection.cursor()

            select_query = "SELECT * FROM public.producto"
            cursor.execute(select_query)

            # Obtener resultados
            resultados = cursor.fetchall()

            # Configurar el número de filas y columnas en el QTableWidget
            self.tableWidget.setRowCount(len(resultados))
            self.tableWidget.setColumnCount(len(cursor.description))

            # Configurar las etiquetas de las columnas en el QTableWidget
            columnas = [desc[0] for desc in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(columnas)

            # Llenar el QTableWidget con los resultados
            for i, row in enumerate(resultados):
                for j, valor in enumerate(row):
                    item = QTableWidgetItem(str(valor))
                    self.tableWidget.setItem(i, j, item)

        except (Exception, psycopg2.Error) as error:
            print("Error al conectar o realizar la consulta:", error)
            QMessageBox.critical(self, "Error", "No se pudo obtener la información de los pedidos.")

        finally:
            # Cerrar conexión
            if connection:
                cursor.close()
                connection.close()



    

    def Agregar_proyecto(self):
        
        self.tabWidget.setCurrentIndex(6)   
    def Eliminar_proyecto(self):
        
        self.tabWidget.setCurrentIndex(7)   
       
    def realizar_insercion_proyecto(self):
        # Obtener referencias a los QLineEdit 
        id = self.lineEdit_25.text()
        fechaInicio = self.lineEdit_24.text()
        final = self.lineEdit_26.text()
        costo = self.lineEdit_27.text()
        id_cliente = self.lineEdit_28.text()
        id_panel = self.lineEdit_29.text()
        

        try:
            connection = psycopg2.connect(
                user=self.usuario,
                password=self.contraseña,
                host="localhost",
                port="5432",
                database="postgres" 
            )

            cursor = connection.cursor()

            # Consulta de inserción
            insert_query = """
                INSERT INTO public.proyecto (
                    id,
                    fechainicio,
                    fechafin,
                    costo,
                    clienteid,
                    productoid

                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                )
            """

            data = (
                id,
                fechaInicio,
                final,
                costo,
                id_cliente,
                id_panel
            )

            cursor.execute(insert_query, data)
            connection.commit()

            

            QMessageBox.information(self, "Éxito", "Proyecto agregado correctamente.")

        except (Exception, psycopg2.Error) as error:
            print("Error al conectar o insertar datos:", error)
            QMessageBox.critical(self, "Error", "No se pudo agregar Proyecto.")

        finally:
            # Cerrar conexión
            if connection:
                cursor.close()
                connection.close()

    def insercion_eliminar_proyecto(self):
        # Obtener el ID del cliente a eliminar desde el QLineEdit
        id_panel_a_eliminar = self.lineEdit_30.text()

        try:
            connection = psycopg2.connect(
                user=self.usuario,
                password=self.contraseña,
                host="localhost",
                port="5432",
                database="postgres"  
            )

            cursor = connection.cursor()

            # Consulta de eliminación
            delete_query = "DELETE FROM public.proyecto WHERE id = %s"

            # Pasar el ID del cliente como parámetro a la consulta
            cursor.execute(delete_query, (id_panel_a_eliminar,))
            connection.commit()

            # Verificar si se eliminó algún registro
            if cursor.rowcount > 0:
                QMessageBox.information(self, "Éxito", f"Cliente con ID {id_panel_a_eliminar} eliminado correctamente.")
            else:
                QMessageBox.warning(self, "Advertencia", f"No se encontró un cliente con ID {id_panel_a_eliminar}.")

        except (Exception, psycopg2.Error) as error:
            print("Error al conectar o eliminar datos:", error)
            QMessageBox.critical(self, "Error", "No se pudo eliminar cliente.")

        finally:
            # Cerrar conexión
            if connection:
                cursor.close()
                connection.close()

    def mostrar_proyecto(self):
        self.tabWidget.setCurrentIndex(8)
        try:
            connection = psycopg2.connect(
                user=self.usuario,
                password=self.contraseña,
                host="localhost",
                port="5432",
                database="postgres"
            )

            cursor = connection.cursor()

            select_query = "SELECT * FROM public.proyecto"
            cursor.execute(select_query)

            # Obtener resultados
            resultados = cursor.fetchall()

            # Configurar el número de filas y columnas en el QTableWidget
            self.tableWidget.setRowCount(len(resultados))
            self.tableWidget.setColumnCount(len(cursor.description))

            # Configurar las etiquetas de las columnas en el QTableWidget
            columnas = [desc[0] for desc in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(columnas)

            # Llenar el QTableWidget con los resultados
            for i, row in enumerate(resultados):
                for j, valor in enumerate(row):
                    item = QTableWidgetItem(str(valor))
                    self.tableWidget.setItem(i, j, item)

        except (Exception, psycopg2.Error) as error:
            print("Error al conectar o realizar la consulta:", error)
            QMessageBox.critical(self, "Error", "No se pudo obtener la información de los pedidos.")

        finally:
            # Cerrar conexión
            if connection:
                cursor.close()
                connection.close()


    def respaldo(self):
        # Configuración
        if self.usuario == "ivan":
            DB_HOST = "localhost"
            DB_PORT = "5432"
            DB_NAME = "postgres"
            DB_USER = "ivan"
            DB_PASSWORD = "messi"
            BACKUP_DIR = r"C:\Users\angel\Documents\SEMESTRE_6\adminBaseDatos\RESPALDO"



            # Nombre del archivo de respaldo
            date_str = datetime.now().strftime("%Y%m%d%H%M%S")
            backup_file = fr"{BACKUP_DIR}\respaldo_paneles.backup"

            # Comando para realizar el respaldo
            command = [
            r"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe",
                "-h", DB_HOST,
                "-p", DB_PORT,
                "-U", DB_USER,
                "-d", DB_NAME,
                "-v",
                "-F", "c",  
                "-b",
                "-f", backup_file
        ]

            try:
                subprocess.run(command, check=True)
                print(f"Respaldo exitoso. Archivo: {backup_file}")
                QMessageBox.information(self, "Éxito", f"Respaldo exitoso: {backup_file}" )
            except subprocess.CalledProcessError as e:
                print(f"Error en el respaldo: {e}")
            
        else:
            QMessageBox.critical(self, "Error", "No tienes permiso")
        

    def auditoria(self):
        if (self.usuario == "ivan"):
            self.tabWidget.setCurrentIndex(8)
            try:
                connection = psycopg2.connect(
                    user=self.usuario,
                    password=self.contraseña,
                    host="localhost",
                    port="5432",
                    database="postgres"
                )

                cursor = connection.cursor()

                select_query = "SELECT * FROM public.auditoria"
                cursor.execute(select_query)

                # Obtener resultados
                resultados = cursor.fetchall()

                # Configurar el número de filas y columnas en el QTableWidget
                self.tableWidget.setRowCount(len(resultados))
                self.tableWidget.setColumnCount(len(cursor.description))

                # Configurar las etiquetas de las columnas en el QTableWidget
                columnas = [desc[0] for desc in cursor.description]
                self.tableWidget.setHorizontalHeaderLabels(columnas)

                # Llenar el QTableWidget con los resultados
                for i, row in enumerate(resultados):
                    for j, valor in enumerate(row):
                        item = QTableWidgetItem(str(valor))
                        self.tableWidget.setItem(i, j, item)

                

            except (Exception, psycopg2.Error) as error:
                print("Error al conectar:", error)
                

            finally:
                # Cerrar conexión
                if connection:
                    cursor.close()
                    connection.close()
        else:
            QMessageBox.critical(self, "Error", "No tienes permiso")


        


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()