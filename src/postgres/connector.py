import psycopg2
import threading
import yaml

from typing import Tuple
class Connector:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if Connector.__instance is not None:
            raise Exception("Cannot create two connectors!")
        
        with open("config/database.yaml") as database_config_obj:
            self.database_config = yaml.safe_load(database_config_obj)

        self.connector = psycopg2.connect(
            database = self.database_config["DATABASE"], 
                        user = self.database_config["USER"], 
                        host= self.database_config["HOST"],
                        password = self.database_config["PASSWORD"],
                        port = self.database_config["PORT"]
                    )
        
    @staticmethod
    def get_instance():
        with Connector.__lock:
            if Connector.__instance is None:
                Connector.__instance = Connector()
                
            return Connector.__instance
        
    def cursor(self):
        return self.connector.cursor()
    
    def insert_card(self, data: Tuple[str, str, str, str, str, str]):
        query = "INSERT INTO card(card_id, user_id, hook, description, thread_id, create_time) values('" + "', '".join(data) + "');"
        _cursor = self.cursor()
        _cursor.execute(query=query)
        self.connector.commit()
        _cursor.close()

    def insert_message(self, data: Tuple[str, str, str, str]):
        query = "INSERT INTO message(message_id, thread_id, content, create_time) values('" + "', '".join(data) + "');"
        _cursor = self.cursor()
        _cursor.execute(query=query)
        self.connector.commit()
        _cursor.close()