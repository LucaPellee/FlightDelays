from database.DB_connect import DBConnect
from model.airport import Airport
from model.collegamento import Collegamento


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(minimo, map):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select tmp.ID, tmp.IATA_CODE, count(*) as N
                    from (
                    SELECT a.ID , a.IATA_CODE , f.AIRLINE_ID, count(*) as n
                    FROM airports a , flights f 
                    WHERE a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID 
                    group by a.ID , a.IATA_CODE , f.AIRLINE_ID
                    ) as tmp
                    group by tmp.ID, tmp.IATA_CODE
                    having N >= %s"""

        cursor.execute(query, (minimo,))

        for row in cursor:
            result.append(map[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(minimo, map):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as numero
    from flights f,
    (select tmp.ID as idAir, tmp.IATA_CODE, count( *) as N
    from (SELECT a.ID, a.IATA_CODE, f.AIRLINE_ID, count( *) as n FROM airports a, flights f
    WHERE a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID
    group by a.ID, a.IATA_CODE, f.AIRLINE_ID) as tmp
    group by tmp.ID, tmp.IATA_CODE
    having N >= %s) as tab,
    (select tmp2.ID as idAir2, tmp2.IATA_CODE, count( *) as N2 from (SELECT a.ID, a.IATA_CODE, f.AIRLINE_ID, count( *) as n
    FROM airports a, flights f
    WHERE
    a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID
    group by a.ID, a.IATA_CODE, f.AIRLINE_ID) as tmp2
    group by tmp2.ID, tmp2.IATA_CODE
    having N2 >= %s) as tab2
where f.ORIGIN_AIRPORT_ID = tab.idAir and f.DESTINATION_AIRPORT_ID = tab2.idAir2
group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID"""

        cursor.execute(query, (minimo, minimo,))

        for row in cursor:
            result.append(Collegamento(map[row["ORIGIN_AIRPORT_ID"]], map[row["DESTINATION_AIRPORT_ID"]], int(row["numero"])))

        cursor.close()
        conn.close()
        return result

