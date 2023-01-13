import pymysql
# import mysql.connector
#
# dataBase = mysql.connector.connect(
#     host="localhost",
#     user="ilya",
#     passwd="228pidorgandon"
# )
#
# # preparing a cursor object
# cursorObject = dataBase.cursor()
#
# # creating database
# cursorObject.execute("CREATE DATABASE db_django")
pymysql.install_as_MySQLdb()