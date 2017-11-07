1.下载Scrapy

    sudo pip3 install scrapy
    
2.开启一个新的Scrapy项目

    scrapy startproject crawler

3.使用genspider创建Spider
    
    scrapy genspider douban douban.com 

3.1项目默认结构

    .
    ├── crawler
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── __pycache__
    │   ├── settings.py
    │   └── spiders
    │       ├── __init__.py
    │       └── __pycache__
    └── scrapy.cfg
    
4.在spiders/laguo.py 编码

    # -*- coding: utf-8 -*-
    import scrapy
    from scrapy.conf import settings
    from login.items import MovieInfoItem,ImageItem
    
    class DoubanSpider(scrapy.Spider):
        name = 'douban'
        allowed_domains = ['douban.com']
        start_urls = ['https://accounts.douban.com/login', ]
    
        form_data = {
            'form-email': '',
            'form-password': '',
            'redir': 'https://www.douban.com',
            'source': 'index_nav',
            'login': '登录',
        }
        def parse(self, response):
            pass


4.1因为爬取豆瓣电影TOP250需要登录,所以需要在获取之前进行登录操作,那么就要重写start\_requests();start\_request()是在parse之前进行的操作
    
    def start_requests(self):
        return [
            scrapy.Request(url=self.start_urls[0],
                           headers=settings['DEFAULT_REQUEST_HEADERS'],
                           meta={'cookiejar': 1},
                           callback=self.parse_validate_image
                           )]
                          
4.2如果有验证码的话,调用parse\_validate\_image;但这只是手动输入验证码

    def parse_validate_image(self, response):
        if 'captcha_image' in str(response.body):
            print('Copy the link:')
            link = response.xpath('//img[@id="captcha_image"]/@src').extract()[0]
            print(link)
            captcha_solution = input('captcha-solution:')
            # python2.7
            # captcha_id = urlparse.parse_qs(urlparse.urlparse(link).query, True)['id']
            captcha_id = link.split("?")[1].split(":")[0].split("=")[1]

            self.form_data['captcha-solution'] = captcha_solution
            self.form_data['captcha-id'] = captcha_id
        client_headers = settings['DEFAULT_REQUEST_HEADERS']
        client_headers['Host']='accounts.douban.com'
        print (client_headers)
        return [scrapy.FormRequest.from_response(response,
                                                 formdata=self.form_data,
                                                 headers=client_headers,
                                                 meta={'cookiejar': response.meta['cookiejar']},
                                                 callback=self.parsefs
                                                 )]
    
4.3登录之后跳转的页面不是Top250,所以这个时候就要跳转到电影Top250并获取到想要的数据

    def parsefs(self, response):
        print(response.status)
        print(response.meta['cookiejar'])

        client_headers = settings['DEFAULT_REQUEST_HEADERS']
        client_headers['Host'] = 'movie.douban.com'
        print(client_headers)
        yield scrapy.Request(url="https://movie.douban.com/top250",
                             meta={'cookiejar':response.meta['cookiejar']},
                             headers = client_headers,
                             callback=self.parse_top,
                             )

    def parse_top(self,response):
        movieinfoItem=MovieInfoItem()
        for x in response.xpath("//div[@class='info']"):
            title=x.xpath("div[@class='hd']/a/span[1]/text()").extract()[0]
            star=x.xpath("div[@class='bd']/div[1]/span[2]/text()").extract()[0]
            movie_url=x.xpath("div[@class='hd']/a/@href").extract()[0]
            movieinfoItem['movie_name']=title
            movieinfoItem['movie_star']=star
            movieinfoItem['movie_url']=movie_url
            yield movieinfoItem
    
5 运行并保存数据
    
    scrapy crawl douban -o xx.json
    
    

## Scarpy图片的抓取

1.定义Item

    class ImageItem(scrapy.Item):
        image_urls=scrapy.Field()
        images=scrapy.Field()
        image_path=scrapy.Field()
        

2.设置条件和属性

    ITEM_PIPELINES = {
       'login.pipelines.MyImagesPipeline': 300,
    }
    IMAGES_STORE='/pythontext/'
    IMAGES_EXPIRES = 90
    IMAGES_MIN_HEIGHT=100
    IMAGES_MIN_WIDTH=100
    
3.修改parse\_top

    def parse_top(self,response):
        imageItem=ImageItem()
        # 查找了相关的文档，了解到使用ImagesPipeline传入的url地址必须是一个list，在传入一个list的时候pipeline处理的速度要快得多，
        item=[] 
        for x in response.xpath("//div[@class='item']"):
            images_urls=x.xpath("div[@class='pic']/a/img/@src").extract()[0]
            item.append(images_urls)
        imageItem['image_urls']=item
        return imageItem

4.ImagePipeline    
    
    class MyImagesPipeline(ImagesPipeline):
        def get_media_requests(self, item, info):
            client_headers = settings['DEFAULT_REQUEST_HEADERS']
            client_headers['Host'] = 'movie.douban.com'
            for image_url in item['image_urls']:
                yield Request(image_url)
    
        def item_completed(self, results, item, info):
            image_paths = [x['path'] for ok, x in results if ok]
            if not image_paths:
                raise DropItem("Item contains no images")
            item['image_paths'] = image_paths
            return item


#### 说明
    
需要在自定义的 ImagePipeline 类中重载的方法: 

get\_media\_requests(item,info) 和 item\_completed(results, items, info)

Pipeline 将从 item 中获取图片的 URLs 并下载它们,所以必须
重载 get\_media\_requests ,并返回一个 Request 对象,这些请求对象将被
Pipeline 处理,当完成下载后,结果将发送到 item\_completed 方法,这些结果
为一个二元组的 list ,每个元祖的包含 (success,
image\_info\_or\_failure) 。
- success : boolean 值, true 表示成功下载
- image_info_or_error :如果 success=true , image_info_or_error
词典包含以下键值对。失败则包含一些出错信息。

    - url :原始 URL
    - path:本地存储路径
    - checksum :校验码
    
    

已有前辈用Requests和BeautifulSoup爬取豆瓣电影TOP250

[Web crawler with Python - 03.豆瓣电影TOP250](https://zhuanlan.zhihu.com/p/20423182)



参考链接
[解决ValueError('Missing scheme in request url: %s' % self._url)](http://blog.csdn.net/lcyong_/article/details/72858453)
[kaokao2011 为知笔记](https://github.com/rockyfire/Crawler/blob/master/scrapy%E5%9B%BE%E7%89%87%E6%8A%93%E5%8F%96_by_hanxiaoyang.pdf)


