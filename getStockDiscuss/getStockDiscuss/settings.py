# -*- coding: utf-8 -*-

BOT_NAME 			= 'getStockDiscuss'
SPIDER_MODULES 		= ['getStockDiscuss.spiders']
NEWSPIDER_MODULE 	= 'getStockDiscuss.spiders'
ITEM_PIPELINES 		= {'getStockDiscuss.pipelines.MongoDBPipeline': 1000, }

DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
	'getStockDiscuss.rotate_useragent.RotateUserAgentMiddleware' :400
}

# put your mongoDB's account info
MONGODB_SERVER	= "etc-dbs"
MONGODB_PORT = 27017
MONGODB_DB 	= "memo"
MONGODB_COLLECTION 	= "stockInfo"
DOWNLOAD_DELAY = 30
CONCURRENT_REQUESTS = 1