from .GeneralBond import *
import pandas as pd
import numpy as np


class Bond2(GeneralBond):
    # load global config
    def __init__(self, bond_code, other_score=None):
        # 参数初始化
        GeneralBond.__init__(self, bond_code)
        self.base_year = self.wd.latestrep.strftime("%Y-%m-%d")
        self.bond_name = self.wd.bond_name
        self.company_name = self.wd.company_name

        self.year_len = 2
        self.raw_data_template = 'Bond2_RawDataFields'
        self.indicator2score_criterion = 'Bond2_Indicator2Score'
        self.factor_weight = 'Bond2_FactorWeight'
        self.score2rating_criterion = 'Bond2_Score2Rating'

        #提取数据、预处理、计算指标
        self.get_raw_data()
        self.pretreat_data()
        self.calc_indicators()

        # 内部评级 & 外部评级
        self.OtherScore = other_score
        self.indicators2score()
        self.weight_score_and_rating()

        self.external_rating()

    # get raw data from database
    def get_raw_data(self):
        GeneralBond.get_raw_data(self)            # general method

    # pretreat raw data: standardization,etc
    def pretreat_data(self):
        # delete the columns without valid data
        treated_data = self.raw_data.dropna(axis=1, how="all")

        # replace nan with 0
        self.treated_data = treated_data.replace(np.nan, 0)
        self.treated_data.ix["TOT_EQUITY"] = self.treated_data.ix["TOT_EQUITY"] - self.treated_data.ix["OTHER_EQUITY_INSTRUMENTS"]

    # calculate indicators
    def calc_indicators(self):
        unit = 1e8
        col_num = len(self.treated_data.columns)
        start_col = min(1, col_num)
        indicators = pd.DataFrame(columns=self.treated_data.columns[start_col:])

        indicators.ix["总资产规模"] = self.treated_data.ix["TOT_ASSETS"][start_col:] / unit
        indicators.ix["净资产规模"] = self.treated_data.ix["TOT_EQUITY"][start_col:] / unit
        indicators.ix["净资产变化率"] = (np.array(self.treated_data.ix["TOT_EQUITY"][start_col:]) / np.array(self.treated_data.ix["TOT_EQUITY"][start_col-1: col_num-1])) - 1

        indicators.ix["营业收入"] = self.treated_data.ix["TOT_OPER_REV"][start_col:] / unit
        indicators.ix["净利润"] = self.treated_data.ix["NET_PROFIT_IS"][start_col:] / unit
        indicators.ix["营业利润"] = self.treated_data.ix["OPPROFIT"][start_col:] / unit

        indicators.ix["有息负债率"] = ((self.treated_data.ix["ST_BORROW"] + self.treated_data.ix["BORROW_CENTRAL_BANK"]
                                         + self.treated_data.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + self.treated_data.ix["LT_BORROW"]
                                         + self.treated_data.ix["BONDS_PAYABLE"]) / self.treated_data.ix["TOT_ASSETS"])[start_col:]

        indicators.ix["经营现金流/总债务"] = ( self.treated_data.ix["NET_CASH_FLOWS_OPER_ACT"] /
                                      (self.treated_data.ix["ST_BORROW"] + self.treated_data.ix["BORROW_CENTRAL_BANK"]
                                       + self.treated_data.ix["TRADABLE_FIN_LIAB"] + self.treated_data.ix["NOTES_PAYABLE"]
                                       + self.treated_data.ix["ACCT_PAYABLE"] + self.treated_data.ix["HANDLING_CHARGES_COMM_PAYABLE"]
                                       + self.treated_data.ix["EMPL_BEN_PAYABLE"] + self.treated_data.ix["TAXES_SURCHARGES_PAYABLE"]
                                       + self.treated_data.ix["INT_PAYABLE"] + self.treated_data.ix["OTH_PAYABLE"]
                                       + self.treated_data.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + self.treated_data.ix["LT_BORROW"]
                                       + self.treated_data.ix["BONDS_PAYABLE"] + self.treated_data.ix["LT_PAYABLE"]
                                       + self.treated_data.ix["SPECIFIC_ITEM_PAYABLE"]) )[start_col:]

        self.indicators = indicators

    # convert indicators to standard score
    def indicators2score(self):
        name_list1 = ['所属行政区GDP规模', 'GDP增长率', '公共财政收入规模', '税收收入/公共财政收入']
        name_list2 = ['平台地位', '主营业务属性', '外部担保', '资产抵押担保', '政府性基金收入稳定性', '手工调整因素']

        # 将需要评分的外部因子整合到indicator中
        for name in name_list1:
            self.indicators.loc[name] = self.OtherScore[name]

        GeneralBond.indicators2score(self)   # use general method from base class

        # 将外部手工因子dict类型合并到计算好的因子中
        for name in name_list2:
            self.score.ix[name] = self.OtherScore[name]

    # calculate weighted score and do rating
    def weight_score_and_rating(self):
        weight = self.config.getConfig('Excel', self.factor_weight)
        weight = pd.read_excel(weight)

        rate = pd.DataFrame(columns=self.score.columns)

        self.score = self.score.reindex(weight.index)
        rate.ix["内部得分-债项"] = np.dot(weight.T, self.score)[0]
        rate.ix["内部评级-债项"] = self.score2rating(rate.ix["内部得分-债项"])
        weight_body = weight.drop(["外部担保", "资产抵押担保"], axis=0)
        df_score_body = self.score.drop(["外部担保", "资产抵押担保"], axis=0)
        rate.ix["内部得分-主体"] = np.dot(weight_body.T, df_score_body)[0]
        rate.ix["内部评级-主体"] = self.score2rating(rate.ix["内部得分-主体"])

        self.rate = rate
