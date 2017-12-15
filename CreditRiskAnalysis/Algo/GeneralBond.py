# this is the general bond class, define some common methods when do credit rating
from ..SQLDB.get_data import *
from ..Common.GlobalConfig import *

class GeneralBond:
    # Parameter initialization
    def __init__(self, bond_code):
        self.bond_code = bond_code
        self.config = GlobalConfig()
        self.wd = GetWindData(self.bond_code, Conn_DB())   # wind查询初始化

    # get raw data from database
    def get_raw_data(self):
        # TODO:进一步扩展，支持非财务数据的简单查询
        # get raw data template from excel (Only Financial Data)
        data_fields = self.config.getConfig('Excel', self.raw_data_template)
        data_fields = pd.read_excel(data_fields)

        # group by table name, {tablename:{"FactorName": [XXX], "OutputName": [XXX], "DBFieldName": [XXX]}}
        data_fields.index = list(data_fields['DBTableName'])
        data_dict = {}
        for table in set(data_fields.index):
            data_dict[table] = {
                "FactorName": list(data_fields.loc[[table]]['FactorName'].values),
                "OutputName": list(data_fields.loc[[table]]['OutputName'].values),
                "DBFieldName": list(data_fields.loc[[table]]['DBFieldName'].values)
            }

        # get raw data from data bases
        raw_data = pd.DataFrame()
        for table_name in data_dict.keys():
            sub_data = self.wd.QueryFinancialData(table_name, data_dict[table_name]["DBFieldName"],
                                             data_dict[table_name]["OutputName"], self.year_len)
            raw_data = pd.concat([raw_data, sub_data], axis=0)

        self.raw_data = raw_data

    # pretreat raw data: standardization,etc
    def pretreat_data(self):
        self.treated_data = pd.DataFrame()
        pass

    # calculate indicators
    def calc_indicators(self):
        self.indicators = pd.DataFrame()
        pass

    # convert indicators to standard score
    def indicators2score(self):
        # read indicators_to_score criterion from excel
        scoring_criterion = self.config.getConfig('Excel', self.indicator2score_criterion)
        scoring_criterion = pd.read_excel(scoring_criterion)

        score_range = np.array(scoring_criterion.columns)

        index = self.indicators.index
        columns = self.indicators.columns
        score = pd.DataFrame(columns=columns, index=index)

        # convert indicators to score
        for i in range(0, index.size):
            for j in range(0, columns.size):
                if scoring_criterion.ix[index[i]].iloc[0] > scoring_criterion.ix[index[i]].iloc[1]: # higher is better
                    ref_index = self.indicators.ix[index[i], columns[j]] >= scoring_criterion.ix[index[i]]
                    score.ix[index[i], columns[j]] = score_range[ref_index][0] if sum(ref_index) > 0 else score_range[-1]
                else:                                                                               # lower is better
                    ref_index = self.indicators.ix[index[i], columns[j]] <= scoring_criterion.ix[index[i]]
                    score.ix[index[i], columns[j]] = score_range[ref_index][0] if sum(ref_index) > 0 else score_range[-1]

        self.score = score

    # calculate weighted score and do rating
    def weight_score_and_rating(self):
        self.rate = pd.DataFrame()
        pass

    # convert total score to rating
    def score2rating(self, score):
        # read score_2_rating template, two columns: socre_threshold, rating
        criterion = self.config.getConfig('Excel', self.score2rating_criterion)
        criterion = pd.read_excel(criterion)

        rate = np.empty(score.shape).astype('str')

        for i in range(0, score.size):
            rate[i] = criterion['rating'][score.iloc[i] > criterion['score']].iloc[0]

        return rate

    # external rating
    def external_rating(self):
        self.rate_outside = self.wd.QueryOutsideRating()
