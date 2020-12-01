import mysql.connector, atexit, csv
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from flask_cors import CORS
from ClimateRegressionPredictor.Database.basicRegs import linReg, expReg


# dbIP = "localhost"
dbIP = "sql9.freemysqlhosting.net"
dbUser = "sql9379236"
dbPassword = "Ax3afA2tkU"

connection = mysql.connector.connect(host = dbIP,
                                    user = dbUser,
                                    password = dbPassword,
                                    database = "sql9379236",
                                    auth_plugin = 'mysql_native_password')

def exit_handler():
    connection.close()

atexit.register(exit_handler)
app = Flask(__name__)
CORS(app)

#global variables
userID = ""

@app.route('/')

@app.route('/createSimulation', methods=['GET', 'POST'])
def createSimulation():
    print("insert completed")
    results = request.get_json()
    sql_insert_Query = "INSERT INTO Simulation (SimulationName, UserID, Country) VALUES (%s, %s, %s)"
    cursor = connection.cursor()
    print(results)
    cursor.execute(sql_insert_Query, (results["simName"], results["username"], results["country"]))
    connection.commit()
    cursor.close()
    return "simulation success"

@app.route('/addNewDataPoint', methods = ['GET', 'POST'])
def addNewDataPoint():
    results = request.get_json()
    sql_find_simID = "SELECT SimulationID, Country FROM Simulation where SimulationName = %s AND UserID = %s"
    cursor = connection.cursor()
    cursor.execute(sql_find_simID, (results["simName"], results["username"]))
    records = cursor.fetchall()
    simID = records[0][0]
    country = records[0][1]
    sql_insert_Query = "INSERT INTO Datapoints (SimulationID, Year, Country, CO2Emissions) VALUES (%s, %s, %s, %s)"
    cursor = connection.cursor()
    cursor.execute(sql_insert_Query, (simID, results["year"], country, results["co2"]))
    connection.commit()
    cursor.close()
    return "success"



@app.route('/getSimulationNames', methods=['GET', 'POST'])
def getSimulationNames():
    results = request.get_json()
    sql_view_Query = "SELECT SimulationName FROM Simulation WHERE UserID = '%s'" % (results["username"])
    cursor = connection.cursor()
    cursor.execute(sql_view_Query)
    records = cursor.fetchall()
    cursor.close()
    return jsonify(records)

@app.route('/getYearData', methods=['GET', 'POST'])
def getYearData():
    results = request.get_json()
    sql_view_Query = "SELECT Year FROM Datapoints Natural Join Simulation WHERE SimulationName = %s AND UserID = %s"
    cursor = connection.cursor()
    cursor.execute(sql_view_Query, ((results["simName"],results["username"])))
    records = cursor.fetchall()
    cursor.close()
    return jsonify(records)


@app.route('/updateSimulation', methods=['GET', 'POST'])
def updateSimulation():
    results = request.get_json()
    sql_update_Query = "UPDATE Datapoints SET CO2Emissions = %s WHERE SimulationID = (SELECT SimulationID FROM Simulation WHERE SimulationName = %s AND UserID = %s) AND Year = %s"
    cursor = connection.cursor()
    cursor.execute(sql_update_Query, (results["co2"], results["simName"], results["username"], results["year"]))
    connection.commit()
    cursor.close()
    return "simulation success"

@app.route('/deleteSimulation', methods=['GET', 'POST'])
def deleteSimulation():
    results = request.get_json()
    sql_delete_Query = "DELETE FROM Simulation WHERE SimulationName = %s AND UserID = %s"
    cursor = connection.cursor()
    cursor.execute(sql_delete_Query, (results["simName"], results["username"]))
    connection.commit()
    cursor.close()
    return "simulation success"

@app.route('/viewSimulation', methods=['GET', 'POST'])
def viewSimulation():
    results = request.get_json()
    sql_view_Query = "SELECT * FROM Datapoints Natural Join Simulation WHERE SimulationName = %s AND UserID = %s"
    cursor = connection.cursor()
    cursor.execute(sql_view_Query, (results["simName"], results["username"]))
    records = cursor.fetchall()
    cursor.close()
    if (len(records) == 0):
        return "fail"
    print(records)
    dataNeeded = []
    # for i in range(len(records)):
    #     temp = []
    #     for j in range(len(records[i])):
    #         temp.append()
    return jsonify(records);

@app.route('/runSimulation', methods=['GET', 'POST'])
def runSimulation():
    results = request.get_json()
    sql_run_Query = "SELECT * FROM Datapoints Natural Join Simulation WHERE SimulationName = %s AND UserID = %s"
    cursor = connection.cursor()
    cursor.execute(sql_run_Query, (results["simName"], results["username"]))
    records = cursor.fetchall()
    cursor.close()
    if (len(records) == 0):
        return "fail"
    print(records)
    country = records[0][1]
    userInput = [[], []]
    for i in range(len(records)):
        userInput[0].append(records[i][2])
        userInput[1].append(records[i][3])
    print(userInput)
    # sql_run_Query = "SELECT Year, CO2Emissions FROM Table WHERE Country = %s"
    # cursor.execute(sql_run_Query, (country))
    # records = cursor.fetchall()
    # existingData = [[], []]
    # for i in range(len(records)):
    #     existingData[0].append(records[i][0])
    #     existingData[1].append(records[i][1])
    # lin, exp = 
    return jsonify(records);

@app.route('/signUp', methods=['GET', 'POST'])
def createUser():
    results = request.get_json()
    sql_insert_Query = "INSERT INTO User (UserID, Password) VALUES (%s, %s)"
    cursor = connection.cursor()
    cursor.execute(sql_insert_Query, (results["userID"], results["password"]))
    connection.commit()
    cursor.close()
    userID = results["userID"]
    return userID

@app.route('/logIn', methods=['GET', 'POST'])
def logIn():
    results = request.get_json()
    sql_login_query = "SELECT count(*) FROM User WHERE UserID = %s AND Password = %s"
    cursor = connection.cursor()
    cursor.execute(sql_login_query, (results["username"], results["password"]))
    records = cursor.fetchall()
    cursor.close()
    print(records[0][0])
    return str(records[0][0])

@app.route('/getUserID', methods=['GET'])
def getUserID():
    print("USER: ", userID)
    return userID

@app.route('/getCountries', methods=['GET'])
def getCountries():
    countries = set()

    with open('annual-co2-emissions-per-country.csv') as co2_data:
        csv_reader = csv.reader(co2_data, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            countries.add(row[0])
    listCountry = list(countries)
    return jsonify(listCountry)

if __name__ == "__main__":
    app.run()
