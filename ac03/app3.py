import os
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mudar123'
app.config['MYSQL_DATABASE_DB'] = 'teste'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.2'
#app.config['MYSQL_DATABASE_HOST'] = '172.17.0.7'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showRegister')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _category = request.form['inputcategory']
        _price = request.form['inputprice']

        print(_name)
        print(_category)
        print(_price)

        # validate the received values
        if _name and _category and _price:
            
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('insert into tbl_user (_name, _category, _price) VALUES (%s, %s, %s)', ( _name,_category,_price))
            conn.commit()

            return render_template('signup.html')
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route('/list',methods=['POST','GET'])
def list():
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute ('select _name, _category, _price from tbl_user')
            data = cursor.fetchall()
            print(data[0]);

            conn.commit()
            return render_template('signup2.html', datas=data)

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
