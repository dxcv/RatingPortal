#coding=utf-8
from .insert_ratingdata import *


# 查询本人所有评级历史记录 CRRecord
def read_rating_record(request, bond_code=None):
    username = request.user
    user = djmodels.User.objects.get(username=username)
    try:
        if bond_code is not None:     # 指定债券的评级结果
            result_test = CRRecord.objects.filter(user=user, bond_code=bond_code)
        else:                         # 所有债券的评级结果
            result_test = CRRecord.objects.filter(user=user)
    except Exception as e:
        return None

    if len(result_test) == 0:
        return None

    return result_test.order_by("-id")


# 查询所有债券/指定债券评级历史记录 CRResult
def read_rating_result(user=None, bond_code='all', bond_name='all', bond_type='all'):
    try:
        if user is None:              # 所有用户的结果
            result_test = CRResult.objects.all()
        else:
            result_test = CRResult.objects.filter(user=user)

        if bond_code == 'all':        # 所有债券代码的评级结果
            pass
        else:                         # 指定债券代码的评级结果
            result_test = result_test.filter(bond_code__icontains=bond_code)

        if bond_name == 'all':        # 所有债券名称的评级结果
            pass
        else:                         # 指定债券代码的评级结果
            result_test = result_test.filter(bond_name__icontains=bond_name)

        if bond_type == 'all':        # 所有债券类型的评级结果
            pass
        else:                         # 指定债券类型的评级结果
            result_test = result_test.filter(bond_type__icontains=bond_type)

    except Exception as e:
        return None

    if len(result_test) == 0:
        return None

    return result_test.order_by("-id")


# 查询某一条result对应的record
def result_to_record(result_id):
    result = CRResult.objects.get(id=result_id)
    if result.bond_type == '一般债项':
        record = CRRecord_Bond1.objects.get(id=result.record_bond1_id)
    elif result.bond_type == '城投债':
        record = CRRecord_Bond2.objects.get(id=result.record_bond2_id)
    elif result.bond_type == '地产债':
        record = CRRecord_Bond3.objects.get(id=result.record_bond3_id)

    return record


# 删除某一条result
def delete_rating_result(result_id):

    record = result_to_record(result_id)
    record.delete()

    return

