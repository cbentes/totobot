import time
import pymongo


class DataManager:

    def __init__(self, user, password, host='127.0.0.1', port='27017'):
        url_db = 'mongodb://{0}:{1}'.format(host, port)
        client = pymongo.MongoClient(url_db)
        self.db = client['totobot']
        self.db.authenticate(user, password)

    def log_data(self, input_data, label):
        logger_db = self.db['logger']
        _data = {'log': input_data, 'timestamp': int(time.time()), 'label': label}
        logger_db.insert(_data)
