r"""获取基金数据
"""

from datetime import datetime
from typing import Optional
import akshare
import pandas as pd
from pybroker.common import DataCol, to_datetime
from pybroker.data import DataSource
from pybroker.ext.data import AKShare
from typing import Any, Final, Iterable, Optional, Union
import akshare as ak
def is_index(symbol):
    
    # 获取所有 ETF 的列表
    import akshare as ak
    index_list = ak.index_stock_info()
    symbols = index_list["index_code"].tolist()
    # 判断 symbol 是否在 ETF 列表中
    if symbol in symbols:
        return True
    else:
        return False

def is_etf(symbol):
    # 获取所有 ETF 的列表
    import akshare as ak

    etf_list = ak.fund_etf_spot_ths()
    # etf_list=etf_list.sort_values(by="总市值",ascending=True).reset_index(drop=True)
    etf_list["申购状态"] = etf_list["申购状态"].fillna("")
    # 2. 使用更严格的判断条件，包括去除空格及其他不可见字符
    etf_list = etf_list[
        (etf_list["基金类型"].str.contains("股票"))
        & (etf_list["申购状态"].str.strip() != "")
    ]
    etf_symbols = etf_list["基金代码"].tolist()
    # 判断 symbol 是否在 ETF 列表中
    if symbol in etf_symbols:
        return True
    else:
        return False


class AKShare_ALL(DataSource):
    r"""Retrieves data from `AKShare <https://akshare.akfamily.xyz/>`_."""

    _tf_to_period = {
        "": "daily",
        "1day": "daily",
        "1week": "weekly",
        "1month": "monthly",
    }

    def _fetch_data(
        self,
        symbols: frozenset[str],
        start_date: datetime,
        end_date: datetime,
        timeframe: Optional[str],
        adjust: Optional[str],
    ) -> pd.DataFrame:
        """:meta private:"""
        start_date_str = to_datetime(start_date).strftime("%Y%m%d")
        end_date_str = to_datetime(end_date).strftime("%Y%m%d")
        symbols_list = list(symbols)
        symbols_simple = [item.split(".")[0] for item in symbols_list]
        result = pd.DataFrame()
        formatted_tf = self._format_timeframe(timeframe)
        if formatted_tf in self._tf_to_period:
            period = self._tf_to_period[formatted_tf]
            for i in range(len(symbols_list)):
                if is_etf(symbols_simple[i]):
                    temp_df = akshare.fund_etf_hist_em(
                        symbol=symbols_simple[i],
                        start_date=start_date_str,
                        end_date=end_date_str,
                        period=period,
                        adjust=adjust if adjust is not None else "",
                    )
                elif(is_index(symbols_simple[i])):
                    temp_df = akshare.index_zh_a_hist(
                        symbol=symbols_simple[i],
                        start_date=start_date_str,
                        end_date=end_date_str,
                        period=period,
                    )
                else:
                    temp_df = akshare.stock_zh_a_hist(
                        symbol=symbols_simple[i],
                        start_date=start_date_str,
                        end_date=end_date_str,
                        period=period,
                        adjust=adjust if adjust is not None else "",
                    )
                if not temp_df.columns.empty:
                    temp_df["symbol"] = symbols_list[i]
                result = pd.concat([result, temp_df], ignore_index=True)
        if result.columns.empty:
            return pd.DataFrame(
                columns=[
                    DataCol.SYMBOL.value,
                    DataCol.DATE.value,
                    DataCol.OPEN.value,
                    DataCol.HIGH.value,
                    DataCol.LOW.value,
                    DataCol.CLOSE.value,
                    DataCol.VOLUME.value,
                ]
            )
        if result.empty:
            return result
        result.rename(
            columns={
                "日期": DataCol.DATE.value,
                "开盘": DataCol.OPEN.value,
                "收盘": DataCol.CLOSE.value,
                "最高": DataCol.HIGH.value,
                "最低": DataCol.LOW.value,
                "成交量": DataCol.VOLUME.value,
            },
            inplace=True,
        )
        result["date"] = pd.to_datetime(result["date"])
        result = result[
            [
                DataCol.DATE.value,
                DataCol.SYMBOL.value,
                DataCol.OPEN.value,
                DataCol.HIGH.value,
                DataCol.LOW.value,
                DataCol.CLOSE.value,
                DataCol.VOLUME.value,
            ]
        ]
        return result


class AKShare_ETF(DataSource):
    r"""Retrieves data from `AKShare <https://akshare.akfamily.xyz/>`_."""

    _tf_to_period = {
        "": "daily",
        "1day": "daily",
        "1week": "weekly",
        "1month": "monthly",
    }

    def _fetch_data(
        self,
        symbols: frozenset[str],
        start_date: datetime,
        end_date: datetime,
        timeframe: Optional[str],
        adjust: Optional[str],
    ) -> pd.DataFrame:
        """:meta private:"""
        start_date_str = to_datetime(start_date).strftime("%Y%m%d")
        end_date_str = to_datetime(end_date).strftime("%Y%m%d")
        symbols_list = list(symbols)
        symbols_simple = [item.split(".")[0] for item in symbols_list]
        result = pd.DataFrame()
        formatted_tf = self._format_timeframe(timeframe)
        if formatted_tf in self._tf_to_period:
            period = self._tf_to_period[formatted_tf]
            for i in range(len(symbols_list)):
                temp_df = akshare.fund_etf_hist_em(
                    symbol=symbols_simple[i],
                    start_date=start_date_str,
                    end_date=end_date_str,
                    period=period,
                    adjust=adjust if adjust is not None else "",
                )
                if not temp_df.columns.empty:
                    temp_df["symbol"] = symbols_list[i]
                result = pd.concat([result, temp_df], ignore_index=True)
        if result.columns.empty:
            return pd.DataFrame(
                columns=[
                    DataCol.SYMBOL.value,
                    DataCol.DATE.value,
                    DataCol.OPEN.value,
                    DataCol.HIGH.value,
                    DataCol.LOW.value,
                    DataCol.CLOSE.value,
                    DataCol.VOLUME.value,
                ]
            )
        if result.empty:
            return result
        result.rename(
            columns={
                "日期": DataCol.DATE.value,
                "开盘": DataCol.OPEN.value,
                "收盘": DataCol.CLOSE.value,
                "最高": DataCol.HIGH.value,
                "最低": DataCol.LOW.value,
                "成交量": DataCol.VOLUME.value,
            },
            inplace=True,
        )
        result["date"] = pd.to_datetime(result["date"])
        result = result[
            [
                DataCol.DATE.value,
                DataCol.SYMBOL.value,
                DataCol.OPEN.value,
                DataCol.HIGH.value,
                DataCol.LOW.value,
                DataCol.CLOSE.value,
                DataCol.VOLUME.value,
            ]
        ]
        return result


# 指数历史行情
class AKShare_ZHISHU(DataSource):
    r"""Retrieves data from `AKShare <https://akshare.akfamily.xyz/>`_."""

    _tf_to_period = {
        "": "daily",
        "1day": "daily",
        "1week": "weekly",
        "1month": "monthly",
    }

    def _fetch_data(
        self,
        symbols: frozenset[str],
        start_date: datetime,
        end_date: datetime,
        timeframe: Optional[str],
        adjust: Optional[str],
    ) -> pd.DataFrame:
        """:meta private:"""
        start_date_str = to_datetime(start_date).strftime("%Y%m%d")
        end_date_str = to_datetime(end_date).strftime("%Y%m%d")
        symbols_list = list(symbols)
        symbols_simple = [item.split(".")[0] for item in symbols_list]
        result = pd.DataFrame()
        formatted_tf = self._format_timeframe(timeframe)
        if formatted_tf in self._tf_to_period:
            period = self._tf_to_period[formatted_tf]
            for i in range(len(symbols_list)):
                temp_df = akshare.index_zh_a_hist(
                    symbol=symbols_simple[i],
                    start_date=start_date_str,
                    end_date=end_date_str,
                    period=period,
                )
                if not temp_df.columns.empty:
                    temp_df["symbol"] = symbols_list[i]
                result = pd.concat([result, temp_df], ignore_index=True)
        if result.columns.empty:
            return pd.DataFrame(
                columns=[
                    DataCol.SYMBOL.value,
                    DataCol.DATE.value,
                    DataCol.OPEN.value,
                    DataCol.HIGH.value,
                    DataCol.LOW.value,
                    DataCol.CLOSE.value,
                    DataCol.VOLUME.value,
                ]
            )
        if result.empty:
            return result
        result.rename(
            columns={
                "日期": DataCol.DATE.value,
                "开盘": DataCol.OPEN.value,
                "收盘": DataCol.CLOSE.value,
                "最高": DataCol.HIGH.value,
                "最低": DataCol.LOW.value,
                "成交量": DataCol.VOLUME.value,
            },
            inplace=True,
        )
        result["date"] = pd.to_datetime(result["date"])
        result = result[
            [
                DataCol.DATE.value,
                DataCol.SYMBOL.value,
                DataCol.OPEN.value,
                DataCol.HIGH.value,
                DataCol.LOW.value,
                DataCol.CLOSE.value,
                DataCol.VOLUME.value,
            ]
        ]
        return result
