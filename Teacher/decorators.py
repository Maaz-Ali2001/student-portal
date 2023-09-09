import functools
from django.shortcuts import render,redirect

def session_check(function):
    session_key = "Teacher_login"
    @functools.wraps(function)
    def wrapper(self,request,*args,**kwargs):
        login_url = "teacher:login"
        if session_key in request.session:
            return function(self,request,*args,**kwargs)
        else:
            return redirect(login_url)

    return wrapper