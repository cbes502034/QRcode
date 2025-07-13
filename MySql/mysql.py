import pymysql
class SQL:
    def __init__(self,USER,PASSWORD,HOST,PORT,DATABASE):
        self.user = USER
        self.password = PASSWORD
        self.host = HOST
        self.port = PORT
        self.database = DATABASE
    def execute(self,instruction, SELECT=False, SET=None):
        con = pymysql.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port = self.port,
            database=self.database
            )
        cur = con.cursor()
        if SELECT:
            cur.execute(instruction, SET)
            result = cur.fetchall()
            con.close()
            return result
        else:
            if SET:
                cur.execute(instruction, SET)
            else:
                cur.execute(instruction)
            con.commit()
            con.close()