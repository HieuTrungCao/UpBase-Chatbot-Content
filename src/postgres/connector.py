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
    
    def insert_thread(self, _cursor, data: str):
        query = "INSERT INTO thread(thread_id) values('" + data + "') ON CONFLICT (thread_id) DO NOTHING;"
        _cursor.execute(query=query)
        self.connector.commit()

    def insert_content(self, data: Tuple[str, str, str, str, str, str]):
        
        query = "INSERT INTO content(card_id, user_id, hook, description, thread_id, create_time) values('" + "', '".join(data) + "');"
        _cursor = self.cursor()
        self.insert_thread(_cursor, data[4])
        _cursor.execute(query=query)
        self.connector.commit()
        _cursor.close()

    def insert_message(self, data: Tuple[str, str, str, str]):
        query = "INSERT INTO messages(message_id, thread_id, content, create_time) values('" + "', '".join(data) + "');"
        _cursor = self.cursor()
        _cursor.execute(query=query)
        self.connector.commit()
        _cursor.close()

    def insert_policy(self, data: Tuple[str, str, str, str, str, str]):
        
        query = "INSERT INTO policy(card_id, user_id, content, thread_id, create_time) values('" + "', '".join(data) + "');"
        print("Query.: ", query)
        _cursor = self.cursor()
        self.insert_thread(_cursor, data[3])
        _cursor.execute(query=query)
        self.connector.commit()
        _cursor.close()