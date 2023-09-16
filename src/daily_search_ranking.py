import psycopg2
from config.db_info import db_params

def daily_search_ranking():
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    search_query = """

        SELECT keyword, RANK() OVER (ORDER BY MAX(created_datetime) DESC, COUNT(*) DESC) AS search_rank
        FROM search_log_keywords
        WHERE keyword IN (
            SELECT DISTINCT item
            FROM (
                SELECT name_org as item FROM artist
                UNION ALL
                SELECT name_org as item FROM track
                UNION ALL
                SELECT name_org as item FROM album
            ) AS items
            WHERE item IS NOT NULL
        )
        GROUP BY keyword
        ORDER BY search_rank;

    """

    
    cursor.execute(search_query)
    search_ranking = cursor.fetchall()

    result = {}
    rank = 1
    
    for _, (keyword, search_rank) in enumerate(search_ranking):
        result[rank] = keyword
        rank += 1
            
        if rank >= 20:  # 20위까지만 결과 저장
            break
    connection.close()
    return result

