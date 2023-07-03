from django.shortcuts import render

def test(request):
    return render(request,"template.html",{"data":{"name":"Nischal","age": 12}})
    