from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import TblAnswer
import json


def index(request):
    request.session['title'] = "2020年嗨鹿人才盘点问卷—管理层"
    questions_config = [
        {
            "item_title": "建设团队与团队合作精神",
            "item_op": [
                "a、通过有效手段帮助团队扫除障碍或问题，形成良好的团队协作和凝聚力",
                "b、公开征求团队成员的不同意见，并利用这些意见改善决策的质量",
                "c、运用策略提升团队的士气和效能（例：录用和解聘的决定、团队任务分配、激励...）"
            ]
        },
        {
            "item_title": "鼓励创新",
            "item_op": [
                "a、理解和支持他人的新观点、新做法，鼓励并提倡工作中的创新举措",
                "b、对现有业务能够围绕目标提出创新思路和想法，并付诸实施，实现利润增长或价值增长"
            ]
        },
        {
            "item_title": "培育担责文化",
            "item_op": [
                "a、工作中积极敬业，愿意付出更多的工作时间和精力，为结果负责，用数据说话",
                "b、不好的绩效能勇于担责，不逃避责任，不找借口，不抱怨不消极，面对困难和压力，能积极释放和寻求解决方法，并有效执行",
                "c、能够向团队成员传递责任文化，建立团队的责任感和目标感，打造敬业和结果导向的团队"
            ]
        },
        {
            "item_title": "诚信",
            "item_op": [
                "a、遭受责难或面临抉择时，依然坚持道德准则、公认的规范和价值观",
                "b、认同并传播公司核心价值观，能作为公司行为规范的表率，并影响他人",
                "c、在涉及到个人利益时，能够很坚定的以大局为重，坚持原则，秉公处理，甚至牺牲自己的个人利益"
            ]
        },
        {
            "item_title": "激励领导力",
            "item_op": [
                "a、通过建立和发展共同目标或使命，有效激励员工，并激发潜能，形成高责任感、高效率的专业团队",
                "b、能以身作则、以行动为表率，尤其在面对压力和挑战时。保持积极正面的态度，第一时间承担责任，遇到问题反求诸己，即使面对无法抗拒的困难"
            ]
        },
        {
            "item_title": "战略执行",
            "item_op": [
                "a、充分理解公司的战略，并能有效的与下属或部门员工把战略沟通到位",
                "b、日常的核心工作能够围绕战略目标以及年度核心KPI来展开",
                "c、有效执行公司决策，对工作快速响应，并能反馈执行中的问题、处理突发性事件，使其不影响正常工作开展"
            ]
        },
        {
            "item_title": "学习导向",
            "item_op": [
                "a、愿意通过各种渠道尽力学习新知识、新技能，而不停留在自己所擅长的事，获得有利于未来发展的能力",
                "b、学以致用，将新的所学实际运用在工作上",
                "c、从失败和错误中汲取教训，探讨“我/我们从中学到什么”，杜绝错误的再次发生"
            ]
        },
        {
            "item_title": "发展意愿",
            "item_op": [
                "a、认同公司价值观和使命，有强烈的向上发展的意愿，不断追求上进，突破自我的意愿和行动。",
                "b、在履行本职工作基础上，积极承担额外的工作安排或主动接受挑战性、不熟悉的任务"
            ]
        }
    ]
    js_script = None
    from_data = None
    if request.GET.get("id"):
        try:
            temp = TblAnswer.objects.get(id=request.GET.get("id"))
            from_data = json.loads(temp.choice_ary_str)
            from_data['name'] = temp.name
        except:
            return HttpResponseRedirect("/polls/questionnaireList")
    if request.method == 'POST' and not request.GET.get("id"):
        from_data = request.POST
        #   验证提交数据
        radio_count = 0
        for key in request.POST.keys():
            radio_count += 1 if key.startswith('radio_') else 0
        if request.POST.get('name') and request.POST.get('level') and radio_count == 21:
            #   数据填写完整
            ary = request.POST.dict()   # 返回字典
            del ary['csrfmiddlewaretoken']  # 清理不要的键
            del ary['name']
            ary_str = json.dumps(ary)

            query = TblAnswer.objects.filter(name=request.POST.get('name'))
            if len(query) >= 1:
                query = query[0]
                if query.choice_ary_str:
                    js_script = '''
                                mui.toast('请检查姓名，该员工已填写问卷');
                                '''
                else:
                    query.choice_ary_str = ary_str
                    query.save()
                return HttpResponseRedirect("/polls/result")
            else:
                Answer = TblAnswer(name=request.POST.get('name'), choice_ary_str=ary_str)
                Answer.save()
                return HttpResponseRedirect("/polls/result")
        else:
            js_script = '''
                        mui.toast('请完整填写表单');
                        '''
    return render(request, 'index.html', {'questions_config': questions_config, 'from_data': from_data, 'js_script': js_script})


def visit(request):
    request.session['title'] = "2020年嗨鹿人才盘点访谈表"
    questions_config = [
        "您知道嗨鹿互动的企业文化是什么吗？",
        "您认为公司的组织架构是否合理？为什么？您所在部门的架构是什么？设立您所在部门的目的是什么？按照能力排序您所在的部门的员工？按照态度排序您所在的部门的员工？",
        "您的岗位职责是什么？您一周的工作时间如何分配？",
        "您个人的职业目标和发展方向是什么？您希望公司在您个人的发展上可以给与什么帮助？",
        "您认为公司的目标是否有为您的工作提供了明确的方向？",
        "您是否明确自己正在逐步实现目标？",
        "您是否希望自己有权制定必要的工作方案，以便有效地进行工作？",
        "在嗨鹿的这段日子里，您在工作中是否有机会学习和成长？",
    ]
    js_script = None
    from_data = None
    if request.GET.get("id"):
        try:
            temp = TblAnswer.objects.get(id=request.GET.get("id"))
            from_data = json.loads(temp.answer_ary_str)
            from_data['name'] = temp.name
        except:
            return HttpResponseRedirect("/polls/questionnaireList")
    if request.method == 'POST' and not request.GET.get("id"):
        from_data = request.POST
        #   验证提交数据
        text_complate = True
        for i, item in enumerate(questions_config):
            if not request.POST.get('text_name_'+str(i+1)):
                text_complate = False
                break
        if request.POST.get('name') and text_complate:
            #   数据填写完整
            ary = request.POST.dict()   # 返回字典
            del ary['csrfmiddlewaretoken']  # 清理不要的键
            del ary['name']
            ary_str = json.dumps(ary)

            query = TblAnswer.objects.filter(name=request.POST.get('name'))
            if len(query) >= 1:
                query = query[0]
                if query.answer_ary_str:
                    js_script = '''
                                mui.toast('请检查姓名，该员工已填写问卷');
                                '''
                else:
                    query.answer_ary_str = ary_str
                    query.save()
                return HttpResponseRedirect("/polls/result")
            else:
                Answer = TblAnswer(name=request.POST.get('name'), answer_ary_str=ary_str)
                Answer.save()
                return HttpResponseRedirect("/polls/result")
        else:
            js_script = '''
                        mui.toast('请完整填写表单');
                        '''
    return render(request, 'visit.html', {'questions_config': questions_config, 'from_data': from_data, 'js_script': js_script})


def result(request):
    request.session['title'] = ""
    return render(request, 'result.html', {})