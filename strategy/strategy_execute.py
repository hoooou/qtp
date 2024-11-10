"""
用于设置策略参数并执行策略
"""

import pandas as pd
import pybroker as pb
from pybroker import Strategy
from pybroker.ext.data import AKShare
from data.data_resouce import AKShare_Found, AKShare_ZHISHU
from strategy.strategy_content import buy_with_indicator
from strategy.strategy_chart import create_strategy_charts
from indicator.indicator_talib import calculate_indicator
import akshare as ak
def create_strategy():
    
    # 定义全局参数 "stock_code"（股票代码）
    pb.param(name='stock_code', value='001616') 
    # 定义全局参数 "start_date" 开始日期
    pb.param(name='start_date', value='20180801') 
    # 定义全局参数 "end_date" 结束日期
    pb.param(name='end_date', value='20241101') 
    
    # 定义全局参数 "percent"（持仓百分比） 1代表100% 0.25代表25%
    pb.param(name='percent', value=1)
    # 定义全局参数 "stop_loss_pct"（止损百分比）
    pb.param(name='stop_loss_pct', value=10)
    # 定义全局参数 "stop_profit_pct"（止盈百分比）
    pb.param(name='stop_profit_pct', value=10)
    
    # 创建策略配置，初始资金为 500000
    my_config = pb.StrategyConfig(initial_cash=500000,fee_amount=0.0013,fee_mode = pb.common.FeeMode.ORDER_PERCENT)
    #使用AKShare获取股票OHLCV数据
    akshare = AKShare_Found()
    
    df = akshare.query(symbols=[pb.param(name='stock_code')], start_date=pb.param(name='start_date'), end_date=pb.param(name='end_date'),adjust="hfq")
    # df=ak.stock_zh_a_hist(symbol="600519", period="daily",start_date=pb.param(name='start_date'), end_date=pb.param(name='end_date'),adjust="hfq")
    print("打印股票数据")
    print(df)
    
    #使用at-lib计算并获取指标
    
    #计算MACD参数
    data_with_indicator = calculate_indicator(df)
    print("打印技术指标")
    print(data_with_indicator)
    #macd_data = calculate_macd(df)
    #存入数据库
    #save_data_macd(macd_data)
    
    # 使用配置、数据源、起始日期、结束日期，以及刚才定义的交易策略创建策略对象
    #strategy = Strategy(akshare, start_date='20230101', end_date='20230201', config=my_config)
    # 添加执行策略，设置股票代码和要执行的函数

    #在pybroker中注册指标名称
    '''MACD指标'''
    pb.register_columns('macd')
    pb.register_columns('macdsignal')
    pb.register_columns('sma_short')
    pb.register_columns('sma_long')
    
    '''MFI指标'''
    pb.register_columns('MFI')
    
    #创建策略
    strategy = Strategy(data_with_indicator, start_date=pb.param(name='start_date'), end_date=pb.param(name='end_date'), config=my_config)
    #配置策略执行参数
    strategy.add_execution(buy_with_indicator, symbols=[pb.param(name='stock_code')])
    
    # 执行回测，并打印出回测结果的度量值（四舍五入到小数点后四位）
    result = strategy.backtest()
    print('======基准收益率==========================')
    first_open = df['open'].iloc[0]
    last_open = df['open'].iloc[-1]
    benchmark_return = (last_open - first_open) / first_open * 100
    print(f"基准收益率{benchmark_return}")
    print('======查看绩效==========================')
    print(result.metrics_df.round(2))
    print('======查看订单==========================')
    print(result.orders)
    print('======查看持仓==========================')
    print(result.positions)
    print('======查看投资组合==========================')
    print(result.portfolio)
    print('======查看交易==========================')
    print(result.trades)

    create_strategy_charts(data_with_indicator,result)
    return result