#coding=utf-8
from django.shortcuts import render_to_response
from django.contrib import auth
from django.http import StreamingHttpResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from .do_credit_rating import *

# Create your views here.
# 登录界面
def login(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                return render_to_response('login_err.html', {'userform': userform})
    else:
        userform = UserForm()
        return render_to_response('login.html', {'userform': userform})


# 登出功能
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


# 主页界面
@login_required(redirect_field_name='next', login_url='/login/')
def home(request):
    group = djmodels.Group.objects.get(user=request.user)
    return render(request, 'home.html', {'manager': str(group) == 'manager'})


# 债券评级页面
@login_required(redirect_field_name='next', login_url='/login/')
def credit_rating(request, bond_type):
    if bond_type == 'bond1':
        return credit_rating_bond1(request)
    elif bond_type == 'bond2':
        return credit_rating_bond2(request)
    elif bond_type == 'bond3':
        return credit_rating_bond3(request)


# 查询评级结果
@login_required(redirect_field_name='next', login_url='/login/')
def rating_result(request, bond_code, bond_name, bond_type):
    if str(djmodels.Group.objects.get(user=request.user)) != 'manager':
        return render(request, 'permission_deny.html')

    form = Select_Bond_Type()
    if request.method == 'POST':  # 当提交表单时
        bond_code = request.POST['bond_code']
        bond_name = request.POST['bond_name']
        bond_type = request.POST['bond_type']

        if len(bond_code) == 0:     # 表单为空
            bond_code = 'all'
        if len(bond_name) == 0:
            bond_name = 'all'
        if bond_type == '--请选择债券类型--':
            bond_type = 'all'

        return HttpResponseRedirect('/credit_rating_result/' + bond_code + "/" + bond_name + "/" + bond_type + "/")

    else:
        rating_res = read_rating_result(bond_code=bond_code, bond_name=bond_name, bond_type=bond_type)
        if rating_res is None:
            no_record = True
        else:
            no_record = False

        return render(request, 'credit_rating_result.html', {'rating_res': rating_res, 'no_record': no_record, 'form':form})


# 查询某一用户评级历史
@login_required(redirect_field_name='next', login_url='/login/')
def user_rating_history(request, bond_code, bond_name, bond_type):
    form = Select_Bond_Type()
    if request.method == 'POST':  # 当提交表单时
        bond_code = request.POST['bond_code']
        bond_name = request.POST['bond_name']
        bond_type = request.POST['bond_type']

        if len(bond_code) == 0:     # 表单为空
            bond_code = 'all'
        if len(bond_name) == 0:
            bond_name = 'all'
        if bond_type == '--请选择债券类型--':
            bond_type = 'all'

        return HttpResponseRedirect('/credit_rating_history/' + bond_code + "/" + bond_name + "/" + bond_type + "/")

    else:
        username = request.user
        user = djmodels.User.objects.get(username=username)

        rating_res = read_rating_result(user=user, bond_code=bond_code, bond_name=bond_name, bond_type=bond_type)
        if rating_res is None:
            no_record = True
        else:
            no_record = False

        return render(request, 'credit_rating_history.html', {'rating_res': rating_res, 'no_record': no_record, 'form':form})


# 查询某一条评级结果的详细评级信息
@login_required(redirect_field_name='next', login_url='/login/')
def rating_detail(request, result_id):
    record = result_to_record(result_id)

    if record.user != djmodels.User.objects.get(username=request.user) and str(djmodels.Group.objects.get(user=request.user)) != 'manager':
            return render(request, 'permission_deny.html')

    pre_url = request.META.get('HTTP_REFERER', "/")

    if record.bond_type == "一般债项":
        return render(request, 'rating_detail_bond1.html', {'form': record, 'pre_url': pre_url})
    elif record.bond_type == "城投债":
        return render(request, 'rating_detail_bond2.html', {'form': record, 'pre_url': pre_url})
    if record.bond_type == "地产债":
        return render(request, 'rating_detail_bond3.html', {'form': record, 'pre_url': pre_url})


# 删除某一条评级结果
@login_required(redirect_field_name='next', login_url='/login/')
def delete_result(request, result_id):
    if str(djmodels.Group.objects.get(user=request.user)) != 'manager':
        return render(request, 'permission_deny.html')

    delete_rating_result(result_id)

    pre_url = request.META.get('HTTP_REFERER', "/")
    return HttpResponseRedirect(pre_url)


# 下载评级的中间文件
@login_required(redirect_field_name='next', login_url='/login/')
def download_file(request, result_id):
    record = result_to_record(result_id)
    if record.user != djmodels.User.objects.get(username=request.user) and str(djmodels.Group.objects.get(user=request.user)) != 'manager':
            return render(request, 'permission_deny.html')

    filename = record.intermediate_data_file
    full_filename = "./IntermediateData/" + filename  # 要下载的文件路径
    response = StreamingHttpResponse(read_file(full_filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response


def read_file(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

