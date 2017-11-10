根据Scrapy的官方文档，当抓取太频繁，就可能被封IP.为了解封,目前有这几种策略：

- 策略1：设置download_delay下载延迟，数字设置为5秒，越大越安全
- 策略2：禁止Cookie，某些网站会通过Cookie识别用户身份，禁用后使得服务器无法识别爬虫轨迹
- 策略3：使用user agent池。也就是每次发送的时候随机从池中选择不一样的浏览器头信息，防止暴露爬虫身份
- 策略4：使用IP池，这个需要大量的IP资源，貌似还达不到这个要求

每个策略都用上还是获取不到数据,但是使用普通的Requests+BeautifulSoup可以实现爬虫

参考

[如何让你的scrapy爬虫不再被ban](https://www.cnblogs.com/rwxwsblog/p/4575894.html)

[scrapy爬虫与动态页面——爬取拉勾网职位信息（2）](http://blog.csdn.net/hk2291976/article/details/51405052)

[Scrapy抓取拉勾网招聘信息（二）](http://www.jianshu.com/p/39b0a1b65f14)

队列Queue知识

[一个简单的多线程Python爬虫](http://www.cnblogs.com/mr-zys/p/5059451.html)

