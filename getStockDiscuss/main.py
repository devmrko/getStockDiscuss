import scrapy.cmdline

def main():
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'getStockDiscuss'])

if __name__ == '__main__':
    main()