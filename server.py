from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()

app= Flask(__name__)

app.config['MYSQL_DB']= os.getenv('MYSQL_DB')
app.config['MYSQL_HOST']= os.getenv('MYSQL_HOST')
app.config['MYSQL_USER']= os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD']= os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_PORT']= int(os.getenv('MYSQL_PORT'))

mysql= MySQL(app)

#CASO N°1
@app.route('/ventas/<year>', methods= ['GET'])
def get_ventas(year):
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM ventas WHERE year(ord_date) like %s', (year,))
    ventas= cur.fetchall()
    ventas_json= [{"stor_id" : stor_id, "ord_num": ord_num, "ord_date" : ord_date, "qty" : qty, "payterms": payterms, "title_id" : title_id} 
                    for stor_id, ord_num, ord_date, qty, payterms, title_id in ventas]
    cur.close()
    return jsonify({ "Ventas" : ventas_json})

#CASO N°2
@app.route('/libros/<tipo>', methods= ['GET'])
def get_libros(tipo):
    cur= mysql.connection.cursor()
    cur.execute("SELECT title, type FROM titulos WHERE type = %s", (tipo,))    
    libros= cur.fetchall()
    libros_json= [{"title" : title, "type": type} for title, type in libros]
    cur.close()
    return jsonify({"Libros" : libros_json})

#CASO N°3
@app.route('/editorial', methods= ["POST"])
def agregar_editorial():
    datos= request.get_json()
    pub_id= datos.get('pub_id')
    pub_name= datos.get('pub_name')
    city= datos.get('city')
    state= datos.get('state')
    country= datos.get('country')
    cur= mysql.connection.cursor()
    cur.execute('INSERT INTO editoriales (pub_id, pub_name, city, state, country) VALUES (%s, %s, %s, %s, %s)', (pub_id, pub_name, 
                                                                                                   city, state, country))
    mysql.connection.commit()
    return jsonify({"mensaje" : "Registro agregado"})

#CASO N°4 
@app.route('/editoriales/<pais>')
def get_editoriales(pais):
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM editoriales WHERE country = %s', (pais,))
    editoriales= cur.fetchall()
    cur.close()
    json_editoriales= [{"pub_id" : pub_id, "pub_name" : pub_name, "city" : city, "state" : state, "country" : country}
                       for pub_id, pub_name, city, state, country in editoriales]
    return jsonify({"editoriales" : json_editoriales})

if __name__ == ('__main__'):
    app.run(debug=True, port=5000)    