import pymysql
# config is not a real module, it is just a user file with the MySQL credentials
import config


# basis for class taken from
# https://medium.com/@vipinc.007/python-a-database-interaction-class-using-pymysql-3338fb90f38c
class MySQLModule:
    # MySQL database credentials stored in user created config file
    # To use this code yourself, you need to get rid of the import config
    # statement and replace the parameters of the connect statement with
    # your MySQL database credentials
    def __connect__(self):
        self.connection = pymysql.connect(host=config.HOST,
                                          user=config.USER,
                                          password=config.PASS,
                                          charset=config.CHARSET)
        self.cursor = self.connection.cursor()

    def __disconnect__(self):
        self.connection.close()

    # gets the results of a valid MySQL command
    def fetch(self, cmd, commit=False, args=()):
        self.execute(cmd, commit, args)
        fetch_result = self.cursor.fetchall()
        return fetch_result

    # executes a MySQL command
    def execute(self, cmd, commit=False, args=()):
        self.__connect__()
        exception_found = False
        if len(args) == 0:
            try:
                self.cursor.execute(cmd)
            except pymysql.err.IntegrityError:
                print("Error executing command: " + cmd)
                exception_found = True
        else:
            try:
                self.cursor.execute(cmd, args)
            except pymysql.err.IntegrityError:
                print("Error executing command: " + cmd + " with args: %s" % (args,))
                exception_found = True
        # only if the command needs to be committed
        if commit:
            if not exception_found:
                self.connection.commit()
        self.__disconnect__()

    def insert_ping_val(self, ping):
        cmd = "INSERT INTO ping_database.ping_data (time_value, ping_value) VALUES" \
              "(%s, %s)"
        self.execute(cmd, True, (ping[0], ping[1],))

    def get_ping_values(self):
        cmd = "SELECT * FROM ping_database.ping_data"
        return self.fetch(cmd)

    def init_database(self):
        cmd = "CREATE DATABASE IF NOT EXISTS ping_database"
        self.execute(cmd)

        cmd = "DROP TABLE IF EXISTS ping_database.ping_data"
        self.execute(cmd)

        cmd = "CREATE TABLE ping_database.ping_data (time_value INT(5), ping_value INT(5))"

        self.execute(cmd)


if __name__ == '__main__':
    module = MySQLModule()

    module.init_database()
