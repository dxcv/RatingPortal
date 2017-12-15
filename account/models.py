from django.db import models
from django.contrib import admin
from datetime import datetime
import django.contrib.auth.models as djmodels
import django

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password')

admin.site.register(User, UserAdmin)


# 信用评级记录：一般债项 Bond1
class CRRecord_Bond1(models.Model):
    user = models.ForeignKey(djmodels.User, null=False)
    create_time = models.DateTimeField(default=django.utils.timezone.now())
    bond_code = models.CharField(max_length=20)
    bond_type = models.CharField(max_length=20)
    bond_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=30)

    # 年报期间
    base_year = models.CharField(max_length=10)

    # 中间文件名称
    intermediate_data_file = models.CharField(max_length=50)

    # 评级结果（内部、外部）
    internal_score_debt = models.FloatField()
    internal_rating_debt = models.CharField(max_length=5)
    internal_score_company = models.FloatField()
    internal_rating_company = models.CharField(max_length=5)

    external_rating_debt = models.CharField(max_length=5, null=True)
    external_rating_company = models.CharField(max_length=5, null=True)

    # 手工因子
    background = models.IntegerField()
    background_remarks = models.CharField(max_length=50, null=True)
    industry = models.IntegerField()
    industry_remarks = models.CharField(max_length=50, null=True)
    external_warranty = models.IntegerField()
    external_warranty_remarks = models.CharField(max_length=50, null=True)
    asset_warranty = models.IntegerField()
    asset_warranty_remarks = models.CharField(max_length=50, null=True)
    industry_boom = models.IntegerField()
    industry_boom_remarks = models.CharField(max_length=50, null=True)
    industry_prospects = models.IntegerField()
    industry_prospects_remarks = models.CharField(max_length=50, null=True)
    industry_rank = models.IntegerField()
    industry_rank_remarks = models.CharField(max_length=50, null=True)
    fund_usage = models.IntegerField()
    fund_usage_remarks = models.CharField(max_length=50, null=True)
    future_expenditure = models.IntegerField()
    future_expenditure_remarks = models.CharField(max_length=50, null=True)

    # 自动计算的因子得分
    pct_major_shareholders = models.FloatField()                      # 大股东比例
    pct_profit_of_parent = models.FloatField()                        # 母公司利润占比
    total_asset = models.FloatField()                                 # 总资产规模
    net_asset = models.FloatField()                                   # 净资产规模
    net_asset_chg = models.FloatField()                               # 净资产变化率
    revenue = models.FloatField()                                     # 营业收入
    net_profit = models.FloatField()                                  # 净利润
    operating_profit = models.FloatField()                            # 营业利润
    EBITDA = models.FloatField()                                      # EBITDA
    operating_cashflow = models.FloatField()                          # 经营现金流净额
    gross_margin = models.FloatField()                                # 毛利率
    profit_margin = models.FloatField()                               # 净利率
    gross_margin_std = models.FloatField()                            # 过去三年毛利率标准差
    gross_margin_chg = models.FloatField()                            # 毛利率变化值
    roe = models.FloatField()                                         # ROE
    short_solvency_1 = models.FloatField()                            # (现金-短债)/净资产, 含应付应收
    short_solvency_2 = models.FloatField()                            # (现金-短债)/净资产，含有息债务
    debt_ratio_with_interest = models.FloatField()                    # 有息负债率
    debt_ratio_with_interest_chg = models.FloatField()                # 有息负债变化值
    debt_ratio = models.FloatField()                                  # 资产负债率
    cost_ratio = models.FloatField()                                  # 三费费率
    fixed_asset_ratio = models.FloatField()                           # 固定资产/总资产
    operating_cf_to_debt = models.FloatField()                        # 经营现金流/总债务
    operating_cf_std = models.FloatField()                            # 三年经营现金流波动
    ebitda_to_debt = models.FloatField()                              # EBITDA/总债务
    fixed_asset_turnover = models.FloatField()                        # 固定资产周转率
    inventory_turnover_days = models.FloatField()                     # 存货周转天数
    receivable_turnover_days = models.FloatField()                    # 应收账款周转天数
    rest_credit_to_debt = models.FloatField()                         # 未使用授信/总债务

    def __str__(self):
        return self.user.get_full_name()

# 信用评级记录：城投债 Bond2
class CRRecord_Bond2(models.Model):
    user = models.ForeignKey(djmodels.User, null=False)
    create_time = models.DateTimeField(default=django.utils.timezone.now())
    bond_code = models.CharField(max_length=20)
    bond_type = models.CharField(max_length=20)
    bond_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=30)

    # 年报期间
    base_year = models.CharField(max_length=10)

    # 中间文件名称
    intermediate_data_file = models.CharField(max_length=50)

    # 评级结果（内部、外部）
    internal_score_debt = models.FloatField()
    internal_rating_debt = models.CharField(max_length=5)
    internal_score_company = models.FloatField()
    internal_rating_company = models.CharField(max_length=5)

    external_rating_debt = models.CharField(max_length=5, null=True)
    external_rating_company = models.CharField(max_length=5, null=True)

    # 手工因子
    platform_status = models.IntegerField()
    platform_status_remarks = models.CharField(max_length=50, null=True)
    main_business = models.IntegerField()
    main_business_remarks = models.CharField(max_length=50, null=True)
    external_warranty = models.IntegerField()
    external_warranty_remarks = models.CharField(max_length=50, null=True)
    asset_warranty = models.IntegerField()
    asset_warranty_remarks = models.CharField(max_length=50, null=True)
    gov_fund_stability = models.IntegerField()
    gov_fund_stability_remarks = models.CharField(max_length=50, null=True)
    manual_adj = models.FloatField()
    manual_adj_remarks = models.CharField(max_length=50, null=True)
    GDP_amount = models.FloatField()
    GDP_amount_remarks = models.CharField(max_length=50, null=True)
    GDP_growth = models.FloatField()
    GDP_growth_remarks = models.CharField(max_length=50, null=True)
    public_revenue = models.FloatField()
    public_revenue_remarks = models.CharField(max_length=50, null=True)
    tax_to_revenue = models.FloatField()
    tax_to_revenue_remarks = models.CharField(max_length=50, null=True)

    # 自动计算的因子得分
    total_asset = models.FloatField()                                 # 总资产规模
    net_asset = models.FloatField()                                   # 净资产规模
    net_asset_chg = models.FloatField()                               # 净资产变化率
    revenue = models.FloatField()                                     # 营业收入
    net_profit = models.FloatField()                                  # 净利润
    operating_profit = models.FloatField()                            # 营业利润
    debt_ratio_with_interest = models.FloatField()                    # 有息负债率
    operating_cf_to_debt = models.FloatField()                        # 经营现金流/总债务

    def __str__(self):
        return self.user.get_full_name()

# 信用评级记录：地产债 Bond3
class CRRecord_Bond3(models.Model):
    user = models.ForeignKey(djmodels.User, null=False)
    create_time = models.DateTimeField(default=django.utils.timezone.now())
    bond_code = models.CharField(max_length=20)
    bond_type = models.CharField(max_length=20)
    bond_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=30)

    # 年报期间
    base_year = models.CharField(max_length=10)

    # 中间文件名称
    intermediate_data_file = models.CharField(max_length=50)

    # 评级结果（内部、外部）
    internal_score_debt = models.FloatField()
    internal_rating_debt = models.CharField(max_length=5)
    internal_score_company = models.FloatField()
    internal_rating_company = models.CharField(max_length=5)

    external_rating_debt = models.CharField(max_length=5, null=True)
    external_rating_company = models.CharField(max_length=5, null=True)

    # 手工因子
    background = models.IntegerField()
    background_remarks = models.CharField(max_length=50, null=True)
    industry = models.IntegerField()
    industry_remarks = models.CharField(max_length=50, null=True)
    external_warranty = models.IntegerField()
    external_warranty_remarks = models.CharField(max_length=50, null=True)
    asset_warranty = models.IntegerField()
    asset_warranty_remarks = models.CharField(max_length=50, null=True)
    industry_boom = models.IntegerField()
    industry_boom_remarks = models.CharField(max_length=50, null=True)
    industry_prospects = models.IntegerField()
    industry_prospects_remarks = models.CharField(max_length=50, null=True)
    industry_rank = models.IntegerField()
    industry_rank_remarks = models.CharField(max_length=50, null=True)
    land_reserve = models.IntegerField()
    land_reserve_remarks = models.CharField(max_length=50, null=True)
    future_expenditure = models.IntegerField()
    future_expenditure_remarks = models.CharField(max_length=50, null=True)

    # 自动计算的因子得分
    pct_major_shareholders = models.FloatField()                      # 大股东比例
    pct_profit_of_parent = models.FloatField()                        # 母公司利润占比
    total_asset = models.FloatField()                                 # 总资产规模
    net_asset = models.FloatField()                                   # 净资产规模
    net_asset_chg = models.FloatField()                               # 净资产变化率
    revenue = models.FloatField()                                     # 营业收入
    net_profit = models.FloatField()                                  # 净利润
    operating_profit = models.FloatField()                            # 营业利润
    EBITDA = models.FloatField()                                      # EBITDA
    operating_cashflow = models.FloatField()                          # 经营现金流净额
    gross_margin = models.FloatField()                                # 毛利率
    profit_margin = models.FloatField()                               # 净利率
    gross_margin_std = models.FloatField()                            # 过去三年毛利率标准差
    gross_margin_chg = models.FloatField()                            # 毛利率变化值
    roe = models.FloatField()                                         # ROE
    short_surplus = models.FloatField()                               # (现金-短债)/净资产
    cash_to_short_debt = models.FloatField()                          # 现金/短期负债
    net_debt_ratio = models.FloatField()                              # 净负债率
    net_debt_ratio_chg = models.FloatField()                          # 净负债率变化值
    debt_ratio = models.FloatField()                                  # 资产负债率
    cost_ratio = models.FloatField()                                  # 三费费率
    fixed_asset_ratio = models.FloatField()                           # 固定资产/总资产
    operating_cf_to_debt = models.FloatField()                        # 经营现金流/总债务
    operating_cf_std = models.FloatField()                            # 三年经营现金流波动
    ebitda_to_debt = models.FloatField()                              # EBITDA/总债务
    fixed_asset_turnover = models.FloatField()                        # 固定资产周转率
    inventory_turnover_days = models.FloatField()                     # 存货周转天数
    receivable_turnover_days = models.FloatField()                    # 应收账款周转天数
    rest_credit_to_debt = models.FloatField()                         # 未使用授信/总债务

    def __str__(self):
        return self.user.get_full_name()

# 信用评级结果
class CRResult(models.Model):
    # 评级信息
    user = models.ForeignKey(djmodels.User, null=False)
    create_time = models.DateTimeField(default=django.utils.timezone.now())
    bond_code = models.CharField(max_length=20)
    bond_type = models.CharField(max_length=20, null=True)
    bond_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=30)
    base_year = models.CharField(max_length=10)

    # 中间文件名称
    intermediate_data_file = models.CharField(max_length=50)

    # 评级结果（内部、外部）
    internal_score_debt = models.FloatField()
    internal_rating_debt = models.CharField(max_length=5)
    internal_score_company = models.FloatField()
    internal_rating_company = models.CharField(max_length=5)

    external_rating_debt = models.CharField(max_length=5, null=True)
    external_rating_company = models.CharField(max_length=5, null=True)

    record_bond1 = models.ForeignKey(CRRecord_Bond1, on_delete=models.CASCADE, related_name='record_bond1_id', null=True)
    record_bond2 = models.ForeignKey(CRRecord_Bond2, on_delete=models.CASCADE, related_name='record_bond2_id', null=True)
    record_bond3 = models.ForeignKey(CRRecord_Bond3, on_delete=models.CASCADE, related_name='record_bond3_id', null=True)

    def __str__(self):
        return self.user.get_full_name()
