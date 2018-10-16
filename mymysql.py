import  MySQLdb

def dbConnect():    
    db = MySQLdb.connect("localhost","root","root","innov" )
    cursor = db.cursor()
    sql = """ CREATE TABLE IF NOT EXISTS users (id  INT NOT NULL AUTO_INCREMENT,
                email  VARCHAR(25),
                series VARCHAR(100),PRIMARY KEY(id));"""

    cursor.execute(sql)
    return db
def insertData(db,email,series):
    sql="INSERT INTO users(email,series) VALUES('%s','%s')"%(email,series)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

