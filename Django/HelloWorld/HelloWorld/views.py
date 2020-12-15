from django.shortcuts import render
import datetime

def runoob(request):
    context = 'Hello World! 模板'
    views_name = "夏天吃西瓜"
    views_list = ["夏天吃西瓜1", "夏天吃西瓜2", "夏天吃西瓜3"]
    views_dict = {"name": "夏天吃西瓜"}
    view_str = "<a href='https://www.baidu.com/'>夏天吃西瓜个人博客</a>"
    times = datetime.datetime.now()
    views_listInfo = ["a", "b", "c", "d", "e"]
    views_listInfo2 = []
    return render(request, "runoob.html",
                  {
                      "name": views_name,
                      "hello":context,
                      "views_list":views_list,
                      "views_dict":views_dict,
                      "default":0,
                      "numlist":1024,
                      "time": times,
                      "views_str": "夏天吃西瓜",
                      "views_str2": view_str,
                      "num":88,
                      "listvar":views_listInfo,
                      "listvar2":views_listInfo2
                  })
