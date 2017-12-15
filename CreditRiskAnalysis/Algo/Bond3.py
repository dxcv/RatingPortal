from .GeneralBond import *
import pandas as pd
import numpy as np


class Bond3(GeneralBond):
    # load global config
    def __init__(self, bond_code, other_score=None):
        # 参数初始化
        GeneralBond.__init__(self, bond_code)
        self.base_year = self.wd.latestrep.strftime("%Y-%m-%d")
        self.bond_name = self.wd.bond_name
        self.company_name = self.wd.company_name

        self.year_len = 3
        self.raw_data_template = 'Bond3_RawDataFields'
        self.indicator2score_criterion = 'Bond3_Indicator2Score'
        self.factor_weight = 'Bond3_FactorWeight'
        self.score2rating_criterion = 'Bond3_Score2Rating'

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

        # 读取该债券评级特定数据             # individual method
        hold_data = self.wd.QueryShareHolderData(self.year_len)
        self.raw_data = pd.concat([self.raw_data, hold_data], axis=0)
        self.raw_data.loc['CREDIT_UNUSED'] = self.wd.QueryUnusedCredit()

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
        start_col = min(2, col_num)
        indicators = pd.DataFrame(columns=self.treated_data.columns[start_col:])

        indicators.ix["大股东比例"] = self.treated_data.ix["HOLDER_PCT"][start_col:] / 100
        indicators.ix["母公司利润占比"] = self.treated_data.ix["NP_BELONGTO_PARCOMSH"] / self.treated_data.ix["NET_PROFIT_IS"][start_col:]

        indicators.ix["总资产规模"] = self.treated_data.ix["TOT_ASSETS"][start_col:] / unit
        indicators.ix["净资产规模"] = self.treated_data.ix["TOT_EQUITY"][start_col:] / unit
        indicators.ix["净资产变化率"] = (np.array(self.treated_data.ix["TOT_EQUITY"][start_col:]) / np.array(self.treated_data.ix["TOT_EQUITY"][start_col-1: col_num-1])) - 1

        indicators.ix["营业收入"] = self.treated_data.ix["TOT_OPER_REV"][start_col:] / unit
        indicators.ix["净利润"] = self.treated_data.ix["NET_PROFIT_IS"][start_col:] / unit
        indicators.ix["营业利润"] = self.treated_data.ix["OPPROFIT"][start_col:] / unit

        indicators.ix["EBITDA"] = self.treated_data.ix[["FIN_EXP_IS", "TOT_PROFIT", "DEPR_FA_COGA_DPBA", "AMORT_INTANG_ASSETS",
                                                        "AMORT_LT_DEFERRED_EXP", "DECR_DEFERRED_EXP", "INCR_ACC_EXP", "LOSS_DISP_FIOLTA", "LOSS_FV_CHG"]
                                                      ].sum(axis=0)[start_col:] / unit

        indicators.ix["经营现金流净额"] = self.treated_data.ix["NET_CASH_FLOWS_OPER_ACT"][start_col:] / unit

        # 盈利指标
        indicators.ix["毛利率"] = (1 - (self.treated_data.ix["OPER_COST"] + self.treated_data.ix["TAXES_SURCHARGES_OPS"]) / self.treated_data.ix["OPER_REV"])[start_col:]
        indicators.ix["净利率"] = (self.treated_data.ix["NET_PROFIT_IS"] / self.treated_data.ix["OPER_REV"])[start_col:]

        indicators.ix["过去三年毛利率标准差"] = np.empty(col_num - 2)

        if start_col == 1:
            indicators.ix["过去三年毛利率标准差"] = np.std(self.treated_data.ix["OPER_REV"].iloc[0:2], ddof=1) / np.mean(self.treated_data.ix["OPER_REV"].iloc[0:2])
        else:
            indicators.ix["过去三年毛利率标准差"] = np.empty(col_num - 2)
            for i in range(0, col_num - 2):
                indicators.ix["过去三年毛利率标准差"].iloc[i] = np.std(self.treated_data.ix["OPER_REV"].iloc[i:i + 3], ddof=1) / np.mean(self.treated_data.ix["OPER_REV"].iloc[i:i + 3])

        indicators.ix["毛利率变化值"] = np.array(indicators.ix["毛利率"]) \
                                        - np.array(1 - (self.treated_data.ix["OPER_COST"] + self.treated_data.ix["TAXES_SURCHARGES_OPS"]) / self.treated_data.ix["OPER_REV"])[start_col - 1:col_num - 1]
        indicators.ix["ROE"] = self.treated_data.ix["ROE"][start_col:] / 100

        indicators.ix["(现金-短债)/净资产"] = (
                                                  ((self.treated_data.ix["MONETARY_CAP"] + self.treated_data.ix["TRADABLE_FIN_ASSETS"]
                                                    + self.treated_data.ix["NOTES_RCV"] + self.treated_data.ix["ACCT_RCV"]
                                                    + self.treated_data.ix["NON_CUR_ASSETS_DUE_WITHIN_1Y"])
                                                    - (self.treated_data.ix["ST_BORROW"] + self.treated_data.ix["BORROW_CENTRAL_BANK"]
                                                    + self.treated_data.ix["TRADABLE_FIN_LIAB"] + self.treated_data.ix["NOTES_PAYABLE"]
                                                    + self.treated_data.ix["ACCT_PAYABLE"] + self.treated_data.ix["HANDLING_CHARGES_COMM_PAYABLE"]
                                                    + self.treated_data.ix["EMPL_BEN_PAYABLE"] + self.treated_data.ix["TAXES_SURCHARGES_PAYABLE"]
                                                    + self.treated_data.ix["INT_PAYABLE"] + self.treated_data.ix["OTH_PAYABLE"]
                                                    + self.treated_data.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + self.treated_data.ix["ST_BONDS_PAYABLE"]
                                                    + self.treated_data.ix["OTH_CUR_LIAB"]
                                                  )) / self.treated_data.ix["TOT_EQUITY"])[start_col:]
        indicators.ix["现金/短期负债"] = ((self.treated_data.ix["MONETARY_CAP"] + self.treated_data.ix["TRADABLE_FIN_ASSETS"])
                                            / (self.treated_data.ix["ST_BORROW"] + self.treated_data.ix["BORROW_CENTRAL_BANK"]
                                               + self.treated_data.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + self.treated_data.ix["ST_BONDS_PAYABLE"]
                                               + self.treated_data.ix["OTH_CUR_LIAB"]
                                               ))[start_col:]
        indicators.ix["净负债率"] = ((self.treated_data.ix["ST_BORROW"] + self.treated_data.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"]
                                        + self.treated_data.ix["OTH_CUR_LIAB"] + self.treated_data.ix["ST_BONDS_PAYABLE"]
                                        + self.treated_data.ix["LT_BORROW"] + self.treated_data.ix["BONDS_PAYABLE"]
                                        + self.treated_data.ix["OTHER_EQUITY_INSTRUMENTS"]
                                        - self.treated_data.ix["MONETARY_CAP"] - self.treated_data.ix["TRADABLE_FIN_ASSETS"]
                                  ) / self.treated_data.ix["TOT_EQUITY"])[start_col:]

        indicators.ix["净负债率变化值"] = np.array(indicators.ix["净负债率"]) - np.array(((self.treated_data.ix["ST_BORROW"] + self.treated_data.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"]
                                  + self.treated_data.ix["OTH_CUR_LIAB"] + self.treated_data.ix["ST_BONDS_PAYABLE"]
                                  + self.treated_data.ix["LT_BORROW"] + self.treated_data.ix["BONDS_PAYABLE"]
                                        + self.treated_data.ix["OTHER_EQUITY_INSTRUMENTS"]
                                  - self.treated_data.ix["MONETARY_CAP"] - self.treated_data.ix["TRADABLE_FIN_ASSETS"]
                                  ) / self.treated_data.ix["TOT_EQUITY"])[start_col-1:-1])

        indicators.ix["资产负债率"] = self.treated_data.ix["TOT_LIAB"] / self.treated_data.ix["TOT_LIAB_SHRHLDR_EQY"][
                                                                    start_col:]
        indicators.ix["三费费率"] = (self.treated_data.ix["SELLING_DIST_EXP"] + self.treated_data.ix["GERL_ADMIN_EXP"] +
                                 self.treated_data.ix["FIN_EXP_IS"]) / self.treated_data.ix["OPER_REV"][start_col:]

        indicators.ix["固定资产/总资产"] = (self.treated_data.ix["LONG_TERM_EQY_INVEST"] + self.treated_data.ix["INVEST_REAL_ESTATE"]
                                     + self.treated_data.ix["FIX_ASSETS"] + self.treated_data.ix["CONST_IN_PROG"] + self.treated_data.ix["PROJ_MATL"]
                                     + self.treated_data.ix["FIX_ASSETS_DISP"] + self.treated_data.ix["PRODUCTIVE_BIO_ASSETS"]
                                     + self.treated_data.ix["OIL_AND_NATURAL_GAS_ASSETS"] + self.treated_data.ix["INTANG_ASSETS"]
                                     + self.treated_data.ix["OTH_NON_CUR_ASSETS"]) / self.treated_data.ix["TOT_ASSETS"][start_col:]

        indicators.ix["经营现金流/总债务"] = ( self.treated_data.ix["NET_CASH_FLOWS_OPER_ACT"] /
                                      (self.treated_data.ix["ST_BORROW"] + self.treated_data.ix["BORROW_CENTRAL_BANK"]
                                          + self.treated_data.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + self.treated_data.ix["ST_BONDS_PAYABLE"]
                                          + self.treated_data.ix["OTH_CUR_LIAB"] + self.treated_data.ix["LT_BORROW"]
                                          + self.treated_data.ix["BONDS_PAYABLE"] + self.treated_data.ix["LT_PAYABLE"]
                                          + self.treated_data.ix["SPECIFIC_ITEM_PAYABLE"]
                                          + self.treated_data.ix["OTHER_EQUITY_INSTRUMENTS"]
                                          + self.treated_data.ix["TRADABLE_FIN_LIAB"] + self.treated_data.ix["NOTES_PAYABLE"]
                                          + self.treated_data.ix["ACCT_PAYABLE"] + self.treated_data.ix["HANDLING_CHARGES_COMM_PAYABLE"]
                                          + self.treated_data.ix["EMPL_BEN_PAYABLE"] + self.treated_data.ix["TAXES_SURCHARGES_PAYABLE"]
                                          + self.treated_data.ix["INT_PAYABLE"] + self.treated_data.ix["OTH_PAYABLE"]))[start_col:]

        if start_col == 1:
            indicators.ix["三年经营现金流波动"] = np.std(self.treated_data.ix["NET_CASH_FLOWS_OPER_ACT"].iloc[0: 2], ddof=1) \
                                         / np.mean(self.treated_data.ix["NET_CASH_FLOWS_OPER_ACT"].iloc[0:2])
        else:
            indicators.ix["三年经营现金流波动"] = np.empty(col_num - 2)
            for i in range(0, col_num - 2):
                indicators.ix["三年经营现金流波动"].iloc[i] = np.std( self.treated_data.ix["NET_CASH_FLOWS_OPER_ACT"].iloc[i: i + 3], ddof=1) \
                                                     / np.mean(self.treated_data.ix["NET_CASH_FLOWS_OPER_ACT"].iloc[i:i + 3])

        indicators.ix["EBITDA/总债务(有息负债)"] = (indicators.ix["EBITDA"] /
                                       ((self.treated_data.ix["ST_BORROW"] + self.treated_data.ix["BORROW_CENTRAL_BANK"]
                                         + self.treated_data.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + self.treated_data.ix["ST_BONDS_PAYABLE"]
                                         + self.treated_data.ix["OTH_CUR_LIAB"]
                                         + self.treated_data.ix["OTHER_EQUITY_INSTRUMENTS"]
                                         + self.treated_data.ix["LT_BORROW"] + self.treated_data.ix["BONDS_PAYABLE"]
                                         + self.treated_data.ix["LT_PAYABLE"] + self.treated_data.ix["SPECIFIC_ITEM_PAYABLE"]) / unit))[start_col:]

        indicators.ix["固定资产周转率"] = self.treated_data.ix["FATURN"][start_col:]
        indicators.ix["存货周转天数"] = self.treated_data.ix["INVTURNDAYS"][start_col:]
        indicators.ix["应收账款周转天数"] = 360 / (self.treated_data.ix["OPER_REV"][start_col:] /
                                           ((np.array(self.treated_data.ix["ACCT_RCV"][start_col-1:col_num-1] + self.treated_data.ix["OTH_RCV"][start_col-1:col_num-1]
                                                      + self.treated_data.ix["LONG_TERM_REC"][start_col-1:col_num-1])
                                             + np.array(self.treated_data.ix["ACCT_RCV"][start_col:] + self.treated_data.ix["OTH_RCV"][start_col:]
                                                        + self.treated_data.ix["LONG_TERM_REC"][start_col:])) / 2))

        indicators.ix["未使用授信/总债务"] = self.treated_data.ix["CREDIT_UNUSED"] / \
                                     ((self.treated_data.ix["ST_BORROW"] + self.treated_data.ix["BORROW_CENTRAL_BANK"]
                                           + self.treated_data.ix["NON_CUR_LIAB_DUE_WITHIN_1Y"] + self.treated_data.ix["ST_BONDS_PAYABLE"]
                                           + self.treated_data.ix["OTH_CUR_LIAB"] + self.treated_data.ix["LT_BORROW"]
                                           + self.treated_data.ix["BONDS_PAYABLE"] + self.treated_data.ix["LT_PAYABLE"]
                                           + self.treated_data.ix["SPECIFIC_ITEM_PAYABLE"]
                                           + self.treated_data.ix["OTHER_EQUITY_INSTRUMENTS"]
                                           + self.treated_data.ix["TRADABLE_FIN_LIAB"] + self.treated_data.ix["NOTES_PAYABLE"]
                                           + self.treated_data.ix["ACCT_PAYABLE"] + self.treated_data.ix["HANDLING_CHARGES_COMM_PAYABLE"]
                                           + self.treated_data.ix["EMPL_BEN_PAYABLE"] + self.treated_data.ix["TAXES_SURCHARGES_PAYABLE"]
                                           + self.treated_data.ix["INT_PAYABLE"] + self.treated_data.ix["OTH_PAYABLE"]) / unit)[start_col:]

        self.indicators = indicators

    # convert indicators to standard score
    def indicators2score(self):
        GeneralBond.indicators2score(self)   # use general method from base class

        # special indicators
        self.score.ix["三年经营现金流波动", self.indicators.ix["三年经营现金流波动"] < 0] = -1.5
        self.score.ix["母公司利润占比", self.indicators.ix["净利润"] < 0] = -1.5

        # 将外部手工因子dict类型合并到计算好的因子中
        for name in self.OtherScore.keys():
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
