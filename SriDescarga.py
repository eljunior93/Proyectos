import pyodbc

direccion_servidor = 'fuentes\\ia2012'
nombre_bd = 'piazza'
nombre_usuario = 'sa'
password = 'ishida2021'
try:
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                              direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
    # OK! conexión exitosa
except Exception as e:
    # Atrapar error
    print("Ocurrió un error al conectar a SQL Server: ", e)