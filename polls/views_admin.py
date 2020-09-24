from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from polls.models import AuthUser, TblAnswer
# 引入页码
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger


# 翻页函数
def pageMain(request, dateList, pagSize):
    backDict = {}
    page_size = int(pagSize) if pagSize else 10
    pageAry = []
    # 获取当前页 如果没有则为第1页
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(dateList, page_size)
    # 构建页码数组
    for i in paginator.page_range:
        pageAry.append(i)
    # 构建数组
    try:
        dateList = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        dateList = paginator.page(1)
    # 限制页码输出
    if page < 3:
        page_range = pageAry[0:5]
    elif page > paginator.num_pages - 2:
        if paginator.num_pages < 5:
            page_range = pageAry[0:paginator.num_pages]
        else:
            page_range = pageAry[paginator.num_pages - 5:paginator.num_pages]
    else:
        page_range = pageAry[page - 3:page + 2]
    backDict["dateList"] = dateList
    backDict["page_range"] = page_range
    return backDict


def login(request):
    request.session['title'] = "登录"
    js_script = None
    if request.method == 'POST':
        #   验证提交数据
        try:
            user = AuthUser.objects.get(username=request.POST.get('username'))
            if check_password(request.POST.get('password'), user.password):
                request.session['user_id'] = user.id
                return HttpResponseRedirect("/polls/questionnaireList")
            else:
                js_script = '''
                    mui.toast('账号或密码错误') 
                '''
        except Exception:
            js_script = '''
                    mui.toast('账号或密码错误') 
                '''
    return render(request, 'login.html', {'js_script': js_script})


def questionnaireList(request):
    if not request.session.get('user_id', False):
        return HttpResponseRedirect("/polls/login")
    else:
        request.session['title'] = '问卷列表'
        TblAnswers = TblAnswer.objects.all()
        date = pageMain(request, TblAnswers, 10)
        dateList = date['dateList']
        page_range = date['page_range']
        return render(request, 'list.html', {'dateList': dateList, 'page_range': page_range})