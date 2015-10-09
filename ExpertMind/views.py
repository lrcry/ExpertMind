from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from user import User

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
#
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
#
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
#
#


def user_register(request, user_name):
    user = User(user_name)
    hometown = user.get_user('yun-user-id')
    print hometown
    return HttpResponse("User name is %s, hometown is" % user_name)
    # return HttpResponse("User name is %s, hometown is" % user_name)
