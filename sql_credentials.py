schema = '' # database name
host = '' # host. '127.0.0.1' for a local server.
user = '' # user name. May be 'root' for a local server or 'admin' for a cloud-based server
password = '' # server password
port = 3306 # This is the MySQL Default
con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'