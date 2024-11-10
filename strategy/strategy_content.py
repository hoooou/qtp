# -*- coding: utf-8 -*-
"""
策略内容函数
"""
from pybroker import ExecContext

# 金叉死叉均线策略
def ma_strategy(ctx:ExecContext):
    pos = ctx.long_pos()
    # 确保两条均线都有数据
    if ctx.sma_short[-1] is None or ctx.sma_long[-1] is None:
        return
    if len(ctx.sma_short) < 2 or len(ctx.sma_long) < 2:
        return
    # 检查金叉条件
    if ctx.sma_short[-1] > ctx.sma_long[-1] and ctx.sma_short[-2] <= ctx.sma_long[-2] and ctx.close[-1]>ctx.sma250[-1]:
        # 当50日均线上穿200日均线，执行买入操作
        if not pos:
            ctx.stop_loss_pct=5
            ctx.stop_loss_exit_price=PriceType.CLOSE
            # 追踪止损/追踪止损价位
            ctx.stop_trailing_pct = 10
            ctx.stop_trailing_exit_price = PriceType.CLOSE
            # 止盈
            ctx.stop_profit_pct=20
            ctx.stop_profit_exit_price=PriceType.CLOSE
            ctx.buy_shares = ctx.calc_target_shares(1)
    # 检查死叉条件
    elif ctx.sma_short[-1] < ctx.sma_long[-1] and ctx.sma_short[-2] >= ctx.sma_long[-2]:
        # 当50日均线下穿30日均线，执行卖出操作
        if pos:
            print(f"{ctx.dt}清仓")
            ctx.sell_all_shares()
            ctx.stop_loss_pct=None
            ctx.stop_loss_exit_price=None
            # 追踪止损/追踪止损价位
            ctx.stop_trailing_pct = None
            ctx.stop_trailing_exit_price = None
            # 止盈
            ctx.stop_profit_pct=None
            ctx.stop_profit_exit_price=None


def macd_strategy(ctx:ExecContext):
      #取得当前持仓状态
    pos = ctx.long_pos()
    percent = float(pb.param(name='percent'))
    #如果未持仓
    if ctx.close[-1]<ctx.SMA250[-1]:
        return;
    if not pos: 
        if ctx.macd[-1] > 0 and ctx.macdsignal[-1] > 0:
            # 将买单的限价设置为比最后收盘价低 0.01 的价格。
            #ctx.buy_limit_price = ctx.close[-1] - 0.01
            # ctx.buy_limit_price = ctx.close[-1]
            # 买入1000股
            # ctx.buy_shares = 1000
            #持有仓位10天
            # ctx.hold_bars = 10
            # ctx.stop_profit_pct=30
            # 止损
            ctx.stop_loss_pct=5
            ctx.stop_loss_exit_price=PriceType.CLOSE
            ctx.buy_shares = ctx.calc_target_shares(percent)
            # 追踪止损/追踪止损价位
            ctx.stop_trailing_pct = 10
            ctx.stop_trailing_exit_price = PriceType.CLOSE
            # 止盈
            ctx.stop_profit_pct=10
            # ctx.stop_profit_exit_price=PriceType.CLOSE

            # print(f"{ctx.dt}:未持仓,买入")
    #如果持仓
    # else:
        # print(f"{ctx.dt}:持仓中")
        # if ctx.macd[-1] < 0 and ctx.macdsignal[-1] < 0:
        #     #卖出全部股票
        #     ctx.sell_all_shares()
        #     print(f"{ctx.dt}:持仓,卖出所有")
        #     #卖出100股
        #     #ctx.buy_shares = ctx.calc_target_shares(percent)
        #     #ctx.sell_shares = 1000
        #     # 设置止盈点位，根据 "stop_profit_pct" 参数确定止盈点位
        #     # ctx.stop_profit_pct = pb.param(name='stop_profit_pct')
        # else:
        #     print(f"{ctx.dt}:指标不符合,有仓位,等待中")
import pybroker as pb
from pybroker import ExecContext
from pybroker import PriceType
def buy_with_indicator(ctx:ExecContext):
    ma_strategy(ctx)
    # macd_strategy(ctx)