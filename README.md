# scrapy

## Important Commands
Create new scrapy project
~~~
scrapy startproject project_name_here

Example:
scrapy startproject scraper
~~~

Create new spider
~~~
scrapy genspider spider_name_here domain_here

Example:
scrapy genspider daraz_smart_phones daraz.pk
~~~

Start crawling spider
~~~
scrapy crawl spider_name_here

Example:
scrapy crawl daraz_smart_phones
~~~
