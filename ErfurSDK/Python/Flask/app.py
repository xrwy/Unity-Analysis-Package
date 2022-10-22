from flask import Flask, request, render_template
import sqlite3 as sql
import os
from randomDbNameGenerator import randomDbNameGenerator, punctuation

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('login-signup.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        if name.strip() == '' or password.strip() == '':
            return "Do not leave the fields blank."

        with sql.connect('db/'+ 'Users.db') as dbUsers:
            cursorUsers = dbUsers.cursor()
            cursorUsers.execute('''CREATE TABLE IF NOT EXISTS Users(User_ID INTEGER PRIMARY KEY AUTOINCREMENT, UserName TEXT, UserPassword TEXT)''')
            cursorUsers.execute('''SELECT * FROM Users''')

            dataSelf = cursorUsers.fetchall()
            if len(dataSelf) == 0:
                return "There is no such record. Register First."
              
            for user in dataSelf:
                if user[1] == name and user[2] == password:
                    with sql.connect('db/Games.db') as dbGames:
                        cursorGames = dbGames.cursor()
                        cursorGames.execute('''CREATE TABLE IF NOT EXISTS Games(Counter INTEGER,Game_ID TEXT,Game_Name)''')
                        cursorGames.execute('''SELECT * FROM Games''')
                        data = cursorGames.fetchall()
                        if len(data) == 0:
                            return render_template('games.html',games = [])

                        return render_template('games.html',games = data)

            return "Unauthorized Access."

    return "For POST Requests Only."


@app.route('/signup', methods = ['GET','POST'])
def signUp():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        if name.strip() == '' or password.strip() == '':
            return "Do not leave the fields blank."

        if len(password) < 8:
            return "Password must be minimum 8 characters."
        
        with sql.connect('db/'+ 'Users.db') as dbUsers:
            cursorUsers = dbUsers.cursor()
            cursorUsers.execute('''CREATE TABLE IF NOT EXISTS Users(User_ID INTEGER PRIMARY KEY AUTOINCREMENT, UserName TEXT, UserPassword TEXT)''')
            cursorUsers.execute('''SELECT * FROM Users''')
            if len(cursorUsers.fetchall()) == 0:
                cursorUsers.execute('''INSERT INTO Users(UserName,UserPassword) VALUES(?,?)''', [name, password])

                with sql.connect('db/Games.db') as dbGames:
                    cursorGames = dbGames.cursor()
                    cursorGames.execute('''CREATE TABLE IF NOT EXISTS Games(Counter INTEGER,Game_ID TEXT,Game_Name)''')
                    cursorGames.execute('''SELECT * FROM Games''')
                    data = cursorGames.fetchall()
                    if len(data) == 0:
                        return render_template('games.html',games = [])
                    return render_template('games.html',games = data)

            else:
                cursorUsers.execute('''SELECT * FROM Users''')
                data = cursorUsers.fetchall()
                for _user in data:
                    if _user[1] == name:
                        return "Such a record already exists."

                cursorUsers.execute('''INSERT INTO Users(UserName,UserPassword) VALUES(?,?)''', [name, password])
                    
                with sql.connect('db/Games.db') as dbGames:
                    cursorGames = dbGames.cursor()
                    cursorGames.execute('''CREATE TABLE IF NOT EXISTS Games(Counter INTEGER,Game_ID TEXT,Game_Name)''')
                    cursorGames.execute('''SELECT * FROM Games''')
                    data = cursorGames.fetchall()
                    if len(data) == 0:
                        return render_template('games.html',games = [])
                    return render_template('games.html',games = data)

    return "For POST Requests Only."


@app.route('/game_id/post', methods = ['GET','POST'])
def addNewGame():
    if request.method == 'POST':
        gameName = request.form['game-name']
        if gameName.strip() == '':
            return 'Do not leave the fields blank'
        
        if len(gameName) > 20:
            return "Game Name must be a maximum length of 20."
            
        dbName = randomDbNameGenerator() + '.db'
        
        if os.path.isdir('db'):
            with sql.connect('db/Games.db') as dbGames:
                cursorGames = dbGames.cursor()
                cursorGames.execute('''SELECT * FROM Games''')
                data = cursorGames.fetchall()
                if len(data) == 0:
                    cursorGames.execute('''CREATE TABLE IF NOT EXISTS Games(Counter INTEGER,Game_ID TEXT,Game_Name)''')
                    cursorGames.execute('''INSERT INTO Games(Counter,Game_ID,Game_Name) VALUES(?,?,?)''', [1,dbName.split('.')[0],gameName])
                else:
                    cursorGames.execute('''SELECT * FROM Games''')
                    data = cursorGames.fetchall()

                    for game in data:
                        if game[2] == gameName:
                            return "There is such a game."
                        
                    cursorGames.execute('''CREATE TABLE IF NOT EXISTS Games(Counter INTEGER,Game_ID TEXT,Game_Name)''')
                    cursorGames.execute('''INSERT INTO Games(Counter,Game_ID,Game_Name) VALUES(?,?,?)''', [len(data) + 1,dbName.split('.')[0],gameName])
                    
            with sql.connect('db/{0}.db'.format(dbName.split('.')[0])) as dbGame:
                dbGameCursor = dbGame.cursor()
                dbGameCursor.execute('''CREATE TABLE IF NOT EXISTS Game(Id INTEGER PRIMARY KEY AUTOINCREMENT, Token TEXT)''')

            with sql.connect('db/Games.db') as dbGames:
                cursorGames = dbGames.cursor()
                cursorGames.execute('''SELECT * FROM Games''')
                return render_template('games.html',games = cursorGames.fetchall())

        else:
            os.mkdir('db')
            with sql.connect('db/Games.db') as db:
                cursor = db.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS Games(Game_ID TEXT,Game_Name)''')
                cursor.execute('''INSERT INTO Games(Game_ID,Game_Name) VALUES(?,?)''', [dbName.split('.')[0],gameName])
                db.commit()

            cursor.execute('''SELECT * FROM Games''')
            return render_template('games.html',games = cursor.fetchall())


    return "For POST Requests Only."


@app.route('/<string:game_id>/get_user_id/', methods = ['GET'])
def getUserId(game_id):
    with sql.connect('db/{0}.db'.format(game_id)) as dbGame:
        dbGameCursor = dbGame.cursor()
        dbGameCursor.execute('''CREATE TABLE IF NOT EXISTS Game(Id INTEGER PRIMARY KEY AUTOINCREMENT, Token TEXT)''')
        dbGameCursor.execute('''INSERT INTO Game(Token) VALUES('') ''')

        dbGameCursor.execute('''SELECT * FROM Game''')
        data = dbGameCursor.fetchall()

        if len(data) == 1:
            return str(1)
        else:
            return str(len(data))


@app.route('/<string:game_id>/<string:user_id>/get_token/', methods = ['GET'])
def getToken(game_id, user_id):
    import sqlite3 as sql
    for file in os.listdir('db/'):
        if game_id + '.db' == file:
            with sql.connect('db/{0}.db'.format(game_id)) as dbGame:
                dbGameCursor = dbGame.cursor()
                dbGameCursor.execute('''CREATE TABLE IF NOT EXISTS Game(Id INTEGER PRIMARY KEY AUTOINCREMENT, Token TEXT)''')
                #dbGameCursor.execute('''INSERT INTO Game(Token) VALUES('') ''')
                sql = '''UPDATE Game SET Token = ? WHERE Id = ?'''
                dbGameCursor.execute(sql, [str(randomDbNameGenerator()),user_id])
                dbGameCursor.execute('''SELECT * FROM Game WHERE Id = ?''', [user_id])
                data = dbGameCursor.fetchone()

                return str(data[1])
                
    return "There is no db named {0}.db".format(game_id)


@app.route('/<string:url>', methods = ['GET'])
def gameInformations(url):
    columnNamesArray = []
    valuesArray = []
    for file in os.listdir('db/'):
        if url + '.db' == file:
            with sql.connect('db/{0}.db'.format(url)) as dbGame:
                dbGameCursor = dbGame.cursor()
                getColumnNames = '''SELECT ColumnNames.name FROM pragma_table_info('Game') ColumnNames;'''
                dbGameCursor.execute(getColumnNames)
                columnNames = dbGameCursor.fetchall()           
                columnNamesArray.append(columnNames)

                query = '''SELECT * FROM Game'''
                dbGameCursor.execute(query)
                data_ = dbGameCursor.fetchall() 
                
                if len(data_) == 0:
                    valuesArray = []
                    return render_template('Game_Results.html', columnNamesArray = columnNamesArray, valuesArray = valuesArray)   
                elif len(data_) == 1:
                    return render_template('Game_Results.html', columnNamesArray = columnNamesArray, valuesArray = data_)
                else:
                    for x in data_:
                        valuesArray.append(x)


                    return render_template('Game_Results.html', columnNamesArray = columnNamesArray, valuesArray = valuesArray)
                
    return "There is no db named {0}.db".format(url)


@app.route('/game_id', methods = ['POST'])
def updateOrAddValue():
    import sqlite3 as sql
    if request.method == "POST":
        gameId = request.form.get('game_id')
        userId = request.form.get('id')
        token_ = request.form.get('token')
        key_ = request.form.get('key')
        value_ = request.form.get('value')

        if gameId == '' or userId == '' or token_ == '' or key_ == '' or value_ == '':
            return "Do not leave the fields blank."
        
        if len(key_) > 30:
            return "Maximum Length Must Be 20 Characters."

        key_ = ''.join(key_.split(' '))

        for file in os.listdir('db/'):
            if gameId + '.db' == file:
                with sql.connect('db/{0}.db'.format(gameId)) as dbGame:
                    dbGameCursor = dbGame.cursor()
                    dbGameCursor.execute('''SELECT * FROM Game WHERE Id = ?''', [int(userId)])
                    data = dbGameCursor.fetchall()
                    for data_ in data:
                        if data_[1] == token_:
                            try:
                                getColumnNames = '''SELECT ColumnNames.name FROM pragma_table_info('Game') ColumnNames;'''
                                dbGameCursor.execute(getColumnNames)
                                columnNames = dbGameCursor.fetchall()
                                
                                for columnName in columnNames:
                                    if columnName[0] == key_:
                                        query = '''UPDATE Game SET {0} = ? WHERE Id = ?'''.format(key_)
                                        if value_.isdigit():
                                            value_ = float(value_)

                                        dbGameCursor.execute(query, [value_, int(data_[0])])
                                        return "True"
                                

                                splitValue = [val for val in key_]

                                for val in splitValue:
                                    newPunctuation = punctuation()
                                    newPunctuation.append('-')

                                    if val in newPunctuation:
                                        return "Value Cannot Be Special Character. Must be a Decimal Value."
                                                    
                                dbGameCursor.execute('''ALTER TABLE Game ADD {0}'''.format(key_))
                                
                                query = '''UPDATE Game SET {0} = ? WHERE Id = ?'''.format(key_)
                                if value_.isdigit():
                                    value_ = float(value_)

                                dbGameCursor.execute(query, [value_, int(data_[0])])
                                return "True"


                            except Exception as e:
                                return "False"

                    return "There is no such token."

        return "There is no db named {0}.db".format(gameId)


@app.route('/game_id_', methods = ['POST'])
def increaseOrAddValue():
    import sqlite3 as sql
    if request.method == "POST":
        gameId = request.form.get('game_id')
        userId = request.form.get('id')
        token_ = request.form.get('token')
        key_ = request.form.get('key')
        value_ = request.form.get('value')

        
        if gameId == '' or userId == '' or token_ == '' or key_ == '' or value_ == '':
            return "Do not leave the fields blank."
        
        if len(key_) > 30:
            return "Maximum Length Must Be 20 Characters."

        key_ = ''.join(key_.split(' '))
        
        if value_ == True or value_ == False or value_.lower() == 'true' or value_.lower() == 'false':
            return "You cannot enter a boolean value."

        elif value_.startswith('.') or value_.endswith('.'):
            return 'Enter the Value Correctly.'
            
        elif value_.isdigit():
            value_ = float(value_)

        elif value_.isalpha():
            return "Value Cannot Contain Characters. Must be decimal"
        
        elif value_.isalnum():
            return "Value Cannot Contain Both Characters and Numbers. Must be decimal"
        
        elif value_.endswith('-'):
            return 'Enter the Value Correctly.'

        elif len(value_.split('.')) == 2 and value_.split('.')[1] == '':
                return 'Enter the Value Correctly.'
        else:
            if value_.count('.') >= 2:
                return "Must be a Decimal Value."

            splitValue = [val for val in value_]

            for val in splitValue:
                if val == '.':
                    continue
                else:
                    if val in punctuation():
                        return "Value Cannot Be Special Character. Must be a Decimal Value."


        if str(value_).isdecimal():
            if len(value_.split('-')) == 2 and value_.split('-')[1] != '':
                splitValue = [val for val in value_]
                for val in splitValue:
                    if val == '.':
                        continue
                    elif val in punctuation():
                        return "Value Cannot Be Special Character. Must be a Decimal Value."

                
            elif value_.count('-') > 1:
                return 'Enter the Value Correctly.'

        if not str(value_).isdecimal():
                value_ = float(value_)
                

        for file in os.listdir('db/'):
            if gameId + '.db' == file:
                with sql.connect('db/{0}.db'.format(gameId)) as dbGame:
                    dbGameCursor = dbGame.cursor()
                    dbGameCursor.execute('''SELECT * FROM Game WHERE Id = ?''', [str(userId)])
                    data = dbGameCursor.fetchall()
                    for data_ in data:
                        if data_[1] == token_:
                            try:
                                getColumnNames = '''SELECT ColumnNames.name FROM pragma_table_info('Game') ColumnNames;'''
                                dbGameCursor.execute(getColumnNames)
                                columnNames = dbGameCursor.fetchall()
                                for columnName in columnNames:
                                    if columnName[0] == key_:
                                        getColumnNames = '''SELECT {0} FROM Game WHERE Id = ?'''.format(key_)
                                        res = dbGameCursor.execute(getColumnNames, [int(data_[0])]).fetchall()
                                        
                                        if res[0][0] == None:
                                            query = '''UPDATE Game SET {0} = ? WHERE Id = ?'''.format(key_)
                                            dbGameCursor.execute(query, [value_, int(data_[0])])
                                            return "True"

                                        else:
                                            trueOrFalse = True
                                            if str(res[0][0]).count('.') == 1:
                                                trueOrFalse = True

                                            elif trueOrFalse:
                                                for i in res[0][0]:
                                                    if i.isdigit():
                                                        trueOrFalse = True
                                                    else:
                                                        trueOrFalse = False
                                                        break
                                            

                                            if trueOrFalse:
                                                res_ = float(res[0][0])

                                                query = '''UPDATE Game SET {0} = ? WHERE Id = ?'''.format(key_)

                                                newValue = float(value_) + float(res_)
                                                dbGameCursor.execute(query, [newValue, int(data_[0])])
                                                return "True"
                                                
                                            elif res[0][0].isalpha():
                                                query = '''UPDATE Game SET {0} = ? WHERE Id = ?'''.format(key_)

                                                newValue = float(value_)
                                                dbGameCursor.execute(query, [newValue, int(data_[0])])
                                                return "True"

                                            elif res[0][0].isalnum():
                                                query = '''UPDATE Game SET {0} = ? WHERE Id = ?'''.format(key_)

                                                newValue = float(value_)
                                                dbGameCursor.execute(query, [newValue, int(data_[0])])
                                                return "True"
   
                                            else:
                                                newValue__ = ''
                                                splitValue = [val for val in res[0][0]]
                                                
                                                for val in splitValue:
                                                    newPunctuation = punctuation()
                                                    newPunctuation.append('-')
                                                    
                                                    if val in newPunctuation:
                                                        newValue__ += str(val)
                                                    else:
                                                        newValue__ += str(val)

                                                res_ = newValue__
                                                
                                                if res_ != '':
                                                    query = '''UPDATE Game SET {0} = ? WHERE Id = ?'''.format(key_)

                                                    newValue = float(value_)
                                                    dbGameCursor.execute(query, [newValue, int(data_[0])])
                                                    return "True"
                                        
                                
                                splitValue = [val for val in key_]

                                for val in splitValue:
                                    newPunctuation = punctuation()
                                    newPunctuation.append('-')

                                    if val in newPunctuation:
                                        return "Value Cannot Be Special Character. Must be a Decimal Value."
                                                    
                                dbGameCursor.execute('''ALTER TABLE Game ADD {0}'''.format(key_))
                                query = '''UPDATE Game SET {0} = ? WHERE Id = ?'''.format(key_)
                                dbGameCursor.execute(query, [value_, int(data_[0])])
                                return "True"

                            except Exception as e:
                                return str(e)

                    return "There is no such token."
                            
        return "There is no db named {0}.db".format(gameId)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

