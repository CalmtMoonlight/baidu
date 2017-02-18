# 【yun】 说明
1. 一个非官方的【百度网盘】资源转存接口,实现【链接--验证码】对应资源的转存
2. 用法：

```Python
>>>urls = [
        ('https://pan.baidu.com/s/1pLCQkQn', '89yi'),
        ("https://pan.baidu.com/s/1o8lNEkU", 'tthx'),
    ]
>>>yun = Yun(urls[0])          #传入元组
>>>yun.save("/test")           #网盘路径必须存在
'''success!'''

```