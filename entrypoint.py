from scrapy.cmdline import execute

# 抓取section
# execute(['scrapy', 'crawl', 'changzhiserver'])

# 抓取section内容
# execute(['scrapy', 'crawl', 'changzhiServerPage'])


# 抓取 News
execute(['scrapy', 'crawl', 'changzhiserverNews'])


