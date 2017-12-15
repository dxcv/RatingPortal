#coding=utf-8
from django import forms

# 债券类型表单
#bond_type_class = (('none', '--请选择债券类型--'), ('Bond1', '一般债项'), ('Bond2', '地产债'), ('Bond3', '城投债'))
bond_type_class = (('--请选择债券类型--', '--请选择债券类型--'), ('一般债项', '一般债项'), ('地产债', '地产债'), ('城投债', '城投债'))

# 查询校招信息表单
class Select_Bond_Type(forms.Form):
    bond_type = forms.ChoiceField(required=True, label='债券类型', choices=bond_type_class)


# 用户表单
class UserForm(forms.Form):
    username = forms.CharField(required=True, label='用户名', max_length=30)
    password = forms.CharField(required=True, label='密__码', widget=forms.PasswordInput())


# 一般债项手工因子表单 Bond1
class FactorForm_Bond1(forms.Form):
    bond_code = forms.CharField(required=True, label='债券代码', max_length=20)

    background = forms.IntegerField(label='企业性质')
    background_remarks = forms.CharField(label='企业性质备注', required=False)
    industry = forms.IntegerField(label='行业因素')
    industry_remarks = forms.CharField(label='行业因素备注', required=False)
    external_warranty = forms.IntegerField(label='外部担保')
    external_warranty_remarks = forms.CharField(label='外部担保备注', required=False)
    asset_warranty = forms.IntegerField(label='资产抵押担保')
    asset_warranty_remarks = forms.CharField(label='资产抵押担保备注', required=False)
    industry_boom = forms.IntegerField(label='行业当前景气度')
    industry_boom_remarks = forms.CharField(label='行业当前景气度备注', required=False)
    industry_prospects = forms.IntegerField(label='行业未来6-12月趋势')
    industry_prospects_remarks = forms.CharField(label='行业未来6-12月趋势备注', required=False)
    industry_rank = forms.IntegerField(label='公司的行业地位')
    industry_rank_remarks = forms.CharField(label='公司的行业地位备注', required=False)
    fund_usage = forms.IntegerField(label='募投项目用途')
    fund_usage_remarks = forms.CharField(label='募投项目用途备注', required=False)
    future_expenditure = forms.IntegerField(label='未来开支计划')
    future_expenditure_remarks = forms.CharField(label='未来开支计划备注', required=False)


# 城投债手工因子表单 Bond2
class FactorForm_Bond2(forms.Form):
    bond_code = forms.CharField(required=True, label='债券代码', max_length=20)

    platform_status = forms.IntegerField(label='平台地位')
    platform_status_remarks = forms.CharField(label='平台地位备注', required=False)
    main_business = forms.IntegerField(label='主营业务属性')
    main_business_remarks = forms.CharField(label='主营业务属性备注', required=False)
    external_warranty = forms.IntegerField(label='外部担保')
    external_warranty_remarks = forms.CharField(label='外部担保备注', required=False)
    asset_warranty = forms.IntegerField(label='资产抵押担保')
    asset_warranty_remarks = forms.CharField(label='资产抵押担保备注', required=False)
    gov_fund_stability = forms.IntegerField(label='政府性基金收入稳定性')
    gov_fund_stability_remarks = forms.CharField(label='政府性基金收入稳定性备注', required=False)
    manual_adj = forms.FloatField(label='手工调整因素')
    manual_adj_remarks = forms.CharField(label='手工调整因素备注', required=False)
    GDP_amount = forms.FloatField(label='所属行政区GDP规模')
    GDP_amount_remarks = forms.CharField(label='所属行政区GDP规模备注', required=False)
    GDP_growth = forms.FloatField(label='GDP增长率')
    GDP_growth_remarks = forms.CharField(label='GDP增长率备注', required=False)
    public_revenue = forms.FloatField(label='公共财政收入规模')
    public_revenue_remarks = forms.CharField(label='公共财政收入规模备注', required=False)
    tax_to_revenue = forms.FloatField(label='税收收入/公共财政收入')
    tax_to_revenue_remarks = forms.CharField(label='税收收入/公共财政收入备注', required=False)


# 城投债手工因子表单 Bond3
class FactorForm_Bond3(forms.Form):
    bond_code = forms.CharField(required=True, label='债券代码', max_length=20)

    background = forms.IntegerField(label='企业性质')
    background_remarks = forms.CharField(label='企业性质备注', required=False)
    industry = forms.IntegerField(label='行业因素')
    industry_remarks = forms.CharField(label='行业因素备注', required=False)
    external_warranty = forms.IntegerField(label='外部担保')
    external_warranty_remarks = forms.CharField(label='外部担保备注', required=False)
    asset_warranty = forms.IntegerField(label='资产抵押担保')
    asset_warranty_remarks = forms.CharField(label='资产抵押担保备注', required=False)
    industry_boom = forms.IntegerField(label='行业当前景气度')
    industry_boom_remarks = forms.CharField(label='行业当前景气度备注', required=False)
    industry_prospects = forms.IntegerField(label='行业未来6-12月趋势')
    industry_prospects_remarks = forms.CharField(label='行业未来6-12月趋势备注', required=False)
    industry_rank = forms.IntegerField(label='公司的行业地位')
    industry_rank_remarks = forms.CharField(label='公司的行业地位备注', required=False)
    land_reserve = forms.IntegerField(label='土地储备数量及质量')
    land_reserve_remarks = forms.CharField(label='土地储备数量及质量备注', required=False)
    future_expenditure = forms.IntegerField(label='未来开支计划')
    future_expenditure_remarks = forms.CharField(label='未来开支计划备注', required=False)