# -*- coding: utf-8 -*-

import time
import os
import json
import logging

from datetime import datetime
from flask import Flask, request
from flask_restful import Api, Resource
from colorama import Style, Fore, init

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
            tempDt = {
                "misc": "chicken"
            }
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
            # NOTE: Debug thingy curl http://127.0.0.1:5000/get?q=chick
            Console().Log(f"The category Parameter is None, Reserting to all categories.")
            # Console().Log(f"Getting Database contents")
            Console().Log(f"Getting Database contents and searching")
            DataList = list()
            resps = dict()
            for i in data:
                for k in data[i]:
                    # DataList.append(k)
                    if k.lower().__contains__(query.lower()) or k.lower().startswith(query.lower()):
                        if not i in resps:
                            resps[i] = []
                        resps[i].append(k)
            # Console().Log(f"Got {len(DataList)} Variables. Searching")
            # resp = list()
            # for i in DataList:
            #     if i.lower().__contains__(query.lower()) or i.lower().startswith(query.lower()):
            #         resp.append(i)
            # Console().Log(f"Returning {len(resp)} Results.")
            Console().Log(f"Returning {len(resps)} Results.\n")
            return resps

class API_Endpoints:
    class Get(Resource):
        def get(self):
            query = request.args.get("q")
            cate = request.args.get("category")
            res = JSONDatabase().Get(query, cate)
            try:
                res["suggestions"][cate]
            except KeyError:
                cate = "all"
            if cate == None or cate == "" or cate == " ":
                cate = "all"
            return {"query": query, "suggestions": res, "category": cate}

server = Flask(__name__)
api = Api(server)

api.add_resource(API_Endpoints.Get, "/get")

if __name__ == '__main__':
    # os.system("cls")
    server.run(debug=True)
