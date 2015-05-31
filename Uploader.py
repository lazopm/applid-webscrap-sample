import mysql.connector
import json
import time
def checkrows():
    cnx = mysql.connector.connect(user='seerk', password='',
                              host='mysql.server',
                              database='seerk$rutdata')
    cursor = cnx.cursor()

    get_range = ("SELECT (t1.rut + 1) as gap_starts_at, (SELECT MIN(t3.rut) -1 FROM data t3 WHERE t3.rut > t1.rut) as gap_ends_at FROM data t1 WHERE NOT EXISTS (SELECT t2.rut FROM data t2 WHERE t2.rut = t1.rut + 1) HAVING gap_ends_at IS NOT NULL")
    cursor.execute(get_range)
    array=[]
    for gap in cursor.fetchall():
        array+=list(range(gap[0],(gap[1]+1)))
    cursor.close()
    cnx.close()
    return array
def getruts(start, end):
    cnx = mysql.connector.connect(user='seerk', password='lolazo',
                              host='mysql.server',
                              database='seerk$rutdata')
    cursor = cnx.cursor()

    get_range = ("SELECT rut FROM data WHERE rut BETWEEN %s AND %s")
    data_range = (start,end)
    cursor.execute(get_range, data_range)
    array = [item[0] for item in cursor.fetchall()]
    cursor.close()
    cnx.close()
    return array
def checkrut(rut):
    for n in range(100):
        try:
            cnx = mysql.connector.connect(user='seerk', password='lolazo',
                                      host='mysql.server',
                                      database='seerk$rutdata')
            cursor = cnx.cursor()

            get_range = ("SELECT rut FROM data WHERE rut = "+str(rut))
            cursor.execute(get_range)
            break
        except:
            time.sleep(1)
            pass
    if cursor.fetchone():
        cursor.close()
        cnx.close()
        return 1
    else:
        cursor.close()
        cnx.close()
        return 0
def updata(rut, data):
    json_data=json.dumps(data)
    for _ in range(5):
        try:
            cnx = mysql.connector.connect(user='seerk', password='lolazo',
                                          host='mysql.server',
                                          database='seerk$rutdata')
            cursor = cnx.cursor()

            add_rut = ("INSERT INTO data "
                           "(rut, data) "
                           "VALUES (%s,%s"
                           ")ON DUPLICATE KEY UPDATE data=VALUES(data)")

            data_rut = (rut,json_data)


            cursor.execute(add_rut, data_rut)

            cnx.commit()

            cursor.close()
            cnx.close()
        except:
            pass

def uperror(rut, err):
    cnx = mysql.connector.connect(user='seerk', password='lolazo',
                                  host='mysql.server',
                                  database='seerk$rutdata')
    cursor = cnx.cursor()

    add_rut = ("INSERT INTO error "
                   "(rut, error) "
                   "VALUES (%s,%s"
                   ")ON DUPLICATE KEY UPDATE error=VALUES(error)")

    data_rut = (rut,err)


    cursor.execute(add_rut, data_rut)

    cnx.commit()

    cursor.close()
    cnx.close()
