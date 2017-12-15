import cx_Oracle
import pandas as pd
import numpy as np
import datetime as dt
from ..Common.GlobalConfig import *

#############################################################################
# 数据库连接、查询语句
#############################################################################
class Conn_DB:
    def __init__(self):
        config = GlobalConfig()
        DSN = config.getConfig('DataBase', 'DSN')
        User = config.getConfig('DataBase', 'User')
        PWD = config.getConfig('DataBase', 'Pwd')
        IP = config.getConfig('DataBase', 'IP')
        Port = config.getConfig('DataBase', 'Port')
        self.conn_str = User + "/" + PWD + "@" + IP + ":" + Port + "/" + DSN

    def __GetConnect(self):
        self.conn = cx_Oracle.connect(self.conn_str)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        try:
            cur.execute(sql)
            resList = cur.fetchall()
        except Exception as e:
            raise
        finally:
            cur.close()
            self.conn.close()

        return resList


#################################################################################
# 父类：基础查询
#################################################################################
class BaseQuery:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    ## Fun1：通用查询
    def GeneralSelectData(self, table_name, field_name=None, equal_constrain=None, in_constrain=None, order_by=None):
        # 生成SQL语句
        sql = "select "
        if field_name is None:
            sql += "* from "
        else:
            if isinstance(field_name, str):              # 只有一个字段
                field_name = [field_name]

            for f in field_name:
                sql += (f + ", ")
            sql = sql[0:len(sql) - 2] + " "

        sql += (" from " + table_name)

        # 等式限制
        if equal_constrain is None:
            pass
        else:
            sql += " where "
            if isinstance(equal_constrain, tuple):                     # 只有一个等式条件
                equal_constrain = [equal_constrain]                 # 转换为列表
            for cons in equal_constrain:
                if isinstance(cons[1], int):
                    sql += (cons[0] + "=" + cons[1] + " and ")
                else:
                    sql += (cons[0] + "='" + cons[1] + "' and ")
            sql = sql[0:-4]

        # in限制
        if in_constrain is None:
            pass
        else:
            if equal_constrain is None:
                sql += " where "
            else:
                sql += " and "
            if isinstance(in_constrain, tuple):
                in_constrain = [in_constrain]

            for cons in in_constrain:
                sql += (cons[0] + " in " + str(cons[1]) + " and ")

            sql = sql[0:-4]

        # 排序字段 order_by
        if order_by is not None:
            sql += " order by "
            if isinstance(order_by, str):
                order_by = [order_by]
            for o in order_by:
                sql += (o + ",")
            sql = sql[0:-1]

        data = self.db_conn.ExecQuery(sql)
        return data

    # Fun2：SQL查询结果转变为DataFrame
    def ConvertToDataFrame(self, sql_result, index_name=None, col_name=None):
        result = pd.DataFrame(np.array(sql_result)).T
        if index_name is not None:
            result.index = index_name
        if col_name is not None:
            result.columns = col_name

        return result.astype('float64')


#################################################################################
# 子类：Wind数据读取
#################################################################################
# wind数据库中具体的查询函数
class GetWindData(BaseQuery):
    def __init__(self, info_code, db_conn):
        self.code = info_code
        self.db_conn = db_conn
        self.bond_name = self.GetBondName()
        self.company_name = self.GetCompanyName()
        self.CompanyID = self.GetCompanyID()
        self.latestrep = self.GetLatestRepYear()

    # Fun1 查询数据库中公司id，作为查询财务数据等的主键
    def GetCompanyID(self):
        result = self.GeneralSelectData(table_name="wind.TB_OBJECT_0001", field_name="F17_0001", equal_constrain=("F1_0001", self.code))

        return result[0][0]

    # Fun1 查询数据库中债券名称、公司名称
    def GetBondName(self):
        result = self.GeneralSelectData(table_name="wind.TB_OBJECT_0001", field_name="F6_0001", equal_constrain=("F1_0001", self.code))
        return result[0][0]

    def GetCompanyName(self):
        result = self.GeneralSelectData(table_name="wind.CBondIssuer", field_name="s_info_compname", equal_constrain=("s_info_windcode", self.code))

        return result[0][0]

    # Fun2 查询数据库中最新的年报期间，用于确定取数区间
    def GetLatestRepYear(self):
        latest_rep = self.GeneralSelectData(table_name="wind.TB_OBJECT_1853", field_name="max(F2_1853)", equal_constrain=("F1_1853", self.CompanyID))

        latest_rep = dt.datetime.strptime(latest_rep[0][0], "%Y%m%d")

        if latest_rep.month < 12:
            latest_year = dt.datetime(latest_rep.year - 1, 12, 31)
        else:
            latest_year = latest_rep

        return latest_year

    # Fun3 查询财务报表/衍生财务指标
    # 可以查询TB_OBJECT_1853/1854/1855/5034
    def QueryFinancialData(self, table_name, field_name, output_name, year_len):
        if isinstance(field_name, str):              # 只查询1个字段
            field_name = [field_name]
        if isinstance(output_name, str):
            output_name = [output_name]

        # 1 生成tablename,提取table_id
        table_name = "wind." + table_name
        table_id = table_name[-4:]

        # 2 生成等式限制条件
        equal_constrain =[("F1_" + table_id, self.CompanyID),           # 公司代码
                         ("F4_" + table_id, "合并报表")]               # 报表类型

        # 4 生成in限制条件（报表期间）
        # 衍生财务指标的报告期为F3，其他为F2
        in_constrain = None
        if table_id in ("1853", "1854", "1855", "5034"):
            rep_field = 'F3_5034' if table_id == "5034" else 'F2_' + table_id
        else:
            return None                # 此函数不支持对该表进行查询

        # 根据year_len确定取哪几年的报表数据
        date_range = [dt.datetime(self.latestrep.year - x, 12, 31).strftime("%Y%m%d") for x in range(year_len - 1, -1, -1)]
        if len(date_range) == 1:           # 只有一年数据
            equal_constrain.append((rep_field, date_range[0]))
        else:
            date_range = tuple(date_range)
            in_constrain = (rep_field, date_range)

        # 从数据库中获取数据,并转变为DataFrame
        data = self.GeneralSelectData(table_name=table_name, field_name=field_name, equal_constrain=equal_constrain,
                                      in_constrain=in_constrain, order_by=rep_field)

        data = self.ConvertToDataFrame(data, index_name=output_name, col_name=[x[0:4] for x in date_range])

        return data

    # Fun4 查询持股比例数据
    def QueryShareHolderData(self, year_len):
        # 根据year_len确定取那几年的报表数据
        date_range = [dt.datetime(self.latestrep.year - x, 12, 31).strftime("%Y%m%d") for x in range(year_len - 1, -1, -1)]
        if len(date_range) == 1:
            date_str = "('" + date_range[0] + "')"
        else:
            date_str = str(tuple(date_range))

        # 生成查询字符串
        sql = "select distinct F8_1017, max(F5_1017) over(partition by F8_1017) temp from wind.TB_OBJECT_1017 " \
              "where F9_1017 = '" + self.CompanyID + "' and F8_1017 in " + date_str

        sql = "select F8_1017, temp from (" + sql +") order by F8_1017"

        # 从数据库中获取数据
        data = self.db_conn.ExecQuery(sql)
        if len(data) == 0:           # 查询的年度内没有披露持仓比例数据，向前查询得到最新的持股比例数据
            sql = "select temp from (" \
                    "select distinct F8_1017, max(F5_1017) over(partition by F8_1017) temp from wind.TB_OBJECT_1017 " \
                    "where F9_1017 = '" + self.CompanyID +"' " \
                    " order by F8_1017) where rownum = 1"
            data = self.db_conn.ExecQuery(sql)
            latest_hold_pct = data[0] if len(data) > 0 else np.nan
            data = [latest_hold_pct] * len(date_range)
        else:           # 查询到了持股比例数据，但可能有缺失
            data = dict(data)
            data = [data[x] if x in data.keys() else np.nan for x in date_range]

        data = self.ConvertToDataFrame(data, index_name=['HOLDER_PCT'], col_name=[x[0:4] for x in date_range]).fillna(method = "pad", axis = 1)

        return data

    # Fun5 查询最新的未使用授信额度
    def QueryUnusedCredit(self):
        sql = "select * from (" \
              "select CREDIT_UNUSED from wind.CompanyLineOfCredit where COMP_ID='" + self.CompanyID + "' "\
              "and CREDIT_COMPNAME = '合计' order by END_DT desc) where ROWNUM = 1"
        # 从数据库中获取数据
        data = self.db_conn.ExecQuery(sql)

        if len(data) == 0:
            return 0
        else:
            return np.float(data[0][0])


    # Fun5 查询最新外部评级
    def QueryOutsideRating(self):
        rate_outside = pd.DataFrame(columns=["外部最新评级"], index=["债项", "主体"])

        # 1. 债项评级
        sql = "select * from ( " \
              "select B_INFO_CREDITRATING from wind.CBondRating " \
              "where S_INFO_WINDCODE='" + self.code + "' " \
              "order by ANN_DT desc) where rownum = 1"

        data1 = self.db_conn.ExecQuery(sql)

        if len(data1) > 0:
            rate_outside.loc["债项", "外部最新评级"] = data1[0][0]

        # 2. 主体评级
        sql = "select * from( " \
              "select B_INFO_CREDITRATING from wind.CBONDISSUERRATING " \
              "where S_INFO_COMPCODE = '" + self.CompanyID +"' " \
              + "order by ANN_DT DESC) where rownum = 1"

        data2 = self.db_conn.ExecQuery(sql)

        if len(data2) > 0:
            rate_outside.loc["主体", "外部最新评级"] = data2[0][0]

        return rate_outside


if __name__ == "__main__":
    db_conn = Conn_DB()
    wd = GetWindData("136164.SH", db_conn)

    table_name = "TB_OBJECT_1854"
    field_name = ["F60_1854", "F61_1854"]
    output_name = ["net_profit_is", "np_belongto_parcomsh"]
    year_len = 3
    financial_data = wd.QueryFinancialData(table_name, field_name, output_name, year_len)
    hold_data = wd.QueryShareHolderData(year_len)
