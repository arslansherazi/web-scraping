import psycopg2


def insert_laptop_details(details, price, image_url):
    conn = psycopg2.connect("host=localhost port=5432 dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO laptop_details (details, price, image_url) VALUES (%s, %s, %s)",
        (details, price, image_url)
    )
    conn.commit()
    cur.close()
    conn.close()