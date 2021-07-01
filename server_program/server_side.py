import base64
import socket
import threading
import pymysql
import pickle
import sys




# function that handles communication with a single user
def newUserHandler(conn, addr):
    try:
        while True:
            request = conn.recv(1024).decode()
            request = tuple(request.split(":"))
            if request[0] == "Users":
                cursor.execute("Select * from users")
                conn.send(pickle.dumps(cursor.fetchall()))
                continue
            if request[0] == "Usernames":
                cursor.execute("Select userName from users")
                conn.send(pickle.dumps(cursor.fetchall()))
                continue
            elif request[0] == "New user":
                new_user_info = pickle.loads(conn.recv(1024))
                sql_query = str(
                    "INSERT INTO `users`(`firstName`, `lastName`, `userName`, `email`, `phone`, `password`, `admin`) " +
                    "VALUES ('" + new_user_info.firstName + "','" + new_user_info.lastName + "','" + new_user_info.username + "','"
                    + new_user_info.phone + "','" + new_user_info.email + "','" + new_user_info.password + "','" + new_user_info.admin + "')")
                cursor.execute(sql_query)
                database.commit()
                if cursor.rowcount > 0:
                    conn.send("Successful".encode())
                continue
            elif request[0] == "LoginCredentials":
                sql_query = str("SELECT * from users WHERE username='" + request[1] + "'and password='" + request[2] + "'")
                cursor.execute(sql_query)
                conn.send(pickle.dumps(cursor.fetchone()))
                continue
            elif request[0] == "Reservations":
                sql_query = str("SELECT * from reservations WHERE user_id=%s" % request[1])
                cursor.execute(sql_query)
                a = cursor.fetchall()
                conn.send(pickle.dumps(a))
                continue
            elif request[0] == "CarInfo":
                sql_query = str("SELECT * from cars WHERE id=%s" % request[1])
                cursor.execute(sql_query)
                conn.send(pickle.dumps(cursor.fetchone()))
                continue
            elif request[0] == "DeleteReservation":
                sql_query = str("DELETE from reservations WHERE id=%d" % int(request[1]))
                if cursor.execute(sql_query):
                    conn.send("Successful".encode())
                    database.commit()
                else:
                    conn.send("Failed".encode())
                continue
            elif request[0] == "DeleteAllReservationsForUser":
                sql_query = str("DELETE from reservations WHERE user_id=%d" % int(request[1]))
                if cursor.execute(sql_query):
                    conn.send("Successful".encode())
                    database.commit()
                else:
                    conn.send("Failed".encode())
                continue
            elif request[0] == "Cars":
                sql_query = "SELECT * from cars"
                cursor.execute(sql_query)
                result = cursor.fetchall()
                conn.send(str(len(result)).encode())
                for car in result:
                    print(car)
                    conn.send(pickle.dumps(car))
                continue
            elif request[0] == "NewReservation":
                id, carId, userId, pickUpDate, dropOffDate = pickle.loads(conn.recv(1024))
                sql_query = "INSERT INTO `reservations`(`car_id`, `user_id`, `pick_up_date`, `drop_off_date`)" \
                            "VALUES ('" + str(carId) + "','" + str(userId) + "','" + str(pickUpDate) + "','" + str(dropOffDate) + "')"
                if cursor.execute(sql_query) > 0:
                    conn.send("Successful".encode())
                    database.commit()
                continue
            elif request[0] == "ChangeUserInfo":
                idUser = request[1]
                none, firstName, lastName, username, phone, email, password, admin = pickle.loads(conn.recv(1024))
                sql_query = "UPDATE `users` SET `firstName`= '" + firstName + "',`lastName`='" + lastName + "'," \
                            "`userName`='" + username + "',`email`='" + email + "',`phone`='" + phone + "',`password`='" + password + \
                            "',`admin`='" + admin + "' WHERE id = '" + idUser + "'"
                cursor.execute(sql_query)
                conn.send("Successful".encode())
                database.commit()
                continue
            elif request[0] == "ReservationsOfCar":
                sql_query = "SELECT * from reservations WHERE car_id =" + request[1]
                cursor.execute(sql_query)
                conn.send(pickle.dumps(cursor.fetchall()))
                continue
            elif request[0] == "AllReservations":
                sql_query = "SELECT * from reservations"
                cursor.execute(sql_query)
                conn.send(pickle.dumps(cursor.fetchall()))
                continue
            elif request[0] == "UserInfo":
                sql_query = str("SELECT * from users where id='%s'" % request[1])
                cursor.execute(sql_query)
                conn.send(pickle.dumps(cursor.fetchone()))
                continue
            elif request[0] == "DeleteUser":
                sql_query = str("DELETE from reservations WHERE user_id=%d" % int(request[1]))
                sql_query2 = str("DELETE FROM users where id=%d" % int(request[1]))
                if cursor.execute(sql_query) >= 0 and cursor.execute(sql_query2) > 0:
                    conn.send("Successful".encode())
                    database.commit()
                else:
                    conn.send("Failed".encode())
                    database.rollback()
                continue
            elif request[0] == "CarsName":
                sql_query = "SELECT manufacturer,model from cars"
                cursor.execute(sql_query)
                conn.send(pickle.dumps(cursor.fetchall()))
                continue
            elif request[0] == "ReservationsForUsername":
                sql_query = str("SELECT * from reservations where user_id=(SELECT id from users where userName='%s')" % request[1])
                cursor.execute(sql_query)
                conn.send(pickle.dumps(cursor.fetchall()))
                continue
            elif request[0] == "ReservationsForCar":
                manufacturer, model = request[1].split(" ")
                sql_query = str("SELECT * from reservations where car_id=(SELECT id from cars where manufacturer='%s' and model='%s')" % (manufacturer, model))
                cursor.execute(sql_query)
                conn.send(pickle.dumps(cursor.fetchall()))
                continue
            elif request[0] == "UpdateCar":
                result = pickle.loads(conn.recv(1700000))
                sql_query = "UPDATE `cars` SET `image` = %s where id = %s"
                sql_query2 = str("UPDATE `cars` SET `manufacturer`='%s',`model`='%s',`engine_power`='%s', " \
                            "`engine_displacement`='%s',`car_body`='%s',`price`='%s' WHERE id='%s'"
                                % (result[2], result[3], int(result[5]), int(result[4]), result[6], int(result[7]), result[0]))
                cursor.execute(sql_query, (result[1], result[0]))
                cursor.execute(sql_query2)
                database.commit()
                conn.send("Successful".encode())
            elif request[0] == "NewCar":
                result = pickle.loads(conn.recv(1700000))
                sql_query = str("INSERT INTO `cars`(`manufacturer`, `model`, `engine_power`, `engine_displacement`, `car_body`, `price`) " \
                            "VALUES ('%s','%s','%s','%s','%s','%s')" % (result[2], result[3], int(result[5]), int(result[4]), result[6], int(result[7])))
                sql_query2 = "SELECT last_insert_id()"
                cursor.execute(sql_query)
                cursor.execute(sql_query2)
                addedCarId = cursor.fetchone()[0]
                cursor.execute("UPDATE `cars` SET `image` = %s where id = %s", (result[1], addedCarId))
                database.commit()
                conn.send("Successful".encode())

    except ConnectionError:
        print("User: %s,\naddr: %s\nDisconnected." % (conn, addr))



# Creating a connection with database
try:
    database = pymysql.connect(host='localhost', port=3306, user="root", db="TestDriveDatabase")
    cursor = database.cursor()
except:
    print("ERROR! Server can't make connection to the database! Check if the MYSQL server is up and try again!")
    sys.exit()
# Main Thread
# Creating socket for accepting connections
try:
    server_socket = socket.socket()
    PORT = 2020
    HOST = socket.gethostname()
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    # Creating new connection for every new user connected
    while True:
        conn, addr = server_socket.accept()
        t1 = threading.Thread(target=lambda: newUserHandler(conn, addr))
        t1.daemon = True
        t1.start()
except:
    print("ERROR! Can't create server host!")