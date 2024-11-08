# -*- coding: utf-8 -*-
"""
策略内容函数
"""

import pybroker as pb
from pybroker import ExecContext
        
def buy_with_indicator(ctx:ExecContext):
    #取得当前持仓状态
    pos = ctx.long_pos()
    percent = float(pb.param(name='percent'))
    #如果未持仓
    if not pos: 
        if ctx.macd[-1] > 0 and ctx.macdsignal[-1] > 0:
            # 将买单的限价设置为比最后收盘价低 0.01 的价格。
            #ctx.buy_limit_price = ctx.close[-1] - 0.01
            # ctx.buy_limit_price = ctx.close[-1]
            # 买入1000股
            # ctx.buy_shares = 1000
            #持有仓位10天
            # ctx.hold_bars = 10
            ctx.stop_profit_pct=20
            ctx.stop_loss_pct=10
            ctx.buy_shares = ctx.calc_target_shares(percent)
            print(f"{ctx.dt}:未持仓,买入")
    #如果持仓
    else:
        if ctx.macd[-1] < 0 and ctx.macdsignal[-1] < 0:
            #卖出全部股票
            ctx.sell_all_shares()
            print(f"{ctx.dt}:持仓,卖出所有")
            #卖出100股
            #ctx.buy_shares = ctx.calc_target_shares(percent)
            #ctx.sell_shares = 1000
            # 设置止盈点位，根据 "stop_profit_pct" 参数确定止盈点位
            # ctx.stop_profit_pct = pb.param(name='stop_profit_pct')
        else:
            print(f"{ctx.dt}:指标不符合,有仓位,等待中")
