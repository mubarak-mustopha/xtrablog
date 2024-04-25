from django.shortcuts import render
from django.views import View
# Create your views here.

class HomePageView(View):
    def get(self, request):
        return render(request,"home.html",{"active":"home"})