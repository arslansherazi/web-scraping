import psycopg2


class BasePipeline(object):
    def __init__(self, settings):
        self.connection = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgres",
            dbname="postgres"
        )
        self.cursor = self.connection.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)


class BeautyProductsPipeline(BasePipeline):
    def process_item(self, item, spider):
        try:
            query = """
                INSERT INTO beauty_product (name, description, rating, total_ratings, price, image_url) 
                VALUES (%s, %s, %s, %s, %s, %s) 
            """
            self.cursor.execute(query, (
                item.get('name'),
                item.get('description'),
                item.get('rating'),
                item.get('total_ratings'),
                item.get('price'),
                item.get('image_url')
            ))
            self.connection.commit()
        except Exception as e:
            print(e)
        return item


class LaptopDetailsPipeline(BasePipeline):
    def process_item(self, item, spider):
        try:
            query = """
                INSERT INTO laptop_details (details, price, image_url) 
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (
                item.get('details'),
                item.get('price'),
                item.get('image_url')
            ))
            self.connection.commit()
        except Exception as e:
            print(e)
        return item
