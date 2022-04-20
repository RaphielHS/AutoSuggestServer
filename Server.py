# -*- coding: utf-8 -*-
# NOTE: This is stil unstable

__version__ = 'b0.0.2'

import requests
import os
import time
import json
import logging
import sqlite3
import hashlib
import base64

from datetime import datetime
from flask import Flask, request
from flask_restful import Api, Resource
from colorama import Style, Fore, init

class Encryption:
    def SHA256Encrypt(self, message) -> str:
        return hashlib.sha256(message.encode()).hexdigest()

    def Base64Encrypt(self, message) -> str:
        return base64.b64encode(message.encode('ascii')).decode('ascii')

    def Base64Decrypt(self, message) -> str:
        return base64.b64decode(message.encode('ascii')).decode('ascii')

    def CheckSamiliarity(self, str1, str2) -> dict:
        resp = dict()
        isSamiliar = False
        if self.SHA256Encrypt(str1) == self.SHA256Encrypt(str2):
            isSamiliar = True
        resp[str1] = {"SHA256-hash": self.SHA256Encrypt(str1), "Base64-hash": self.Base64Encrypt(str1), "samiliar": isSamiliar}
        resp[str2] = {"SHA256-hash": self.SHA256Encrypt(str2), "Base64-hash": self.Base64Encrypt(str2), "samiliar": isSamiliar}
        return resp

class Auth:
    def __init__(self):
        if not os.path.exists("./database/admin/users/"):
            os.makedirs("./database/admin/users/")
        db = sqlite3.connect("./database/admin/users/users.db")
        cur = db.cursor()

        with db:
            cur.execute("""CREATE TABLE IF NOT EXISTS Admins(
                ID INTEGER,
                username REAL,
                password REAL,
                Lastused REAL
            )""")

    def GetPassword(self, username):
        if not os.path.exists("./database/admin/users/"):
            os.makedirs("./database/admin/users/")
        db = sqlite3.connect("./database/admin/users/users.db")
        cur = db.cursor()

        with db:
            cur.execute("""CREATE TABLE IF NOT EXISTS Admins(
                ID INTEGER,
                username REAL,
                password REAL,
                Lastused REAL
            )""")
        passws = cur.execute("SELECT password FROM Admins WHERE (username=username)", {"username": username}).fetchone()
        try:
            return passws[0]
        except:
            return ""

    def ExecuteAdminQueryDatabase(self, query, params):
        try:
            if not os.path.exists("./database/admin/users/"):
                os.makedirs("./database/admin/users/")
            db = sqlite3.connect("./database/admin/users/users.db")
            cur = db.cursor()

            with db:
                cur.execute("""CREATE TABLE IF NOT EXISTS Admins(
                    ID INTEGER,
                    username REAL,
                    password REAL,
                    Lastused REAL
                )""")
            with db:
                cur.execute(query, param)
            return True
        except:
            return False

    def CheckUser(self, username, password) -> bool:
        passw = self.GetPassword(username)
        if passw != None or passw != " " or passw != "":
            if passw == password:
                return True
        else:
            return False

class Logging:
    __isInit__ = False;
    def __init__(self):
        if Logging.__isInit__ == False:
            if not os.path.exists('./logs/'):
                print("Making Logs folder...")
                os.makedirs('./logs/')

            print(f"{Style.BRIGHT}[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {Fore.GREEN}{Fore.GREEN}[LOGGING]{Fore.RESET} - Resetting Info log{Style.RESET_ALL}")
            open("./logs/info.log", "w").write(" ")

            print(f"{Style.BRIGHT}[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {Fore.GREEN}{Fore.GREEN}[LOGGING]{Fore.RESET} - Resetting Warning log{Style.RESET_ALL}")
            open("./logs/warning.log", "w").write(" ")

            print(f"{Style.BRIGHT}[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {Fore.GREEN}[LOGGING]{Fore.RESET} - Resetting Error log{Style.RESET_ALL}")
            open("./logs/error.log", "w").write(" ")

            print(f"{Style.BRIGHT}[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {Fore.GREEN}[LOGGING]{Fore.RESET} - Resetting Critical log{Style.RESET_ALL}")
            open("./logs/critical.log", "w").write(" ")
            Logging.__isInit__ = True

        logging.basicConfig(filename="./logs/info.log", level=logging.INFO, format=f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - %(message)s")
        logging.basicConfig(filename="./logs/warning.log", level=logging.WARNING, format=f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - %(message)s")
        logging.basicConfig(filename="./logs/error.log", level=logging.ERROR, format=f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - %(message)s")
        logging.basicConfig(filename="./logs/critical.log", level=logging.CRITICAL, format=f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - %(message)s")

    def info(self, content) -> str:
        try:
            logging.info(content)
            return "Success"
        except Exception as e:
            return e

    def error(self, content) -> str:
        try:
            logging.error(content)
            return "Success"
        except Exception as e:
            return e

    def warning(self, content) -> str:
        try:
            logging.warning(content)
            return "Success"
        except Exception as e:
            return e

    def critical(self, content) -> str:
        try:
            logging.critical(content)
            return "Success"
        except Exception as e:
            return e

class Console:
    def __init__(self):
        init()

    def Log(self, message):
        Logging().info(message)
        print(f"{Style.BRIGHT}[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {Fore.GREEN}[LOG]{Fore.RESET} - {message}{Style.RESET_ALL}")

    def Error(self, message):
        Logging().error(message)
        print(f"{Style.BRIGHT}[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {Fore.RED}[ERR]{Fore.RESET} - {message}{Style.RESET_ALL}")

    def Critical(self, message):
        Logging().critical(message)
        print(f"{Style.BRIGHT}[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {Fore.RED}[CRIT]{Fore.RESET} - {message}{Style.RESET_ALL}")

    def Warning(self, message):
        Logging().warning(message)
        print(f"{Style.BRIGHT}[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {Fore.RED}[WARN]{Fore.RESET} - {message}{Style.RESET_ALL}")

class JSONDatabase:
    def __init__(self):
        self._directory = "./database/"
        try:
            Console().Log("Checking if Database folder exists")
            if not os.path.exists(self._directory):
                Console().Log("Database Folder dosent exists, Creating Database folder")
                os.makedirs(self._directory)
                Console().Log("Database folder Created")
            else:
                Console().Log("Database folder exists")
        except Exception as e:
            Console().Error(e)
        Console().Log("Checking Database file")
        if not os.path.exists("./database/database.json"):
            Console().Log("Database File dosent exists, Creating Database file")
            tempDt = {}
            with open("./database/database.json", "w+") as f:
                json.dump(tempDt, f, ensure_ascii=False, indent=4)
            Console().Log("Database file created")
        else:
            Console().Log("Database file exixts")

    def Get(self, query, category=None):
        all = False
        if category == "" or category == " " or category == None:
            category = None
            all = True
        Console().Log(f"Getting information from database")
        data = None
        with open("./database/database.json", 'r') as f:
            data = json.loads(f.read())
        if category != None:
            Console().Log(f"Category Parameter is NOT None. Checking if the category {category} Exists")
            try:
                data[category]
                Console().Log(f"Category {category} Exists, loading values")
                cate = data[category]
                Console().Log(f"Seaching in Category, Keyword={query}")
                resp = list()
                for i in cate:
                    if i.lower().__contains__(query.lower()):
                        resp.append(i)
                Console().Log(f"Returning {len(cate)} Items from the Category={category} with keyword={query}")
                return resp
            except Exception as e:
                if type(e) == KeyError:
                    Console().Log(f"Category {category} Does NOT Exists, Switching to All")
                    all = True
                else:
                    Console().Error(f"Unknown Error has occured when trying check if the category {category} Exists, Err: {e}\n")
                    return None
        if all:
            Console().Log(f"The category Parameter is None, Reserting to all categories.")
            Console().Log(f"Getting Database contents and searching")
            DataList = list()
            resps = dict()
            for i in data:
                for k in data[i]:
                    if k.lower().__contains__(query.lower()) or k.lower().startswith(query.lower()):
                        if not i in resps:
                            resps[i] = []
                        resps[i].append(k)
            Console().Log(f"Returning {len(resps)} Results.\n")
            return resps

class AdminControl:
    def __init__(self):
        if not os.path.exists("./database/admin/users/"):
            os.makedirs("./database/admin/users/")
        db = sqlite3.connect("./database/admin/users/users.db")
        cur = db.cursor()

        with db:
            cur.execute("""CREATE TABLE IF NOT EXISTS Admins(
                ID INTEGER,
                username REAL,
                password REAL,
                Lastused REAL
            )""")

    def GetIDs(self):
        db = sqlite3.connect("./database/admin/users/users.db")
        cur = db.cursor()
        return cur.execute("SELECT ID FROM Admins").fetchall()

    def GetUsernames(self):
        db = sqlite3.connect("./database/admin/users/users.db")
        cur = db.cursor()
        return cur.execute("SELECT username FROM Admins").fetchall()

    def AddAdmin(self, username, rawPassword):
        db = sqlite3.connect("./database/admin/users/users.db")
        cur = db.cursor()
        id = len(self.GetIDs())
        for i in self.GetUsernames():
            if i[0] == username:
                return {"Message": "user already exists"}
        with db:
            cur.execute("INSERT INTO Admins(ID, username, password, Lastused) VALUES (?,?,?,?)",
                (id + 1, username, Encryption().SHA256Encrypt(rawPassword), datetime.now()))
            return {"Message": "added a new admin: " + username}

class API_Endpoints:
    class Get(Resource):
        def get(self):
            query = request.args.get("q")
            cate = request.args.get("category")
            if query == "" or query == None or query == " ":
                return {"message": "Query is empty."}
            res = JSONDatabase().Get(query, cate)
            try:
                res["suggestions"][cate]
            except KeyError:
                cate = "all"
            if cate == None or cate == "" or cate == " ":
                cate = "all"
            return {"query": query, "suggestions": res, "category": cate}

    class AdminDatabase:
        class AddToDatabase(Resource):
            def post(self):
                JSONDatabase()
                try:
                    data = json.loads(str(request.data.decode()))
                    username = data["auth"]["cred"]["username"]
                    passw = data["auth"]["cred"]["password"]
                    Console().Log("Checking Admin Cred")
                    if Auth().CheckUser(username, passw):
                        dt = data["data"]
                        cate = dt["category"]
                        cateVal = dt["categoryValues"]
                        duplicates = []
                        with open("./database/database.json", 'r') as f:
                            dts = json.load(f)
                        Console().Log("Checking Category")
                        try:
                            dts[cate]
                        except:
                            dts[cate] = []
                        Console().Log("Checking for duplicates")
                        for i in dts[cate]:
                            if isinstance(cateVal, list):
                                for r in cateVal:
                                    if i.lower() == r.lower():
                                        cateVal.append(i)
                                        break
                            else:
                                try:
                                    if i.lower() == cateVal.lower():
                                        Console().Warning("key [" + i + "] Already Exists")
                                        return {"Message": "The key already exists in the database"}
                                except Exception as e:
                                    Console().Error("key [" + i + "] Unknown error, " + e)
                                    return {"Error": "Unknown Error"}
                        Console().Log("Checking Value Type")
                        if isinstance(cateVal, list):
                            for i in cateVal:
                                if not duplicates.__contains__(cateVal):
                                    Console().Log("Adding Value [" + i + "] to Category " + cate)
                                    dts[cate].append(i)
                                else:
                                    Console().Warning("Duplicate [" + i + "] Found")
                        else:
                            Console().Log("Adding Value [" + cateVal + "] to Category " + cate)
                            if not duplicates.__contains__(cateVal):
                                dts[cate].append(cateVal)
                            else:
                                Console().Warning("Duplicate [" + i + "] Found")
                        Console().Log("Saving Database and writing...\n")
                        with open("./database/database.json", 'w') as f:
                            json.dump(dts, f, indent=4, ensure_ascii=False)
                        return {"Message": "Added Items Successfully"}
                    return {"Message": "Invalid JSON data"}
                except Exception as e:
                    if type(e) == KeyError:
                        return {"Message": "Invalid JSON Data"}
                    return {"Message": e}

def main():
    server = Flask(__name__)
    api = Api(server)

    api.add_resource(API_Endpoints.Get, "/get")
    api.add_resource(API_Endpoints.AdminDatabase.AddToDatabase, "/admin/database/add")

    Console().Warning(f"{Fore.RED}THIS IS STILL UNSTABLE, I (RaphielHS) DO NOT TAKE RESPONSIBILITY FOR ANY DATA THAT IS LOST.")
    time.sleep(3)
    Console().Log("Checking for Updates")
    r = requests.get("https://raw.githubusercontent.com/RaphielHS/AutoSuggestServer/main/__version__").text
    if r != __version__:
        Console().Warning(f"This Version of the server is Outdated. Please update at https://github.com/RaphielHS/AutoSuggestServer")
        time.sleep(3)
    else:
        Console().Log(f"This Version of the server is up to date")

    server.run(debug=True)

if __name__ == '__main__':
    main()
