#coding=utf-8

## 一般债项因子字典：Bond1
# 自定义因子字典
def external_factor2name_bond1():
    factor_name = dict()

    factor_name['企业性质'] = 'background'
    factor_name['行业因素'] = 'industry'
    factor_name['外部担保'] = 'external_warranty'
    factor_name['资产抵押担保'] = 'asset_warranty'
    factor_name['行业当前景气度'] = 'industry_boom'
    factor_name['行业未来6-12月趋势'] = 'industry_prospects'
    factor_name['公司的行业地位'] = 'industry_rank'
    factor_name['募投项目用途'] = 'fund_usage'
    factor_name['未来开支计划'] = 'future_expenditure'

    return factor_name


# Wind数据计算的因子字典
def wind_factor2name_bond1():
    factor_name = dict()

    factor_name["大股东比例"] = "pct_major_shareholders"
    factor_name["母公司利润占比"] = "pct_profit_of_parent"
    factor_name["总资产规模"] = "total_asset"
    factor_name["净资产规模"] = "net_asset"
    factor_name["净资产变化率"] = "net_asset_chg"
    factor_name["营业收入"] = "revenue"
    factor_name["净利润"] = "net_profit"
    factor_name["营业利润"] = "operating_profit"
    factor_name["EBITDA"] = "EBITDA"
    factor_name["经营现金流净额"] = "operating_cashflow"
    factor_name["毛利率"] = "gross_margin"
    factor_name["净利率"] = "profit_margin"
    factor_name["过去三年毛利率标准差"] = "gross_margin_std"
    factor_name["毛利率变化值"] = "gross_margin_chg"
    factor_name["ROE"] = "roe"
    factor_name["(现金-短债)/净资产, 含应付应收"] = "short_solvency_1"
    factor_name["(现金-短债)/净资产，含有息债务"] = "short_solvency_2"
    factor_name["有息负债率"] = "debt_ratio_with_interest"
    factor_name["有息负债变化值"] = "debt_ratio_with_interest_chg"
    factor_name["资产负债率"] = "debt_ratio"
    factor_name["三费费率"] = "cost_ratio"
    factor_name["固定资产/总资产"] = "fixed_asset_ratio"
    factor_name["经营现金流/总债务"] = "operating_cf_to_debt"
    factor_name["三年经营现金流波动"] = "operating_cf_std"
    factor_name["EBITDA/总债务"] = "ebitda_to_debt"
    factor_name["固定资产周转率"] = "fixed_asset_turnover"
    factor_name["存货周转天数"] = "inventory_turnover_days"
    factor_name["应收账款周转天数"] = "receivable_turnover_days"
    factor_name["未使用授信/总债务"] = "rest_credit_to_debt"

    return factor_name


# 全部因子字典
def all_factor2name_bond1():
    factor_name = external_factor2name_bond1()
    factor_name.update(wind_factor2name_bond1())

    return factor_name


## 城投债因子字典：Bond2
# 自定义因子字典
def external_factor2name_bond2():
    factor_name = dict()

    factor_name['平台地位'] = 'platform_status'
    factor_name['主营业务属性'] = 'main_business'
    factor_name['外部担保'] = 'external_warranty'
    factor_name['资产抵押担保'] = 'asset_warranty'
    factor_name['政府性基金收入稳定性'] = 'gov_fund_stability'
    factor_name['手工调整因素'] = 'manual_adj'
    factor_name['所属行政区GDP规模'] = 'GDP_amount'
    factor_name['GDP增长率'] = 'GDP_growth'
    factor_name['公共财政收入规模'] = 'public_revenue'
    factor_name['税收收入/公共财政收入'] = 'tax_to_revenue'

    return factor_name


# Wind数据计算的因子字典
def wind_factor2name_bond2():
    factor_name = dict()

    factor_name["总资产规模"] = "total_asset"
    factor_name["净资产规模"] = "net_asset"
    factor_name["净资产变化率"] = "net_asset_chg"
    factor_name["营业收入"] = "revenue"
    factor_name["净利润"] = "net_profit"
    factor_name["营业利润"] = "operating_profit"
    factor_name["有息负债率"] = "debt_ratio_with_interest"
    factor_name["经营现金流/总债务"] = "operating_cf_to_debt"

    return factor_name


# 全部因子字典
def all_factor2name_bond2():
    factor_name = external_factor2name_bond2()
    factor_name.update(wind_factor2name_bond2())

    return factor_name


## 地产因子字典：Bond3
# 自定义因子字典
def external_factor2name_bond3():
    factor_name = dict()

    factor_name['企业性质'] = 'background'
    factor_name['行业因素'] = 'industry'
    factor_name['外部担保'] = 'external_warranty'
    factor_name['资产抵押担保'] = 'asset_warranty'
    factor_name['行业当前景气度'] = 'industry_boom'
    factor_name['行业未来6-12月趋势'] = 'industry_prospects'
    factor_name['公司的行业地位'] = 'industry_rank'
    factor_name['土地储备数量及质量'] = 'land_reserve'
    factor_name['未来开支计划'] = 'future_expenditure'

    return factor_name


# Wind数据计算的因子字典
def wind_factor2name_bond3():
    factor_name = dict()

    factor_name["大股东比例"] = "pct_major_shareholders"
    factor_name["母公司利润占比"] = "pct_profit_of_parent"
    factor_name["总资产规模"] = "total_asset"
    factor_name["净资产规模"] = "net_asset"
    factor_name["净资产变化率"] = "net_asset_chg"
    factor_name["营业收入"] = "revenue"
    factor_name["净利润"] = "net_profit"
    factor_name["营业利润"] = "operating_profit"
    factor_name["EBITDA"] = "EBITDA"
    factor_name["经营现金流净额"] = "operating_cashflow"
    factor_name["毛利率"] = "gross_margin"
    factor_name["净利率"] = "profit_margin"
    factor_name["过去三年毛利率标准差"] = "gross_margin_std"
    factor_name["毛利率变化值"] = "gross_margin_chg"
    factor_name["ROE"] = "roe"
    factor_name["(现金-短债)/净资产"] = "short_surplus"
    factor_name["现金/短期负债"] = "cash_to_short_debt"
    factor_name["净负债率"] = "net_debt_ratio"
    factor_name["净负债率变化值"] = "net_debt_ratio_chg"
    factor_name["资产负债率"] = "debt_ratio"
    factor_name["三费费率"] = "cost_ratio"
    factor_name["固定资产/总资产"] = "fixed_asset_ratio"
    factor_name["经营现金流/总债务"] = "operating_cf_to_debt"
    factor_name["三年经营现金流波动"] = "operating_cf_std"
    factor_name["EBITDA/总债务(有息负债)"] = "ebitda_to_debt"
    factor_name["固定资产周转率"] = "fixed_asset_turnover"
    factor_name["存货周转天数"] = "inventory_turnover_days"
    factor_name["应收账款周转天数"] = "receivable_turnover_days"
    factor_name["未使用授信/总债务"] = "rest_credit_to_debt"

    return factor_name


# 全部因子字典
def all_factor2name_bond3():
    factor_name = external_factor2name_bond3()
    factor_name.update(wind_factor2name_bond3())

    return factor_name