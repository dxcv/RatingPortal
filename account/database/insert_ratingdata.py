#coding=utf-8
import time
import pandas as pd
import numpy as np
from ..models import *
from ..dictionary import *
import django.contrib.auth.models as djmodels
from datetime import datetime


# 将输入的外部数据转换成DataFrame
def out_factor_to_DF(input_data, bond_type):
    if bond_type == 'bond1':
        ef = external_factor2name_bond1()
    elif bond_type == 'bond2':
        ef = external_factor2name_bond2()
    elif bond_type == 'bond3':
        ef = external_factor2name_bond3()

    data = pd.DataFrame(np.nan, index=list(ef.keys()), columns=['得分', '备注'])
    for name in ef.keys():
        data.loc[name, '得分'] = input_data[ef[name]]
        data.loc[name, '备注'] = input_data[ef[name]+"_remarks"]

    return data


# 将评级的过程存储到excel
def rateing_process_to_excel(user, input_data, rating_data, bond_type):
    # 存储中间数据到Excel
    out_factor = out_factor_to_DF(input_data, bond_type)
    filename = user.get_username() + "_" + rating_data.bond_code + "_" \
               + time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())) + '.xls'
    # write to excel
    writer = pd.ExcelWriter("./IntermediateData/" + filename)
    rating_data.raw_data.to_excel(writer, 'raw_data', index=True)
    rating_data.indicators.to_excel(writer, 'factor_value', index=True)
    rating_data.score.to_excel(writer, 'factor_score', index=True)
    rating_data.rate.to_excel(writer, 'credit_rate', index=True)
    out_factor.to_excel(writer, 'out_factor', index=True)
    writer.save()

    return filename


# 插入评级结果
def insert_rating_result(user, create_time, rating_data, in_rating, out_rating, insert_record, bond_type):
    insert_result = CRResult.objects.create(
        user=user,
        create_time=create_time,
        bond_code=rating_data.bond_code,
        #bond_type=bond_type,
        bond_name=rating_data.bond_name,
        company_name=rating_data.company_name,
        base_year=rating_data.base_year,
        intermediate_data_file=insert_record.intermediate_data_file,

        # 评级结果（内部、外部）
        internal_score_debt=np.round(in_rating['内部得分-债项'], 2),
        internal_rating_debt=in_rating['内部评级-债项'],
        internal_score_company=np.round(in_rating['内部得分-主体'], 2),
        internal_rating_company=in_rating['内部评级-主体'],

        external_rating_debt=out_rating['债项'],
        external_rating_company=out_rating['主体'],
        #record=insert_record
    )

    if bond_type == 'bond1':
        insert_result.bond_type = "一般债项"
        insert_result.record_bond1 = insert_record
    elif bond_type == 'bond2':
        insert_result.bond_type = "城投债"
        insert_result.record_bond2 = insert_record
    elif bond_type == 'bond3':
        insert_result.bond_type = "地产债"
        insert_result.record_bond3 = insert_record

    insert_result.save()

    return insert_result.id


# 将评级结果和记录输入数据库：一般债项 bond1
def add_rating_result_bond1(request, rating_data, input_data):
    # 提取相关数据
    factor = rating_data.score.copy()
    # 因子名称改成数据库字段名
    factor_name = all_factor2name_bond1()
    factor.index = [factor_name[name] for name in factor.index]
    factor = factor[factor.columns[0]]

    # 评级数据
    in_rating = rating_data.rate.copy()
    in_rating = in_rating[in_rating.columns[0]]
    out_rating = rating_data.rate_outside.copy()
    out_rating = out_rating[out_rating.columns[0]]

    username = request.user
    user = djmodels.User.objects.get(username=username)

    # 评级过程存储到excel
    filename = rateing_process_to_excel(user, input_data, rating_data, "bond1")

    create_time = datetime.now()
    #评级记录插入数据库
    insert_record = CRRecord_Bond1.objects.create(
        user=user,
        create_time=create_time,
        bond_code=rating_data.bond_code,
        bond_type="一般债项",
        bond_name=rating_data.bond_name,
        company_name=rating_data.company_name,

        # 年报期间
        base_year=rating_data.base_year,

        # 中间文件名称
        intermediate_data_file=filename,

        # 评级结果（内部、外部）
        internal_score_debt=np.round(in_rating['内部得分-债项'], 2),
        internal_rating_debt=in_rating['内部评级-债项'],
        internal_score_company=np.round(in_rating['内部得分-主体'], 2),
        internal_rating_company=in_rating['内部评级-主体'],

        external_rating_debt=out_rating['债项'],
        external_rating_company=out_rating['主体'],

        # 手工因子
        background=factor['background'],
        background_remarks=input_data['background_remarks'],
        industry=factor['industry'],
        industry_remarks=input_data['industry_remarks'],
        external_warranty=factor['external_warranty'],
        external_warranty_remarks=input_data['external_warranty_remarks'],
        asset_warranty=factor['asset_warranty'],
        asset_warranty_remarks=input_data['asset_warranty_remarks'],
        industry_boom=factor['industry_boom'],
        industry_boom_remarks=input_data['industry_boom_remarks'],
        industry_prospects=factor['industry_prospects'],
        industry_prospects_remarks=input_data['industry_prospects_remarks'],
        industry_rank=factor['industry_rank'],
        industry_rank_remarks=input_data['industry_rank_remarks'],
        fund_usage=factor['fund_usage'],
        fund_usage_remarks=input_data['fund_usage_remarks'],
        future_expenditure=factor['future_expenditure'],
        future_expenditure_remarks=input_data['future_expenditure_remarks'],

        # 自动计算的因子得分
        pct_major_shareholders=factor['pct_major_shareholders'],
        pct_profit_of_parent=factor['pct_profit_of_parent'],
        total_asset=factor['total_asset'],
        net_asset=factor['net_asset'],
        net_asset_chg=factor['net_asset_chg'],
        revenue=factor['revenue'],
        net_profit=factor['net_profit'],
        operating_profit=factor['operating_profit'],
        EBITDA=factor['EBITDA'],
        operating_cashflow=factor['operating_cashflow'],
        gross_margin=factor['gross_margin'],
        profit_margin=factor['profit_margin'],
        gross_margin_std=factor['gross_margin_std'],
        gross_margin_chg=factor['gross_margin_chg'],
        roe=factor['roe'],
        short_solvency_1=factor['short_solvency_1'],
        short_solvency_2=factor['short_solvency_2'],
        debt_ratio_with_interest=factor['debt_ratio_with_interest'],
        debt_ratio_with_interest_chg=factor['debt_ratio_with_interest_chg'],
        debt_ratio=factor['debt_ratio'],
        cost_ratio=factor['cost_ratio'],
        fixed_asset_ratio=factor['fixed_asset_ratio'],
        operating_cf_to_debt=factor['operating_cf_to_debt'],
        operating_cf_std=factor['operating_cf_std'],
        ebitda_to_debt=factor['ebitda_to_debt'],
        fixed_asset_turnover=factor['fixed_asset_turnover'],
        inventory_turnover_days=factor['inventory_turnover_days'],
        receivable_turnover_days=factor['receivable_turnover_days'],
        rest_credit_to_debt=factor['rest_credit_to_debt']
    )

    result_id = insert_rating_result(user, create_time, rating_data, in_rating, out_rating, insert_record, "bond1")

    return result_id


# 将评级结果和记录输入数据库：城投债 bond2
def add_rating_result_bond2(request, rating_data, input_data):
    # 提取相关数据
    factor = rating_data.score.copy()
    # 因子名称改成数据库字段名
    factor_name = all_factor2name_bond2()
    factor.index = [factor_name[name] for name in factor.index]
    factor = factor[factor.columns[0]]

    # 评级数据
    in_rating = rating_data.rate.copy()
    in_rating = in_rating[in_rating.columns[0]]
    out_rating = rating_data.rate_outside.copy()
    out_rating = out_rating[out_rating.columns[0]]

    username = request.user
    user = djmodels.User.objects.get(username=username)

    # 评级过程存储到excel
    filename = rateing_process_to_excel(user, input_data, rating_data, "bond2")

    create_time = datetime.now()
    #评级记录插入数据库
    insert_record = CRRecord_Bond2.objects.create(
        user=user,
        create_time=create_time,
        bond_code=rating_data.bond_code,
        bond_type="城投债",
        bond_name=rating_data.bond_name,
        company_name=rating_data.company_name,

        # 年报期间
        base_year=rating_data.base_year,

        # 中间文件名称
        intermediate_data_file=filename,

        # 评级结果（内部、外部）
        internal_score_debt=np.round(in_rating['内部得分-债项'], 2),
        internal_rating_debt=in_rating['内部评级-债项'],
        internal_score_company=np.round(in_rating['内部得分-主体'], 2),
        internal_rating_company=in_rating['内部评级-主体'],

        external_rating_debt=out_rating['债项'],
        external_rating_company=out_rating['主体'],

        # 手工因子
        platform_status=factor['platform_status'],
        platform_status_remarks=input_data['platform_status_remarks'],
        main_business=factor['main_business'],
        main_business_remarks=input_data['main_business_remarks'],
        external_warranty=factor['external_warranty'],
        external_warranty_remarks=input_data['external_warranty_remarks'],
        asset_warranty=factor['asset_warranty'],
        asset_warranty_remarks=input_data['asset_warranty_remarks'],
        gov_fund_stability=factor['gov_fund_stability'],
        gov_fund_stability_remarks=input_data['gov_fund_stability_remarks'],
        manual_adj=factor['manual_adj'],
        manual_adj_remarks=input_data['manual_adj_remarks'],
        GDP_amount=factor['GDP_amount'],
        GDP_amount_remarks=input_data['GDP_amount_remarks'],
        GDP_growth=factor['GDP_growth'],
        GDP_growth_remarks=input_data['GDP_growth_remarks'],
        public_revenue=factor['public_revenue'],
        public_revenue_remarks=input_data['public_revenue_remarks'],
        tax_to_revenue=factor['tax_to_revenue'],
        tax_to_revenue_remarks=input_data['tax_to_revenue_remarks'],

        # 自动计算的因子得分
        total_asset=factor['total_asset'],
        net_asset=factor['net_asset'],
        net_asset_chg=factor['net_asset_chg'],
        revenue=factor['revenue'],
        net_profit=factor['net_profit'],
        operating_profit=factor['operating_profit'],
        debt_ratio_with_interest=factor['debt_ratio_with_interest'],
        operating_cf_to_debt=factor['operating_cf_to_debt']
    )

    result_id = insert_rating_result(user, create_time, rating_data, in_rating, out_rating, insert_record, "bond2")

    return result_id


# 将评级结果和记录输入数据库：地产债 bond3
def add_rating_result_bond3(request, rating_data, input_data):
    # 提取相关数据
    factor = rating_data.score.copy()
    # 因子名称改成数据库字段名
    factor_name = all_factor2name_bond3()
    factor.index = [factor_name[name] for name in factor.index]
    factor = factor[factor.columns[0]]

    # 评级数据
    in_rating = rating_data.rate.copy()
    in_rating = in_rating[in_rating.columns[0]]
    out_rating = rating_data.rate_outside.copy()
    out_rating = out_rating[out_rating.columns[0]]

    username = request.user
    user = djmodels.User.objects.get(username=username)

    # 评级过程存储到excel
    filename = rateing_process_to_excel(user, input_data, rating_data, "bond3")

    create_time = datetime.now()
    #评级记录插入数据库
    insert_record = CRRecord_Bond3.objects.create(
        user=user,
        create_time=create_time,
        bond_code=rating_data.bond_code,
        bond_type="地产债",
        bond_name=rating_data.bond_name,
        company_name=rating_data.company_name,

        # 年报期间
        base_year=rating_data.base_year,

        # 中间文件名称
        intermediate_data_file=filename,

        # 评级结果（内部、外部）
        internal_score_debt=np.round(in_rating['内部得分-债项'], 2),
        internal_rating_debt=in_rating['内部评级-债项'],
        internal_score_company=np.round(in_rating['内部得分-主体'], 2),
        internal_rating_company=in_rating['内部评级-主体'],

        external_rating_debt=out_rating['债项'],
        external_rating_company=out_rating['主体'],

        # 手工因子
        background=factor['background'],
        background_remarks=input_data['background_remarks'],
        industry=factor['industry'],
        industry_remarks=input_data['industry_remarks'],
        external_warranty=factor['external_warranty'],
        external_warranty_remarks=input_data['external_warranty_remarks'],
        asset_warranty=factor['asset_warranty'],
        asset_warranty_remarks=input_data['asset_warranty_remarks'],
        industry_boom=factor['industry_boom'],
        industry_boom_remarks=input_data['industry_boom_remarks'],
        industry_prospects=factor['industry_prospects'],
        industry_prospects_remarks=input_data['industry_prospects_remarks'],
        industry_rank=factor['industry_rank'],
        industry_rank_remarks=input_data['industry_rank_remarks'],
        land_reserve=factor['land_reserve'],
        land_reserve_remarks=input_data['land_reserve_remarks'],
        future_expenditure=factor['future_expenditure'],
        future_expenditure_remarks=input_data['future_expenditure_remarks'],

        # 自动计算的因子得分
        pct_major_shareholders=factor['pct_major_shareholders'],
        pct_profit_of_parent=factor['pct_profit_of_parent'],
        total_asset=factor['total_asset'],
        net_asset=factor['net_asset'],
        net_asset_chg=factor['net_asset_chg'],
        revenue=factor['revenue'],
        net_profit=factor['net_profit'],
        operating_profit=factor['operating_profit'],
        EBITDA=factor['EBITDA'],
        operating_cashflow=factor['operating_cashflow'],
        gross_margin=factor['gross_margin'],
        profit_margin=factor['profit_margin'],
        gross_margin_std=factor['gross_margin_std'],
        gross_margin_chg=factor['gross_margin_chg'],
        roe=factor['roe'],
        short_surplus=factor['short_surplus'],
        cash_to_short_debt=factor['cash_to_short_debt'],
        net_debt_ratio=factor['net_debt_ratio'],
        net_debt_ratio_chg=factor['net_debt_ratio_chg'],
        debt_ratio=factor['debt_ratio'],
        cost_ratio=factor['cost_ratio'],
        fixed_asset_ratio=factor['fixed_asset_ratio'],
        operating_cf_to_debt=factor['operating_cf_to_debt'],
        operating_cf_std=factor['operating_cf_std'],
        ebitda_to_debt=factor['ebitda_to_debt'],
        fixed_asset_turnover=factor['fixed_asset_turnover'],
        inventory_turnover_days=factor['inventory_turnover_days'],
        receivable_turnover_days=factor['receivable_turnover_days'],
        rest_credit_to_debt=factor['rest_credit_to_debt']
    )

    result_id = insert_rating_result(user, create_time, rating_data, in_rating, out_rating, insert_record, "bond3")

    return result_id
