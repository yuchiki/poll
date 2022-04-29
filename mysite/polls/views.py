from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You are at the polls index.")


def details(request, question_id):
    return HttpResponse(f"You're looking at question {question_id}")


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")
