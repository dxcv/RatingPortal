#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .form import *
from .database.opratedb import *
from CreditRiskAnalysis.Algo.Bond1 import *
from CreditRiskAnalysis.Algo.Bond2 import *
from CreditRiskAnalysis.Algo.Bond3 import *


# 一般债项评级
def credit_rating_bond1(request):
    if request.method == 'POST':  # 当提交表单时
        form = FactorForm_Bond1(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            # 进行债券评级
            try:
                input_data = form.cleaned_data
                bond_code = input_data['bond_code']
                # 手工因子转化为字典
                factor_name = external_factor2name_bond1()
                other_score = {}
                for name in factor_name.keys():
                    other_score[name] = int(input_data[factor_name[name]])
                rating_data = Bond1(bond_code, other_score)
            except Exception as e:
                return render(request, 'credit_rating_iferr_bond1.html', {'form': form})

            # 将评级结果和评级记录输入数据库
            result_id = add_rating_result_bond1(request, rating_data, form.cleaned_data)

            # 提取网页输出的相关数据
            return HttpResponseRedirect('/credit_rating_detail/'+str(result_id))

        else:
            return render(request, 'credit_rating_bond1.html', {'form': form})

    else:  # 当正常访问时
        form = FactorForm_Bond1()
        return render(request, 'credit_rating_bond1.html', {'form': form})


# 城投债评级
def credit_rating_bond2(request):
    if request.method == 'POST':  # 当提交表单时
        form = FactorForm_Bond2(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            # 进行债券评级
            try:
                input_data = form.cleaned_data
                bond_code = input_data['bond_code']
                # 手工因子转化为字典
                factor_name = external_factor2name_bond2()
                other_score = {}
                for name in factor_name.keys():
                    other_score[name] = float(input_data[factor_name[name]])
                rating_data = Bond2(bond_code, other_score)
            except Exception as e:
                return render(request, 'credit_rating_iferr_bond2.html', {'form': form})

            # 将评级结果和评级记录输入数据库
            result_id = add_rating_result_bond2(request, rating_data, form.cleaned_data)

            # 提取网页输出的相关数据
            return HttpResponseRedirect('/credit_rating_detail/'+str(result_id))

        else:
            return render(request, 'credit_rating_bond3.html', {'form': form})

    else:  # 当正常访问时
        form = FactorForm_Bond2()
        return render(request, 'credit_rating_bond2.html', {'form': form})


# 地产债评级
def credit_rating_bond3(request):
    if request.method == 'POST':  # 当提交表单时
        form = FactorForm_Bond3(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            # 进行债券评级
            try:
                input_data = form.cleaned_data
                bond_code = input_data['bond_code']
                # 手工因子转化为字典
                factor_name = external_factor2name_bond3()
                other_score = {}
                for name in factor_name.keys():
                    other_score[name] = int(input_data[factor_name[name]])
                rating_data = Bond3(bond_code, other_score)
            except Exception as e:
                return render(request, 'credit_rating_iferr_bond3.html', {'form': form})

            # 将评级结果和评级记录输入数据库
            result_id = add_rating_result_bond3(request, rating_data, form.cleaned_data)

            # 提取网页输出的相关数据
            return HttpResponseRedirect('/credit_rating_detail/'+str(result_id))

        else:
            return render(request, 'credit_rating_bond3.html', {'form': form})

    else:  # 当正常访问时
        form = FactorForm_Bond3()
        return render(request, 'credit_rating_bond3.html', {'form': form})