from django.shortcuts import render, redirect
from .models import Pay, studentcheck, VocabularyPreview, U10R1VocabularyPreviewAns, U10R2VocabularyPreviewAns
from .models import BeforeYouRead, U10BeforeYouReadAns, FocusOnContent, U10R1FocusonContentAns, U10R2FocusonContentAns
from .models import VocabularyReview, U10R1VocabularyReviewAns, U10R2VocabularyReviewAns, VocabularyDetail, SetNaoIP, SetStartTime
from .models import CustomizeStudentList, CustomizeVocabulary, CustomizeQuiz, CustomizeClassInfo, CustomizeReading, CustomizeExerciseInfo, CustomizeDiscussion
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.db.models import Q
from django.core import serializers

section = ["section", "section", "section", "section", "section"]
vocabularylist = []


def pay(request):

    if request.method == 'POST':
        item_spend = request.POST.get('item_spend')
        id = request.POST.get('id')
        money = request.POST.get('money')
        year = request.POST.get('year')
        month = request.POST.get('month')
        day = request.POST.get('day')
        isPri = request.POST.get('isPri')
        fun = request.POST.get('fun')
        if fun == '1':
            Pay.objects.create(id=id, item_spend=item_spend, money=money, year=year, month=month, day=day, isPri=isPri)
            try:
                t = Pay.objects.get(id=id)
                return HttpResponse("add_ok")
            except ObjectDoesNotExist:
                return HttpResponse("add_error")
        elif fun == '2':
            try:
                temp = Pay.objects.get(id=id)
                temp.delete()
                return HttpResponse("delete_ok")
            except ObjectDoesNotExist:
                return HttpResponse("not_found")
    else:
        return HttpResponse("error")

# ?????????????????????
def homepage(request):
    return render(request, "homepage.html", locals())

# ??????Nao IP???url
def setnaoipNET(request):
    naoip = request.GET.get('ip')
    SetNaoIP.objects.create(IPAddress=naoip)
    print(naoip+"?????????")
    return JsonResponse({'result': 'Save Successfully'})

# ????????????????????????
def setclassstarttime(request):
    starttime = request.GET.get('starttime')
    print(parse_datetime(starttime))
    SetStartTime.objects.create(starttime=starttime)
    return JsonResponse({'result': 'Save Successfully'})

# ?????????????????????????????????Nao IP?????????
def getnaoipNET(request):
    newestrecord = SetNaoIP.objects.all().last()
    print(newestrecord.IPAddress)
    return JsonResponse({'IP': newestrecord.IPAddress})

# ???????????????????????????????????????????????????
def getnextstarttime(request):
    newestrecord = SetStartTime.objects.all().last()
    print(newestrecord.starttime)
    if timezone.now() < newestrecord.starttime:
        timecomparison = "notyet"
    elif (timezone.now() - newestrecord.starttime).total_seconds() > 3600:
        timecomparison = "Expired"
    else:
        timecomparison = "OK"
    return JsonResponse({'starttime': str(newestrecord.starttime), 'timecomparison': timecomparison})

# Just Say Hello
def sayhello(request):

    return HttpResponse("Hello django !")

# Say Hello too
def hello2(request,username):

    return HttpResponse("Hello " + username)

# ???????????????????????????
def naoindexNET(request):
    return render(request, "naoindex.html", locals())

# ??????
@csrf_exempt
def home(request):
    nextstarttime = SetStartTime.objects.all().last()
    if timezone.now() < nextstarttime.starttime:
        result = "???????????????????????????????????????????????????????????????????????????"
    elif (timezone.now() - nextstarttime.starttime).total_seconds() > 3600:
        result = "???????????????????????????????????????????????????"
    else:
        result = "????????????????????????????????????????????????????????????????????????"
    return render(request, "home.html", locals())

# ?????????????????? ????????????Students??????
def checkstudentNET(request):

    checkedstudent1 = studentcheck.objects.filter(cGroup='1').order_by('id')
    checkedstudent2 = studentcheck.objects.filter(cGroup='2').order_by('id')
    checkedstudent3 = studentcheck.objects.filter(cGroup='3').order_by('id')
    checkedstudent4 = studentcheck.objects.filter(cGroup='4').order_by('id')
    checkedstudent5 = studentcheck.objects.filter(cGroup='5').order_by('id')
    checkedstudent6 = studentcheck.objects.filter(cGroup='6').order_by('id')

    errormessage = " (???????????? !)"
    return render(request, "uncheckedstudent.html", locals())

# ???????????????????????????????????????
def getstudentchecksituation(request):

    idlist = ['', '', '', '', '', '']
    checksituationlist = ['', '', '', '', '', '']
    group = request.GET.get('group')
    week = request.GET.get('week')
    index = 0
    groupstudent = studentcheck.objects.filter(cGroup=group).order_by('id')
    for student in groupstudent:
        idlist[index] = student.cId
        if week == '1':
            checksituationlist[index] = student.FirstweekCheck
        elif week == '2':
            checksituationlist[index] = student.SecondweekCheck
        elif week == '3':
            checksituationlist[index] = student.ThirdweekCheck
        elif week == '4':
            checksituationlist[index] = student.ForthweekCheck
        else:
            print("Error")
        index += 1
    print(idlist)
    print(checksituationlist)
    return JsonResponse({'cId1': idlist[0], 'cId2': idlist[1], 'cId3': idlist[2], 'cId4': idlist[3], 'cId5': idlist[4], 'cId6': idlist[5],
                         'check1': checksituationlist[0], 'check2': checksituationlist[1], 'check3': checksituationlist[2], 'check4': checksituationlist[3], 'check5': checksituationlist[4], 'check6': checksituationlist[5]})

# ???????????????????????????
def editcheck(request):

    cId = request.GET.get('cId')
    week = request.GET.get('week')
    print("??????", cId, "???????????? ???")

    t = studentcheck.objects.get(cId=cId)
    try:
        if week == '1':
            if t.FirstweekCheck == '?????????':
                t.FirstweekCheck = '????????????'
                t.save()
                print("??????")
            elif t.FirstweekCheck == '????????????':
                t.FirstweekCheck = '?????????'
                t.save()
                print("??????")
        elif week == '2':
            if t.SecondweekCheck == '?????????':
                t.SecondweekCheck = '????????????'
                t.save()
                print("??????")
            elif t.SecondweekCheck == '????????????':
                t.SecondweekCheck = '?????????'
                t.save()
                print("??????")
        elif week == '3':
            if t.ThirdweekCheck == '?????????':
                t.ThirdweekCheck = '????????????'
                t.save()
                print("??????")
            elif t.ThirdweekCheck == '????????????':
                t.ThirdweekCheck = '?????????'
                t.save()
                print("??????")
        elif week == '4':
            if t.ForthweekCheck == '?????????':
                t.ForthweekCheck = '????????????'
                t.save()
                print("??????")
            elif t.ForthweekCheck == '????????????':
                t.ForthweekCheck = '?????????'
                t.save()
                print("??????")
        return JsonResponse({"responsemessage": "????????????"})
    except:
        return JsonResponse({"responsemessage": "????????????"})

# ????????????Zenbo Junior?????????views????????????
def studentcheckNET(request):

    groupzenbo = request.GET.get('zenbo')
    cId = request.GET.get('cId')
    print("??????", cId)
    week = request.GET.get('week')
    print("???", week, "???")
    t = studentcheck.objects.get(cId=cId)
    if int(groupzenbo) == t.cGroup:
        if week == '1':
            t.FirstweekCheck = "?????????"
        if week == '2':
            t.SecondweekCheck = '?????????'
        if week == '3':
            t.ThirdweekCheck = '?????????'
        if week == '4':
            t.ForthweekCheck = '?????????'
        t.save()
        print("????????????")
        return JsonResponse({'cId': t.cId, 'cName': t.cName, 'cGroup': t.cGroup})
    else:
        return JsonResponse({'cId': t.cId, 'cName': t.cName, 'cGroup': t.cGroup})

# ??????????????????
def pluspointNET(request):

    cId = request.GET.get('cId')
    print("??????", cId, "????????????")
    try:
        t = studentcheck.objects.get(cId=cId)
        t.point += 1
        t.save()
        print("??????")
        return JsonResponse({"responsemessage": "????????????"})
    except:
        return JsonResponse({"responsemessage": "????????????"})

# ??????????????????
def subpointNET(request):

    cId = request.GET.get('cId')
    print("??????", cId, "????????????")
    try:
        t = studentcheck.objects.get(cId=cId)
        t.point -= 1
        t.save()
        print("??????")
        return JsonResponse({"responsemessage": "????????????"})
    except:
        return JsonResponse({"responsemessage": "????????????"})

# ??????????????????
def randompickstudentNET(request):

    group = request.GET.get('group')
    week = request.GET.get('week')
    print(group+"  "+week)
    num = 0
    if week == '1':
        while True:
            students = studentcheck.objects.filter(cGroup=group, FirstweekCheck="?????????", picked=num).order_by(
                '?')
            if students.count() > 0:
                print("a")
                t = students.first()
                break
            else:
                print("c")
                num += 1
            # elif not students.exists():
            #     print("b")
            #     return JsonResponse({'result': 'Error ! ???????????????????????????'})
    elif week == '2':
        while True:
            if group == 'all':
                students = studentcheck.objects.filter(SecondweekCheck="?????????", picked=num).order_by('?')
            else:
                students = studentcheck.objects.filter(cGroup=group, SecondweekCheck="?????????", picked=num).order_by(
                    '?')
            if students.count() > 0:
                t = students.first()
                break
            elif not students.exists():
                return JsonResponse({'picked': 'Error ! ???????????????????????????'})
            else:
                num += 1
    elif week == '3':
        while True:
            students = studentcheck.objects.filter(cGroup=group, ThirdweekCheck="?????????", picked=num).order_by(
                    '?')
            if students.count() > 0:
                t = students.first()
                break
            elif not students.exists():
                return JsonResponse({'picked': 'Error ! ???????????????????????????'})
            else:
                num += 1
    elif week == '4':
            while True:
                students = studentcheck.objects.filter(cGroup=group, ForthweekCheck="?????????", picked=num).order_by(
                    '?')
                if students.count() > 0:
                    t = students.first()
                    break
                elif not students.exists():
                    return JsonResponse({'picked': 'Error ! ???????????????????????????'})
                else:
                    num += 1
    t.picked += 1
    t.save()
    print("??????????????????" + t.cName)
    return JsonResponse({'result': t.cName})

# reading ??????
def readingNET(request):

    return render(request,"readaloud.html",locals())

# before you read ??????????????????
def beforeyoureadresultNET(request):

    try:
        unit = request.GET.get('unit')
        print("unit", unit)
        if unit == '10':
            for i in range(1, 5):
                if i == 1:
                    question = BeforeYouRead.objects.get(unit=unit, number=1)
                    studentans = U10BeforeYouReadAns.objects.filter(q1answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q1answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q1answer=question.option3)
                    question.numof3 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q1answer=question.option4)
                    question.numof4 = studentans.count()
                    question.save()
                elif i == 2:
                    question = BeforeYouRead.objects.get(unit=unit, number=2)
                    studentans = U10BeforeYouReadAns.objects.filter(q2answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q2answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q2answer=question.option3)
                    question.numof3 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q2answer=question.option4)
                    question.numof4 = studentans.count()
                    question.save()
                elif i == 3:
                    question = BeforeYouRead.objects.get(unit=unit, number=3)
                    studentans = U10BeforeYouReadAns.objects.all()
                    if studentans.count() != 0:
                        question.numof1 = 0
                        question.numof2 = 0
                        question.numof3 = 0
                        question.numof4 = 0
                        question.numof5 = 0
                        question.save()
                        question = BeforeYouRead.objects.get(unit=unit, number=3)
                        for j in range(0, studentans.count()):
                            studentansset = U10BeforeYouReadAns.objects.all()[j]
                            if question.option1 in studentansset.q3answer:
                                question.numof1 = question.numof1 + 1
                            if question.option2 in studentansset.q3answer:
                                question.numof2 = question.numof2 + 1
                            if question.option3 in studentansset.q3answer:
                                question.numof3 = question.numof3 + 1
                            if question.option4 in studentansset.q3answer:
                                question.numof4 = question.numof4 + 1
                            if question.option5 in studentansset.q3answer:
                                question.numof5 = question.numof5 + 1
                    question.save()
                elif i == 4:
                    question = BeforeYouRead.objects.get(unit=unit, number=4)
                    studentans = U10BeforeYouReadAns.objects.filter(q4answer=question.option1)
                    question.numof1 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q4answer=question.option2)
                    question.numof2 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q4answer=question.option3)
                    question.numof3 = studentans.count()
                    studentans = U10BeforeYouReadAns.objects.filter(q3answer=question.option4)
                    question.numof4 = studentans.count()
                    question.save()
        questionset = BeforeYouRead.objects.filter(unit=unit).order_by('number')

    except:
        print("error")
    return render(request, "beforeyoureadresult.html", locals())

# vocabulary preview ??????????????????
def vocabularypreviewresultNET(request):

    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        print("Unit", unit, "Reading", reading)
        correctansset = VocabularyPreview.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        if unit == '10' and reading == '1':
            studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading).order_by('cId')
            numofansstudent = studentans.count()
            for i in range(1, 9):
                correctans = VocabularyPreview.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 3:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 4:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 5:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 6:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 7:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 8:
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                correctans.save()
        elif unit == '10' and reading == '2':
            studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading).order_by('cId')
            numofansstudent = studentans.count()
            for i in range(1, 9):
                correctans = VocabularyPreview.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 3:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 4:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 5:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 6:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 7:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 8:
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyPreviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                correctans.save()
    except:
        print("error ! ")
        errormessage = "Error !"
    return render(request, "vocabularypreviewresult.html", locals())

# focus on content ??????????????????
def focusoncontentresultNET(request):

    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        print("Unit", unit, "Reading", reading)
        correctansset = FocusOnContent.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        if unit == '10' and reading == '1':
            studentansset = U10R1FocusonContentAns.objects.all().order_by('cId')
            numofansstudent = studentansset.count()
            for i in range(1, 8):
                correctans = FocusOnContent.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 3:
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 4:
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 5:
                    studentans = U10R1FocusonContentAns.objects.filter(q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 6:
                    studentans = U10R1FocusonContentAns.objects.filter(q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 7:
                    studentans = U10R1FocusonContentAns.objects.filter(q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1FocusonContentAns.objects.filter(q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                correctans.save()
        if unit == '10' and reading == '2':
            studentansset = U10R2FocusonContentAns.objects.all().order_by('cId')
            numofansstudent = studentansset.count()
            for i in range(1, 11):
                correctans = FocusOnContent.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 3:
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 4:
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 5:
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.option4)
                    correctans.numof4 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.option5)
                    correctans.numof5 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 6:
                    studentans = U10R2FocusonContentAns.objects.filter(q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 7:
                    studentans = U10R2FocusonContentAns.objects.filter(q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 8:
                    studentans = U10R2FocusonContentAns.objects.filter(q8answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q8answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q8answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 9:
                    studentans = U10R2FocusonContentAns.objects.filter(q9answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q9answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q9answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                elif i == 10:
                    studentans = U10R2FocusonContentAns.objects.filter(q10answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q10answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2FocusonContentAns.objects.filter(q10answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent - studentans.count()) / numofansstudent),
                                                     2)) * 100
                correctans.save()
    except:
        print("error !")
    return render(request, "focusoncontentresult.html", locals())

# vocabulary review ??????????????????
def vocabularyreviewresultNET(request):

    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        print("Unit", unit, "Reading", reading)
        correctansset = VocabularyReview.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        if unit == '10' and reading == '1':
            studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading).order_by('cId')
            numofansstudent = studentans.count()
            for i in range(1, 9):
                correctans = VocabularyReview.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 3:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 4:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 5:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 6:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 7:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 8:
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R1VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                correctans.save()
        elif unit == '10' and reading == '2':
            studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading).order_by('cId')
            numofansstudent = studentans.count()
            for i in range(1, 9):
                correctans = VocabularyReview.objects.get(unit=unit, reading=reading, questionnum=i)
                if i == 1:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q1answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 2:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q2answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 3:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q3answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 4:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q4answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 5:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q5answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 6:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q6answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 7:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q7answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                elif i == 8:
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option1)
                    correctans.numof1 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option2)
                    correctans.numof2 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.option3)
                    correctans.numof3 = studentans.count()
                    studentans = U10R2VocabularyReviewAns.objects.filter(unit=unit, reading=reading, q8answer=correctans.correctans)
                    correctans.falsepercent = (round(((numofansstudent-studentans.count())/numofansstudent), 2))*100
                correctans.save()
    except:
        print("error ! ")
        errormessage = "Error !"
    return render(request, "vocabularyreviewresult.html", locals())

# ????????????vocabulary preview?????????
def vocabularypreviewdetail(request):

    def countavg(group, reading):
        total = 0
        count = 0
        if reading == 1:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('vp1point')
            for student in groupcount:
                if student.vp1point is not None:
                    total += student.vp1point
                    count += 1
        elif reading == 2:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('vp2point')
            for student in groupcount:
                if student.vp2point is not None:
                    total += student.vp2point
                    count += 1
        if count == 0:
            count = 1
        avg = round(total / count, 2)
        return avg

    def savepoint(group, reading):
        studentgroup = studentcheck.objects.filter(cGroup=group).order_by('cId')
        if reading == 1:
            for student in studentgroup:
                t = U10R1VocabularyPreviewAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.vp1point = t.first().point
                    student.save()
        elif reading == 2:
            for student in studentgroup:
                t = U10R2VocabularyPreviewAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.vp2point = t.first().point
                    student.save()
        return studentgroup

    unit = request.GET.get('unit')
    reading = request.GET.get('reading')

    if unit == '10' and reading == '1':
        group1 = savepoint(1, 1)
        group2 = savepoint(2, 1)
        group3 = savepoint(3, 1)
        group4 = savepoint(4, 1)
        group5 = savepoint(5, 1)
        group1avg = countavg(1, 1)
        group2avg = countavg(2, 1)
        group3avg = countavg(3, 1)
        group4avg = countavg(4, 1)
        group5avg = countavg(5, 1)
        return render(request, "vocabularypreviewdetail.html", locals())

    elif unit == '10' and reading == '2':
        group1 = savepoint(1, 2)
        group2 = savepoint(2, 2)
        group3 = savepoint(3, 2)
        group4 = savepoint(4, 2)
        group5 = savepoint(5, 2)
        group1avg = countavg(1, 2)
        group2avg = countavg(2, 2)
        group3avg = countavg(3, 2)
        group4avg = countavg(4, 2)
        group5avg = countavg(5, 2)
        return render(request, "vocabularypreviewdetail2.html", locals())

# ????????????focus on content?????????
def focusoncontentdetail(request):

    def countavg(group, reading):
        total = 0
        count = 0
        if reading == 1:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('foc1point')
            for student in groupcount:
                if student.foc1point is not None:
                    total += student.foc1point
                    count += 1
        elif reading == 2:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('foc2point')
            for student in groupcount:
                if student.foc2point is not None:
                    total += student.foc2point
                    count += 1

        if count == 0:
            count = 1
        avg = total / count
        return avg

    def savepoint(group, reading):
        studentgroup = studentcheck.objects.filter(cGroup=group).order_by('cId')
        if reading == 1:
            for student in studentgroup:
                t = U10R1FocusonContentAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.foc1point = t.first().point
                    student.save()
        elif reading == 2:
            for student in studentgroup:
                t = U10R2FocusonContentAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.foc2point = t.first().point
                    student.save()
        return studentgroup

    unit = request.GET.get('unit')
    reading = request.GET.get('reading')

    if unit == '10' and reading == '1':
        group1 = savepoint(1, 1)
        group2 = savepoint(2, 1)
        group3 = savepoint(3, 1)
        group4 = savepoint(4, 1)
        group5 = savepoint(5, 1)
        group1avg = countavg(1, 1)
        group2avg = countavg(2, 1)
        group3avg = countavg(3, 1)
        group4avg = countavg(4, 1)
        group5avg = countavg(5, 1)
        return render(request, "focusoncontentdetail.html", locals())

    elif unit == '10' and reading == '2':
        group1 = savepoint(1, 2)
        group2 = savepoint(2, 2)
        group3 = savepoint(3, 2)
        group4 = savepoint(4, 2)
        group5 = savepoint(5, 2)
        group1avg = countavg(1, 2)
        group2avg = countavg(2, 2)
        group3avg = countavg(3, 2)
        group4avg = countavg(4, 2)
        group5avg = countavg(5, 2)
        return render(request, "focusoncontentdetail2.html", locals())

# ????????????vocabulary review?????????
def vocabularyreviewdetail(request):


    def countavg(group, reading):
        total = 0
        count = 0
        if reading == 1:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('vr1point')
            for student in groupcount:
                if student.vr1point is not None:
                    total += student.vr1point
                    count += 1
        elif reading == 2:
            groupcount = studentcheck.objects.filter(cGroup=group).order_by('vr2point')
            for student in groupcount:
                if student.vr2point is not None:
                    total += student.vr2point
                    count += 1

        if count == 0:
            count = 1
        avg = total / count
        return avg

    def savepoint(group, reading):
        studentgroup = studentcheck.objects.filter(cGroup=group).order_by('cId')
        if reading == 1:
            for student in studentgroup:
                t = U10R1VocabularyReviewAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.vr1point = t.first().point
                    student.save()
        elif reading == 2:
            for student in studentgroup:
                t = U10R2VocabularyReviewAns.objects.filter(cId=student.cId)
                if (t.count() > 0):
                    student.vr2point = t.first().point
                    student.save()
        return studentgroup

    unit = request.GET.get('unit')
    reading = request.GET.get('reading')

    if unit == '10' and reading == '1':
        group1 = savepoint(1, 1)
        group2 = savepoint(2, 1)
        group3 = savepoint(3, 1)
        group4 = savepoint(4, 1)
        group5 = savepoint(5, 1)
        group1avg = countavg(1, 1)
        group2avg = countavg(2, 1)
        group3avg = countavg(3, 1)
        group4avg = countavg(4, 1)
        group5avg = countavg(5, 1)
        return render(request, "vocabularyreviewdetail.html", locals())

    elif unit == '10' and reading == '2':
        group1 = savepoint(1, 2)
        group2 = savepoint(2, 2)
        group3 = savepoint(3, 2)
        group4 = savepoint(4, 2)
        group5 = savepoint(5, 2)
        group1avg = countavg(1, 2)
        group2avg = countavg(2, 2)
        group3avg = countavg(3, 2)
        group4avg = countavg(4, 2)
        group5avg = countavg(5, 2)
        return render(request, "vocabularyreviewdetail2.html", locals())

# ???before you read?????????????????????????????????????????????Nao??????
def announcebeforeyoureadNET(request):

    QNumber = []
    QQuestion = []
    Qoption1 = []
    Qoption2 = []
    Qoption3 = []
    Qoption4 = []
    Qoption5 = []
    Qnumof1 = []
    Qnumof2 = []
    Qnumof3 = []
    Qnumof4 = []
    Qnumof5 = []
    try:
        unit = request.GET.get('unit')
        beforeyoureadset = BeforeYouRead.objects.filter(unit=unit).order_by('number')
        for beforeyouread in beforeyoureadset:
            QNumber.append(beforeyouread.number)
            QQuestion.append(beforeyouread.question)
            Qoption1.append(beforeyouread.option1)
            Qoption2.append(beforeyouread.option2)
            Qoption3.append(beforeyouread.option3)
            Qoption4.append(beforeyouread.option4)
            Qoption5.append(beforeyouread.option5)
            Qnumof1.append(beforeyouread.numof1)
            Qnumof2.append(beforeyouread.numof2)
            Qnumof3.append(beforeyouread.numof3)
            Qnumof4.append(beforeyouread.numof4)
            Qnumof5.append(beforeyouread.numof5)
    except:
        print("error !")
    return JsonResponse({'QNumber': QNumber, 'QQuestion': QQuestion, 'Qoption1': Qoption1, 'Qoption2': Qoption2,
                        'Qoption3': Qoption3, 'Qoption4': Qoption4, 'Qoption5': Qoption5, 'Qnumof1': Qnumof1,
                        'Qnumof2': Qnumof2, 'Qnumof3': Qnumof3, 'Qnumof4': Qnumof4, 'Qnumof5': Qnumof5})

# ???vocabulary preview?????????????????????????????????????????????Nao??????
def announcevocabularypreviewNET(request):

    QNumber = []
    QQuestion = []
    Qoption1 = []
    Qoption2 = []
    Qoption3 = []
    Qnumof1 = []
    Qnumof2 = []
    Qnumof3 = []
    Qcorrectans = []
    Qfalsepercent = []
    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        vocabularypreviewset = VocabularyPreview.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        for vocabularypreview in vocabularypreviewset:
            QNumber.append(vocabularypreview.questionnum)
            QQuestion.append(vocabularypreview.question)
            Qoption1.append(vocabularypreview.option1)
            Qoption2.append(vocabularypreview.option2)
            Qoption3.append(vocabularypreview.option3)
            Qnumof1.append(vocabularypreview.numof1)
            Qnumof2.append(vocabularypreview.numof2)
            Qnumof3.append(vocabularypreview.numof3)
            Qcorrectans.append(vocabularypreview.correctans)
            Qfalsepercent.append(vocabularypreview.falsepercent)
    except:
        print("error !")
    return JsonResponse({'QNumber': QNumber, 'QQuestion': QQuestion, 'Qoption1': Qoption1, 'Qoption2': Qoption2,
                        'Qoption3': Qoption3, 'Qnumof1': Qnumof1, 'Qnumof2': Qnumof2, 'Qnumof3': Qnumof3, 'Qcorrectans': Qcorrectans,
                         'Qfalsepercent': Qfalsepercent})

# ???focus on content?????????????????????????????????????????????Nao??????
def announcefocusoncontentNET(request):

    QNumber = []
    QQuestion = []
    Qoption1 = []
    Qoption2 = []
    Qoption3 = []
    Qoption4 = []
    Qoption5 = []
    Qnumof1 = []
    Qnumof2 = []
    Qnumof3 = []
    Qnumof4 = []
    Qnumof5 = []
    Qcorrectans = []
    Qfalsepercent = []
    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        focusoncontentset = FocusOnContent.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        for focusoncontent in focusoncontentset:
            QNumber.append(focusoncontent.questionnum)
            QQuestion.append(focusoncontent.question)
            Qoption1.append(focusoncontent.option1)
            Qoption2.append(focusoncontent.option2)
            Qoption3.append(focusoncontent.option3)
            Qoption4.append(focusoncontent.option4)
            Qoption5.append(focusoncontent.option5)
            Qnumof1.append(focusoncontent.numof1)
            Qnumof2.append(focusoncontent.numof2)
            Qnumof3.append(focusoncontent.numof3)
            Qnumof4.append(focusoncontent.numof4)
            Qnumof5.append(focusoncontent.numof5)
            Qcorrectans.append(focusoncontent.correctans)
            Qfalsepercent.append(focusoncontent.falsepercent)
    except:
        print("errorr !")
    return JsonResponse({'QNumber': QNumber, 'QQuestion': QQuestion, 'Qoption1': Qoption1, 'Qoption2': Qoption2,
                        'Qoption3': Qoption3, 'Qoption4': Qoption4, 'Qoption5': Qoption5, 'Qnumof1': Qnumof1,
                         'Qnumof2': Qnumof2, 'Qnumof3': Qnumof3, 'Qnumof4': Qnumof4, 'Qnumof5': Qnumof5,
                         'Qcorrectans': Qcorrectans, 'Qfalsepercent': Qfalsepercent})

# ???vocabulary review?????????????????????????????????????????????Nao??????
def announcevocabularyreviewNET(request):

    QNumber = []
    QQuestion = []
    Qoption1 = []
    Qoption2 = []
    Qoption3 = []
    Qnumof1 = []
    Qnumof2 = []
    Qnumof3 = []
    Qcorrectans = []
    Qfalsepercent = []
    try:
        unit = request.GET.get('unit')
        reading = request.GET.get('reading')
        vocabularyreviewset = VocabularyReview.objects.filter(unit=unit, reading=reading).order_by('questionnum')
        for vocabularyreview in vocabularyreviewset:
            QNumber.append(vocabularyreview.questionnum)
            QQuestion.append(vocabularyreview.question)
            Qoption1.append(vocabularyreview.option1)
            Qoption2.append(vocabularyreview.option2)
            Qoption3.append(vocabularyreview.option3)
            Qnumof1.append(vocabularyreview.numof1)
            Qnumof2.append(vocabularyreview.numof2)
            Qnumof3.append(vocabularyreview.numof3)
            Qcorrectans.append(vocabularyreview.correctans)
            Qfalsepercent.append(vocabularyreview.falsepercent)
    except:
        print("error !")
    return JsonResponse({'QNumber': QNumber, 'QQuestion': QQuestion, 'Qoption1': Qoption1, 'Qoption2': Qoption2,
                        'Qoption3': Qoption3, 'Qnumof1': Qnumof1, 'Qnumof2': Qnumof2, 'Qnumof3': Qnumof3, 'Qcorrectans': Qcorrectans,
                         'Qfalsepercent': Qfalsepercent})

# ????????????????????????
def announceuncheckedstudentNET(request):

    week = request.GET.get('week')
    uncheckedstudentname = []
    if week == '1':
        uncheckedstudent = studentcheck.objects.filter(FirstweekCheck="????????????")
    elif week == '2':
        uncheckedstudent = studentcheck.objects.filter(SecondweekCheck="????????????")
    elif week == '3':
        uncheckedstudent = studentcheck.objects.filter(ThirdweekCheck="????????????")
    else:
        uncheckedstudent = studentcheck.objects.filter(ForthweekCheck="????????????")

    print(uncheckedstudent.count())
    for i in uncheckedstudent:
        uncheckedstudentname.append(i.cName)

    print(uncheckedstudentname)

    return JsonResponse({'result': uncheckedstudentname})

# ????????????????????????
def changesectiontostudentcheck(request):

    global section
    zenbo = request.GET.get('zenbo')
    if zenbo == '1':
        section[0] = 'studentcheck'
        print("Zenbo 1 Change section to " + section[0])
        print(section)
    elif zenbo == '2':
        section[1] = 'studentcheck'
        print("Zenbo 2 Change section to " + section[1])
        print(section)
    elif zenbo == '3':
        section[2] = 'studentcheck'
        print("Zenbo 3 Change section to " + section[2])
        print(section)
    elif zenbo == '4':
        section[3] = 'studentcheck'
        print("Zenbo 4 Change section to " + section[3])
        print(section)
    elif zenbo == '5':
        section[4] = 'studentcheck'
        print("Zenbo 5 Change section to " + section[4])
        print(section)
    elif zenbo == 'all':
        section = ['studentcheck', 'studentcheck', 'studentcheck', 'studentcheck', 'studentcheck']
        print("All zenbo Change section to " + section[4])
        print(section)

    return JsonResponse({'my_string': "???????????????????????????"})

# ??????????????????before you read
def changesectiontobeforeyouread(request):

    global section
    zenbo = request.GET.get('zenbo')
    if zenbo == '1':
        section[0] = 'beforeyouread'
        print("Zenbo 1 Change section to " + section[0])
        print(section)
    elif zenbo == '2':
        section[1] = 'beforeyouread'
        print("Zenbo 2 Change section to " + section[1])
        print(section)
    elif zenbo == '3':
        section[2] = 'beforeyouread'
        print("Zenbo 3 Change section to " + section[2])
        print(section)
    elif zenbo == '4':
        section[3] = 'beforeyouread'
        print("Zenbo 4 Change section to " + section[3])
        print(section)
    elif zenbo == '5':
        section[4] = 'beforeyouread'
        print("Zenbo 5 Change section to " + section[4])
        print(section)
    elif zenbo == 'all':
        section = ['beforeyouread', 'beforeyouread', 'beforeyouread',
                   'beforeyouread', 'beforeyouread']
        print("All zenbo Change section to " + section[4])
        print(section)

    return JsonResponse({'my_string': "?????????Before you read??????"})

# ??????????????????vocabulary preview
def changesectiontovocabularypreview(request):

    global section
    unit = request.GET.get('unit')
    reading = request.GET.get('reading')
    zenbo = request.GET.get('zenbo')
    if unit == '10' and reading == '1':
        if zenbo == '1':
            section[0] = 'U10R1vocabularypreview'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R1vocabularypreview'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R1vocabularypreview'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R1vocabularypreview'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R1vocabularypreview'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R1vocabularypreview', 'U10R1vocabularypreview', 'U10R1vocabularypreview', 'U10R1vocabularypreview', 'U10R1vocabularypreview']
            print("All zenbo Change section to " + section[4])
            print(section)
    elif unit == '10' and reading == '2':
        if zenbo == '1':
            section[0] = 'U10R2vocabularypreview'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R2vocabularypreview'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R2vocabularypreview'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R2vocabularypreview'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R2vocabularypreview'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R2vocabularypreview', 'U10R2vocabularypreview', 'U10R2vocabularypreview',
                       'U10R2vocabularypreview', 'U10R2vocabularypreview']
            print("All zenbo Change section to " + section[4])
            print(section)

    return JsonResponse({'my_string': "?????????vocabulary preview??????"})

# ??????????????????focus on content
def changesectiontofocusoncontent(request):

    global section
    unit = request.GET.get('unit')
    reading = request.GET.get('reading')
    zenbo = request.GET.get('zenbo')
    if unit == '10' and reading == '1':
        if zenbo == '1':
            section[0] = 'U10R1focusoncontent'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R1focusoncontent'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R1focusoncontent'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R1focusoncontent'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R1focusoncontent'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R1focusoncontent', 'U10R1focusoncontent', 'U10R1focusoncontent', 'U10R1focusoncontent', 'U10R1focusoncontent']
            print("All zenbo Change section to " + section[4])
            print(section)
    elif unit == '10' and reading == '2':
        if zenbo == '1':
            section[0] = 'U10R2focusoncontent'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R2focusoncontent'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R2focusoncontent'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R2focusoncontent'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R2focusoncontent'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R2focusoncontent', 'U10R2focusoncontent', 'U10R2focusoncontent', 'U10R2focusoncontent', 'U10R2focusoncontent']
            print("All zenbo Change section to " + section[4])
            print(section)

    return JsonResponse({'my_string': "?????????focus on content??????"})

# ??????????????????vocabulary review
def changesectiontovocabularyreview(request):

    global section
    unit = request.GET.get('unit')
    reading = request.GET.get('reading')
    zenbo = request.GET.get('zenbo')
    if unit == '10' and reading == '1':
        if zenbo == '1':
            section[0] = 'U10R1vocabularyreview'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R1vocabularyreview'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R1vocabularyreview'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R1vocabularyreview'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R1vocabularyreview'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R1vocabularyreview', 'U10R1vocabularyreview', 'U10R1vocabularyreview', 'U10R1vocabularyreview', 'U10R1vocabularyreview']
            print("All zenbo Change section to " + section[4])
            print(section)
    elif unit == '10' and reading == '2':
        if zenbo == '1':
            section[0] = 'U10R2vocabularyreview'
            print("Zenbo 1 Change section to " + section[0])
            print(section)
        elif zenbo == '2':
            section[1] = 'U10R2vocabularyreview'
            print("Zenbo 2 Change section to " + section[1])
            print(section)
        elif zenbo == '3':
            section[2] = 'U10R2vocabularyreview'
            print("Zenbo 3 Change section to " + section[2])
            print(section)
        elif zenbo == '4':
            section[3] = 'U10R2vocabularyreview'
            print("Zenbo 4 Change section to " + section[3])
            print(section)
        elif zenbo == '5':
            section[4] = 'U10R2vocabularyreview'
            print("Zenbo 5 Change section to " + section[4])
            print(section)
        elif zenbo == 'all':
            section = ['U10R2vocabularyreview', 'U10R2vocabularyreview', 'U10R2vocabularyreview', 'U10R2vocabularyreview', 'U10R2vocabularyreview']
            print("All zenbo Change section to " + section[4])
            print(section)

    return JsonResponse({'my_string': "?????????vocabulary review??????"})

# ??????????????????Critical thinking
def changesectiontocriticalthinking(request):

    global section
    zenbo = request.GET.get('zenbo')
    if zenbo == '1':
        section[0] = 'criticalthinking'
        print("Zenbo 1 Change section to " + section[0])
        print(section)
    elif zenbo == '2':
        section[1] = 'criticalthinking'
        print("Zenbo 2 Change section to " + section[1])
        print(section)
    elif zenbo == '3':
        section[2] = 'criticalthinking'
        print("Zenbo 3 Change section to " + section[2])
        print(section)
    elif zenbo == '4':
        section[3] = 'criticalthinking'
        print("Zenbo 4 Change section to " + section[3])
        print(section)
    elif zenbo == '5':
        section[4] = 'criticalthinking'
        print("Zenbo 5 Change section to " + section[4])
        print(section)
    elif zenbo == 'all':
        section = ['criticalthinking', 'criticalthinking', 'criticalthinking',
                   'criticalthinking', 'criticalthinking']
        print("All zenbo Change section to " + section[4])
        print(section)

    return JsonResponse({'my_string': "?????????Critical Thinking??????"})

# ????????????????????????????????????
def groupcheckok(request):

    global section
    group = request.GET.get('group')
    week = request.GET.get('week')
    if group == '1':
        section[0] = "section"
    elif group == '2':
        section[1] = "section"
    elif group == '3':
        section[2] = "section"
    elif group == '4':
        section[3] = "section"
    elif group == '5':
        section[4] = "section"
    else:
        section = ["section", "section", "section", "section", "section"]

    return JsonResponse({"": "Done"})

# ???????????????????????????Zenbo Junior
def checksection(request):

    global section
    zenbo = request.GET.get('zenbo')
    if zenbo == '1':
        return JsonResponse({"section": section[0]})
    elif zenbo == '2':
        return JsonResponse({"section": section[1]})
    elif zenbo == '3':
        return JsonResponse({"section": section[2]})
    elif zenbo == '4':
        return JsonResponse({"section": section[3]})
    elif zenbo == '5':
        return JsonResponse({"section": section[4]})
    else:
        return JsonResponse({"": "Error"})

# ?????????????????????vocabulary preview??????
def getvocabularypreviewscoreNET(request):

    try:
        cId = request.GET.get('cId')
        reading = request.GET.get('reading')
        student = studentcheck.objects.get(cId=cId)
        if reading == '1':
            point = str(student.vp1point)+"pts"
            return JsonResponse({"": point})
        elif reading == '2':
            point = str(student.vp2point) + "pts"
            return JsonResponse({"": point})
    except:
        point = "Error"
        return JsonResponse({"": point})
        print("Error")

# ?????????????????????vocabulary review??????
def getvocabularyreviewscoreNET(request):

    try:
        cId = request.GET.get('cId')
        reading = request.GET.get('reading')
        student = studentcheck.objects.get(cId=cId)
        if reading == '1':
            point = str(student.vr1point) + "pts"
            return JsonResponse({"": point})
        elif reading == '2':
            point = str(student.vr2point) + "pts"
            return JsonResponse({"": point})
    except:
        point = "Error"
        return JsonResponse({"": point})
        print("Error")

# ?????????????????????focus on content??????
def getfocusoncontentscoreNET(request):

    try:
        cId = request.GET.get('cId')
        reading = request.GET.get('reading')
        student = studentcheck.objects.get(cId=cId)
        if reading == '1':
            point = str(student.foc1point) + "pts"
            return JsonResponse({"": point})
        elif reading == '2':
            point = str(student.foc2point) + "pts"
            return JsonResponse({"": point})
    except:
        point = "Error"
        return JsonResponse({"": point})
        print("Error")

# ?????????????????????????????????
def getvocabularydetailNET(request):

    global vocabularylist
    vocabularylist.clear()
    i = 0
    unit = request.GET.get('unit')
    reading = request.GET.get('reading')
    vocabularyarray = VocabularyDetail.objects.filter(unit=unit, reading=reading)
    for vocabulary in vocabularyarray:
        vocabularylist.append(str(vocabulary))
        print(str(vocabulary))
    return JsonResponse({'v1': vocabularylist[0], 'v2': vocabularylist[1], 'v3': vocabularylist[2]
                         , 'v4': vocabularylist[3], 'v5': vocabularylist[4], 'v6': vocabularylist[5]
                         , 'v7': vocabularylist[6], 'v8': vocabularylist[7]})

# ??????????????????vocabulary preview???????????????
def getvocabularypreviewanswerNET(request):

    reading = request.GET.get('reading')
    cId = request.GET.get('cId')
    if reading == '1':
        studentdetail = U10R1VocabularyPreviewAns.objects.filter(cId=cId).first()
    else:
        studentdetail = U10R2VocabularyPreviewAns.objects.filter(cId=cId).first()
    correctans = VocabularyPreview.objects.filter(reading=reading)
    questionset = VocabularyPreview.objects.filter(reading=reading).order_by('questionnum')
    return JsonResponse({'cId': studentdetail.cId, 'Q1': questionset[0].question, 'Q2': questionset[1].question
                         , 'Q3': questionset[2].question, 'Q4': questionset[3].question, 'Q5': questionset[4].question
                         , 'Q6': questionset[5].question, 'Q7': questionset[6].question, 'Q8': questionset[7].question
                         , 'q1answer': studentdetail.q1answer, 'q2answer': studentdetail.q2answer
                         , 'q3answer': studentdetail.q3answer, 'q4answer': studentdetail.q4answer, 'q5answer': studentdetail.q5answer
                         , 'q6answer': studentdetail.q6answer, 'q7answer': studentdetail.q7answer, 'q8answer': studentdetail.q8answer
                         , 'q1coranswer': correctans[0].correctans, 'q2coranswer': correctans[1].correctans, 'q3coranswer': correctans[2].correctans
                         , 'q4coranswer': correctans[3].correctans, 'q5coranswer': correctans[4].correctans, 'q6coranswer': correctans[5].correctans
                         , 'q7coranswer': correctans[6].correctans, 'q8coranswer': correctans[7].correctans, 'point': studentdetail.point})

# ??????????????????vocabulary review???????????????
def getvocabularyreviewanswerNET(request):

    reading = request.GET.get('reading')
    cId = request.GET.get('cId')
    if reading == '1':
        studentdetail = U10R1VocabularyReviewAns.objects.filter(cId=cId).first()
    else:
        studentdetail = U10R2VocabularyReviewAns.objects.filter(cId=cId).first()
    correctans = VocabularyReview.objects.filter(reading=reading)
    questionset = VocabularyReview.objects.filter(reading=reading).order_by('questionnum')
    return JsonResponse({'cId': studentdetail.cId, 'Q1': questionset[0].question, 'Q2': questionset[1].question
                         , 'Q3': questionset[2].question, 'Q4': questionset[3].question, 'Q5': questionset[4].question
                         , 'Q6': questionset[5].question, 'Q7': questionset[6].question, 'Q8': questionset[7].question
                         , 'q1answer': studentdetail.q1answer, 'q2answer': studentdetail.q2answer, 'q3answer': studentdetail.q3answer
                         , 'q4answer': studentdetail.q4answer, 'q5answer': studentdetail.q5answer, 'q6answer': studentdetail.q6answer
                         , 'q7answer': studentdetail.q7answer, 'q8answer': studentdetail.q8answer
                         , 'q1coranswer': correctans[0].correctans, 'q2coranswer': correctans[1].correctans, 'q3coranswer': correctans[2].correctans
                         , 'q4coranswer': correctans[3].correctans, 'q5coranswer': correctans[4].correctans, 'q6coranswer': correctans[5].correctans
                         , 'q7coranswer': correctans[6].correctans, 'q8coranswer': correctans[7].correctans, 'point': studentdetail.point})

# ???????????????critical thinking?????????
def criticalthinkingrecord(request):

    cId = request.GET.get('cId')
    choose = request.GET.get('choose')
    beforeorafter = request.GET.get('time')
    student = studentcheck.objects.get(cId=cId)
    if choose == 'affirmative':
        if beforeorafter == 'before':
            student.ctchoosebeforediscuss = 1
        elif beforeorafter == 'after':
            student.ctchooseafterdiscuss = 1
    elif choose == 'negative':
        if beforeorafter == 'before':
            student.ctchoosebeforediscuss = -1
        elif beforeorafter == 'after':
            student.ctchooseafterdiscuss = -1
    student.save()

    return JsonResponse({'result': "Good Job"})

# Zenbo Junior ???????????????????????????????????????
def getgroupstudents(request):

    group = request.GET.get('group')
    students = studentcheck.objects.all()
    if group == "1":
        students = studentcheck.objects.filter(cGroup=group).order_by('id')
    elif group == "2":
        students = studentcheck.objects.filter(cGroup=group).order_by('id')
    elif group == "3":
        students = studentcheck.objects.filter(cGroup=group).order_by('id')
    elif group == "4":
        students = studentcheck.objects.filter(cGroup=group).order_by('id')
    elif group == "5":
        students = studentcheck.objects.filter(cGroup=group).order_by('id')
    else:
        students = studentcheck.objects.filter(cGroup=group).order_by('id')

    if students.count() == 4:
        return JsonResponse(
            {'student1': students[0].cId, 'student2': students[1].cId, 'student3': students[2].cId,
             'student4': students[3].cId})
    elif students.count() == 5:
        return JsonResponse(
            {'student1': students[0].cId, 'student2': students[1].cId, 'student3': students[2].cId,
             'student4': students[3].cId, 'student5': students[4].cId, 'student6': "student"})
    else:
        return JsonResponse(
            {'student1': students[0].cId, 'student2': students[1].cId, 'student3': students[2].cId,
             'student4': students[3].cId, 'student5': students[4].cId, 'student6': students[5].cId})


# ???????????????

nowautoclassname = 0
nowclassid = 0
groupsready = []
customizesection = []
customizediscussion = []
stepnow = 0
readingpart = 0

# ??????????????????unready (Normal Function)
def init_groupsready():
    global groupsready
    for i in range(len(groupsready)):
        groupsready[i] = "unready"
    print(str(groupsready))

# ?????????????????? (Normal Function)
def changesection(group, section):
    global stepnow
    global customizesection
    if group != "startall":
        stepnow += 1
        for i in range(len(customizesection)):
            customizesection[i] = section
    else:
        for i in range(len(customizesection)):
            customizesection[i] = section
    print(str(customizesection))
    print(stepnow)

# ??????????????????????????????????????????
def customizestudentslist(request):
    changesection("all", "studentcheck")
    classid = request.GET.get('classid')
    if classid != None:
        StudentsList = CustomizeStudentList.objects.filter(classid=classid)
        serializersstudentlist = serializers.serialize("json", StudentsList)
    classids = []
    classidname = ""
    randomset = CustomizeStudentList.objects.filter(~Q(classid=classidname)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(classid=classidname)).order_by('id')
        randomone = randomset.first()
        classidname = randomone.classid
        classids.append(classidname)
        if randomset.filter(~Q(classid=classidname)).count() == 0:
            break
    classname = request.GET.get('classname')
    if classname != None:
        stepnow = request.GET.get('step')
        autoclass = CustomizeClassInfo.objects.get(classname=classname)
        stepbystep = autoclass.stepbystep.split('/')
        stepbystepdetail = autoclass.stepbystepdetail.split('/')
        attention = autoclass.attention
        if int(stepnow) != len(stepbystep):
            nextstep = stepbystep[int(stepnow) - 1 + 1]
            nextstepdetail = stepbystepdetail[int(stepnow) - 1 + 1]
        print("stepnow : " + stepnow)
    return render(request, "CustomizeStudents.html", locals())

# ????????????????????????????????????
def teachcustomizevocabulary(request):
    changesection("all", "vocabularyteach")
    package = request.GET.get('package')
    if package != None:
        Vocabularies = CustomizeVocabulary.objects.filter(package=package)
        serializersvocabularies = serializers.serialize("json", Vocabularies)
    categories = []
    packagename = ""
    randomset = CustomizeVocabulary.objects.filter(~Q(package=packagename)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(package=packagename)).order_by('id')
        randomone = randomset.first()
        packagename = randomone.package
        categories.append(packagename)
        if randomset.filter(~Q(package=packagename)).count() == 0:
            break
    classname = request.GET.get('classname')
    if classname != None:
        stepnow = request.GET.get('step')
        autoclass = CustomizeClassInfo.objects.get(classname=classname)
        stepbystep = autoclass.stepbystep.split('/')
        stepbystepdetail = autoclass.stepbystepdetail.split('/')
        attention = autoclass.attention
        if int(stepnow) != len(stepbystep):
            nextstep = stepbystep[int(stepnow) - 1 + 1]
            nextstepdetail = stepbystepdetail[int(stepnow) - 1 + 1]
            print("stepnow : " + stepnow)
    return render(request, "CustomizeVocabularyTeach.html", locals())

# ?????????????????????????????????????????????
def customizequiz(request):
    changesection("all", "quiz")
    package = request.GET.get('package')
    if package != None:
        Questionset = CustomizeQuiz.objects.filter(package=package)
        serializersquestions = serializers.serialize("json", Questionset)
    categories = []
    packagename = ""
    randomset = CustomizeQuiz.objects.filter(~Q(package=packagename)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(package=packagename)).order_by('id')
        randomone = randomset.first()
        packagename = randomone.package
        categories.append(packagename)
        if randomset.filter(~Q(package=packagename)).count() == 0:
            break
    classname = request.GET.get('classname')
    if classname != None:
        stepnow = request.GET.get('step')
        autoclass = CustomizeClassInfo.objects.get(classname=classname)
        stepbystep = autoclass.stepbystep.split('/')
        stepbystepdetail = autoclass.stepbystepdetail.split('/')
        attention = autoclass.attention
        i = 0
        for step in stepbystep:
            if step == "studentcheck":
                classid = stepbystepdetail[i]
            else:
                i += 1
        if int(stepnow) != len(stepbystep):
            nextstep = stepbystep[int(stepnow) - 1 + 1]
            nextstepdetail = stepbystepdetail[int(stepnow) - 1 + 1]
        print("stepnow : " + stepnow)
    return render(request, "CustomizeQuiz.html", locals())

# ?????????????????????????????????
def customizereading(request):
    changesection("all", "reading")
    init_groupsready()
    lesson = request.GET.get('lesson')
    print(lesson)
    if lesson != None:
        Teachlesson = CustomizeReading.objects.filter(lesson=lesson)
        serializersteachlesson = serializers.serialize("json", Teachlesson)
    readinglessons = []
    lessonname = ""
    randomset = CustomizeReading.objects.filter(~Q(lesson=lessonname)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(lesson=lessonname)).order_by('id')
        randomone = randomset.first()
        lessonname = randomone.lesson
        readinglessons.append(lessonname)
        if randomset.filter(~Q(lesson=lessonname)).count() == 0:
            break
    classname = request.GET.get('classname')
    if classname != None:
        stepnow = request.GET.get('step')
        autoclass = CustomizeClassInfo.objects.get(classname=classname)
        stepbystep = autoclass.stepbystep.split('/')
        stepbystepdetail = autoclass.stepbystepdetail.split('/')
        attention = autoclass.attention
        i = 0
        for step in stepbystep:
            if step == "studentcheck":
                classid = stepbystepdetail[i]
            else:
                i += 1
        if int(stepnow) != len(stepbystep):
            nextstep = stepbystep[int(stepnow) - 1 + 1]
            nextstepdetail = stepbystepdetail[int(stepnow) - 1 + 1]
        print("stepnow : " + stepnow)
    return render(request, "customizereading.html", locals())

# reading????????????????????????
def readingpartsettingandgetting(request):
    global stepnow
    global nowautoclassname
    global readingpart
    nowautoclass = CustomizeClassInfo.objects.get(classname=nowautoclassname)
    nowautoclassstepbystepdetail = nowautoclass.stepbystepdetail.split('/')
    print(stepnow)
    nowlesson = nowautoclassstepbystepdetail[stepnow-1]
    print(nowlesson)
    nowreading = CustomizeReading.objects.filter(lesson=nowlesson)
    access = request.GET.get('access')
    if access == "setting":
        readingpart = int(request.GET.get('part'))
        return JsonResponse({"result": "OK"})
    elif access == "getting":
        nowreading = nowreading.get(part=readingpart)
        return JsonResponse({"result": nowreading.readingexplanationaudio})

# ????????????(?????????)
def customizeexercise(request):
    changesection("all", "exercise")
    exercise = request.GET.get('exercisename')
    Exerciseset = CustomizeExerciseInfo.objects.all()
    if exercise != None:
        playingexercise = CustomizeExerciseInfo.objects.get(exercisename=exercise).musicdirectory
    exercises = []
    exercisename = ""
    randomset = CustomizeExerciseInfo.objects.filter(~Q(exercisename=exercisename)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(exercisename=exercisename)).order_by('id')
        randomone = randomset.first()
        exercisename = randomone.exercisename
        exercises.append(exercisename)
        if randomset.filter(~Q(exercisename=exercisename)).count() == 0:
            break
    classname = request.GET.get('classname')
    if classname != None:
        stepnow = request.GET.get('step')
        autoclass = CustomizeClassInfo.objects.get(classname=classname)
        stepbystep = autoclass.stepbystep.split('/')
        stepbystepdetail = autoclass.stepbystepdetail.split('/')
        attention = autoclass.attention
        i = 0
        for step in stepbystep:
            if step == "studentcheck":
                classid = stepbystepdetail[i]
            else:
                i += 1
        if int(stepnow) != len(stepbystep):
            nextstep = stepbystep[int(stepnow) - 1 + 1]
            nextstepdetail = stepbystepdetail[int(stepnow) - 1 + 1]
        print("stepnow : " + stepnow)
    return render(request, "CustomizeExercise.html", locals())

# ????????????
def clock(request):
    classname = request.GET.get('classname')
    if classname != None:
        stepnow = request.GET.get('step')
        autoclass = CustomizeClassInfo.objects.get(classname=classname)
        stepbystep = autoclass.stepbystep.split('/')
        stepbystepdetail = autoclass.stepbystepdetail.split('/')
        attention = autoclass.attention
        if int(stepnow) != len(stepbystep):
            nextstep = stepbystep[int(stepnow) - 1 + 1]
            nextstepdetail = stepbystepdetail[int(stepnow) - 1 + 1]
        print("stepnow : " + stepnow)
    return render(request, "clock.html", locals())

# ????????????
def customizediscussion(request):
    changesection("all", "discussion")
    getissue = request.GET.get('issue')
    discussionissues = getissue.split('\\')
    print(discussionissues)
    timetowait = 0
    for issue in discussionissues:
        if CustomizeDiscussion.objects.get(issuename=issue).time > timetowait:
            timetowait = CustomizeDiscussion.objects.get(issuename=issue).time
    classname = request.GET.get('classname')
    if classname != None:
        stepnow = request.GET.get('step')
        autoclass = CustomizeClassInfo.objects.get(classname=classname)
        stepbystep = autoclass.stepbystep.split('/')
        stepbystepdetail = autoclass.stepbystepdetail.split('/')
        attention = autoclass.attention
        if int(stepnow) != len(stepbystep):
            nextstep = stepbystep[int(stepnow) - 1 + 1]
            nextstepdetail = stepbystepdetail[int(stepnow) - 1 + 1]
    groupsnum = len(groupsready)
    return render(request, "CustomizeDiscussion.html", locals())

# ????????????????????????????????????
def customizestudentchangepoint(request):
    studentid = request.GET.get('student')
    plusorminus = request.GET.get('change')
    student = CustomizeStudentList.objects.get(studentid=studentid)
    if plusorminus == "plus":
        student.studentpoint += 1
    else:
        student.studentpoint -= 1
    student.save()
    return JsonResponse({'responsemessage': "Success"})

# ?????????????????????????????????????????????
def customizestudentchangecheck(request):
    studentid = request.GET.get('student')
    student = CustomizeStudentList.objects.get(studentid=studentid)
    if student.studentcheck == "????????????":
        student.studentcheck = "?????????"
    else:
        student.studentcheck = "????????????"
    student.save()
    return JsonResponse({'responsemessage': 'Success'})

# ???????????????????????????????????????
def customizerandompickstudent(request):
    group = request.GET.get('group')
    classid = request.GET.get('classid')
    if group == "all":
        pickedstudent = CustomizeStudentList.objects.filter(classid=classid).order_by('?').first()
    else:
        pickedstudent = CustomizeStudentList.objects.filter(classid=classid, studentgroup=group).order_by('?').first()
    return JsonResponse({'pickedstudent': pickedstudent.studentname})

# ???????????????????????????
def customizeclassinfopage(request):
    classids = []
    classidname = ""
    randomset = CustomizeStudentList.objects.filter(~Q(classid=classidname)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(classid=classidname)).order_by('id')
        randomone = randomset.first()
        classidname = randomone.classid
        classids.append(classidname)
        if randomset.filter(~Q(classid=classidname)).count()==0:
            break
    categories = []
    packagename = ""
    randomset = CustomizeVocabulary.objects.filter(~Q(package=packagename)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(package=packagename)).order_by('id')
        randomone = randomset.first()
        packagename = randomone.package
        categories.append(packagename)
        if randomset.filter(~Q(package=packagename)).count() == 0:
            break
    quizpackages = []
    packagename = ""
    randomset = CustomizeQuiz.objects.filter(~Q(package=packagename)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(package=packagename)).order_by('id')
        randomone = randomset.first()
        packagename = randomone.package
        quizpackages.append(packagename)
        if randomset.filter(~Q(package=packagename)).count() == 0:
            break
    readinglessons = []
    lessonname = ""
    randomset = CustomizeReading.objects.filter(~Q(lesson=lessonname)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(lesson=lessonname)).order_by('id')
        randomone = randomset.first()
        lessonname = randomone.lesson
        readinglessons.append(lessonname)
        if randomset.filter(~Q(lesson=lessonname)).count() == 0:
            break
    exercises = []
    exercisename = ""
    randomset = CustomizeExerciseInfo.objects.filter(~Q(exercisename=exercisename)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(exercisename=exercisename)).order_by('id')
        randomone = randomset.first()
        exercisename = randomone.exercisename
        exercises.append(exercisename)
        if randomset.filter(~Q(exercisename=exercisename)).count() == 0:
            break
    issues = []
    issuename = ""
    randomset = CustomizeDiscussion.objects.filter(~Q(issuename=issuename)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(issuename=issuename)).order_by('id')
        randomone = randomset.first()
        issuename = randomone.issuename
        issues.append(issuename)
        if randomset.filter(~Q(issuename=issuename)).count() == 0:
            break
    return render(request, "CustomizeClassInfo.html", locals())

# ??????????????????????????????????????????
def customizeclassinfosetting(request):
    classname = request.GET.get('classname')
    stepbystep = request.GET.get('stepbystep')
    stepbystepdetail = request.GET.get('stepbystepdetail')
    stepbysteptoshow = request.GET.get('stepbysteptoshow')
    attention = request.GET.get('attention')
    CustomizeClassInfo.objects.create(classname=classname, stepbystep=stepbystep, stepbystepdetail=stepbystepdetail, stepbysteptoshow=stepbysteptoshow, attention=attention)
    return JsonResponse({'responsemessage': "??????????????????"})

# ????????????????????????????????????????????????????????????
def startcustomizeautoclass(request):
    AutoClassInfo = CustomizeClassInfo.objects.all().order_by('id').reverse()
    serializersautoclasslist = serializers.serialize("json", AutoClassInfo)
    return render(request, "StartAutoClass.html", locals())

# ?????????????????????
def startautoclass(request):
    global stepnow
    stepnow = 0
    global customizesection
    customizesection.clear()
    global customizediscussion
    customizediscussion = []
    global nowautoclassname
    global nowclassid
    global groupsready
    groupsready = []
    nowautoclassname = request.GET.get('classname')
    theclass = CustomizeClassInfo.objects.get(classname=nowautoclassname)
    stepbystep = theclass.stepbystep.split('/')
    stepbystepdetail = theclass.stepbystepdetail.split('/')
    i = 0
    for step in stepbystep:
        if step == "studentcheck":
            nowclassid = stepbystepdetail[i]
        else:
            if step == "discussion":
                everygroupdiscussion = stepbystepdetail[i].split('\\\\')
                for dis in everygroupdiscussion:
                    customizediscussion.append(dis)
            print(customizediscussion)
        i += 1
    group = 0
    randomset = CustomizeStudentList.objects.filter(classid=nowclassid).filter(~Q(studentgroup=group)).order_by('id')
    while 1:
        randomset = randomset.filter(~Q(studentgroup=group)).order_by('id')
        randomone = randomset.first()
        group = randomone.studentgroup
        groupsready.append("unready")
        customizesection.append("section")
        if randomset.filter(~Q(studentgroup=group)).count() == 0:
            break
    print("\n" + nowautoclassname + "/" + nowclassid + "\n")
    changesection("startall", stepbystep[0])
    return JsonResponse({'result': "OK !"})

# Zenbo App ????????????????????????????????????
def zenbogetclassinfo(request):
    access = request.GET.get('access')
    if access == "getclassid":
        classids = []
        classidname = ""
        randomset = CustomizeStudentList.objects.filter(~Q(classid=classidname)).order_by('id')
        while 1:
            randomset = randomset.filter(~Q(classid=classidname)).order_by('id')
            randomone = randomset.first()
            classidname = randomone.classid
            classids.append(classidname)
            if randomset.filter(~Q(classid=classidname)).count() == 0:
                break
        return JsonResponse(classids, safe=False)
    elif access == "getgroups":
        classid = request.GET.get('classid')
        studentlist = CustomizeStudentList.objects.filter(classid=classid)
        groupsnumlist = []
        group = 0
        randomset = studentlist.filter(~Q(studentgroup=group)).order_by('id')
        while 1:
            randomset = randomset.filter(~Q(studentgroup=group)).order_by('id')
            randomone = randomset.first()
            group = randomone.studentgroup
            groupsnumlist.append("Group"+str(group))
            if randomset.filter(~Q(studentgroup=group)).count() == 0:
                break
        return JsonResponse(groupsnumlist, safe=False)
    elif access == "getstudentlist":
        classid = request.GET.get('classid')
        group = request.GET.get('group')
        studentlist = CustomizeStudentList.objects.filter(classid=classid, studentgroup=int(group))
        studentidlist = []
        for student in studentlist:
            studentidlist.append(student.studentid)
        return JsonResponse(studentidlist, safe=False)

# Zenbo App ready
def zenbogetready(request):
    global groupsready
    group = request.GET.get('group')
    groupsready[int(group)-1] = 'ready'
    return JsonResponse({"result": "OK !"})

# Zenbo Check Section
def zenbochecksection(request):
    global customizesection
    group = request.GET.get('group')
    return JsonResponse({'section': customizesection[int(group)-1]})

# Zenbo ?????????????????????????????????
def zenbogetdiscussion(request):

    global customizediscussion
    group = request.GET.get('group')
    discussion = customizediscussion[int(group)-1]
    issue = CustomizeDiscussion.objects.get(issuename=discussion).issue
    sampleanswer = CustomizeDiscussion.objects.get(issuename=discussion).sampleanswer
    return JsonResponse({'issue': issue, "sampleanswer": sampleanswer})

# ?????????????????????zenbo junior??????
def customizestudentcheck(request):
    cId = request.GET.get('cId')
    student = CustomizeStudentList.objects.get(studentid=cId)
    student.studentcheck = "?????????"
    student.save()
    return JsonResponse({'cId': student.studentid, 'cName': student.studentname, 'cGroup': student.studentgroup})

# Nao?????????????????????????????????????????????
def checkallgroupready(request):
    global groupsready
    readygroup = 0
    for group in groupsready:
        if group == "ready":
            readygroup += 1
    if readygroup != len(groupsready):
        return JsonResponse({"result": "unready", "readygroupnum": readygroup})
    init_groupsready()
    return JsonResponse({"result": "ready"})

# Create your views here.