import pybroker as pb
import pandas as pd

from indicator_talib import calculate_indicator
from pybroker import Strategy
from sqlalchemy import create_engine, text
from strategy_content import buy_with_indicator

def execute_backtest(engine):
    print("开始回测")
    conn = engine.connect()
    sql = "SELECT * FROM basic_data_stock_code"
    df = pd.read_sql(text(sql), conn)
    
    my_config = pb.StrategyConfig(initial_cash=500000)
    
    # 处理查询结果
    for index,row in df.iterrows():
        try:
            symbolCode = row['Symbol']
            stockName = row['StockName']
            
            sql = "SELECT * FROM basic_data_stock_history WHERE symbol='" + symbolCode + "' order by date"
            df = pd.read_sql(text(sql), conn)
            
            data_with_indicator = calculate_indicator(df)
            data_with_indicator['date'] = pd.to_datetime(data_with_indicator['date'])
            
            # print(data_with_indicator)
            
            #在pybroker中注册指标名称
            '''MACD指标'''
            pb.register_columns('macd')
            pb.register_columns('macdsignal')
            pb.register_columns('macdhist')
            
            
            '''MFI指标'''
            pb.register_columns('MFI')
            
            
            #创建策略
            strategy = Strategy(data_with_indicator, start_date=pb.param(name='start_date'), end_date=pb.param(name='end_date'), config=my_config)

            #配置策略执行参数
            strategy.add_execution(buy_with_indicator, symbols=[symbolCode])
           
            # 执行回测，并打印出回测结果的度量值（四舍五入到小数点后四位）
            result = strategy.backtest()
            print(result.metrics_df.round(2))
            return_order_metrics = result.metrics_df.round(2)
            
            trade_count=0
            initial_market_value=0
            
            for index,row in return_order_metrics.iterrows():
                name = row['name']
                value = row['value']
                
                if(name=='trade_count'): trade_count=value
                elif (name=='initial_market_value'): initial_market_value=value
                elif (name=='end_market_value'): end_market_value=value
                elif (name=='total_pnl'): total_pnl=value
                elif (name=='unrealized_pnl'): unrealized_pnl=value
                elif (name=='total_return_pct'): total_return_pct=value
                elif (name=='total_profit'): total_profit=value
                elif (name=='total_loss'): total_loss=value
                elif (name=='total_fees'): total_fees=value
                elif (name=='max_drawdown'): max_drawdown=value
                elif (name=='max_drawdown_pct'): max_drawdown_pct=value
                elif (name=='win_rate'): win_rate=value
                elif (name=='loss_rate'): loss_rate=value
                elif (name=='winning_trades'): winning_trades=value
                elif (name=='losing_trades'): losing_trades=value
                elif (name=='avg_pnl'): avg_pnl=value
                elif (name=='avg_return_pct'): avg_return_pct=value
                elif (name=='avg_trade_bars'): avg_trade_bars=value
                elif (name=='avg_profit'): avg_profit=value
                elif (name=='avg_profit_pct'): avg_profit_pct=value
                elif (name=='avg_winning_trade_bars'): avg_winning_trade_bars=value
                elif (name=='avg_loss'): avg_loss=value
                elif (name=='avg_loss_pct'): avg_loss_pct=value
                elif (name=='avg_losing_trade_bars'): avg_losing_trade_bars=value
                elif (name=='largest_win'): largest_win=value
                elif (name=='largest_win_pct'): largest_win_pct=value
                elif (name=='largest_win_bars'): largest_win_bars=value
                elif (name=='largest_loss'): largest_loss=value
                elif (name=='largest_loss_pct'): largest_loss_pct=value
                elif (name=='largest_loss_bars'): largest_loss_bars=value
                elif (name=='max_wins'): max_wins=value
                elif (name=='max_losses'): max_losses=value
                elif (name=='sharpe'): sharpe=value
                elif (name=='sortino'): sortino=value
                elif (name=='profit_factor'): profit_factor=value
                elif (name=='ulcer_index'): ulcer_index=value
                elif (name=='upi'): upi=value
                elif (name=='equity_r2'): equity_r2=value
                elif (name=='std_error'): std_error=value
            
            insertsql = text("INSERT INTO return_metrics (symbolCode, stockName, trade_count, initial_market_value, end_market_value, total_pnl, unrealized_pnl, total_return_pct, total_profit, total_loss, total_fees, max_drawdown, max_drawdown_pct, win_rate, loss_rate, winning_trades, losing_trades, avg_pnl, avg_return_pct, avg_trade_bars, avg_profit, avg_profit_pct, avg_winning_trade_bars, avg_loss, avg_loss_pct, avg_losing_trade_bars, largest_win, largest_win_pct, largest_win_bars, largest_loss, largest_loss_pct, largest_loss_bars, max_wins, max_losses, sharpe, sortino, profit_factor, ulcer_index, upi, equity_r2, std_error) VALUES ('" 
                              + symbolCode 
                              + "', '" + stockName 
                              + "', " + str(trade_count) 
                              + ", " + str(initial_market_value) 
                              + ", " + str(end_market_value) 
                              + ", " + str(total_pnl) 
                              + ", " + str(unrealized_pnl) 
                              + ", " + str(total_return_pct) 
                              + ", " + str(total_profit) 
                              + ", " + str(total_loss) 
                              + ", " + str(total_fees) 
                              + ", " + str(max_drawdown) 
                              + ", " + str(max_drawdown_pct) 
                              + ", " + str(win_rate) 
                              + ", " + str(loss_rate) 
                              + ", " + str(winning_trades) 
                              + ", " + str(losing_trades) 
                              + ", " + str(avg_pnl) 
                              + ", " + str(avg_return_pct) 
                              + ", " + str(avg_trade_bars) 
                              + ", " + str(avg_profit) 
                              + ", " + str(avg_profit_pct) 
                              + ", " + str(avg_winning_trade_bars) 
                              + ", " + str(avg_loss) 
                              + ", " + str(avg_loss_pct) 
                              + ", " + str(avg_losing_trade_bars) 
                              + ", " + str(largest_win) 
                              + ", " + str(largest_win_pct) 
                              + ", " + str(largest_win_bars) 
                              + ", " + str(largest_loss) 
                              + ", " + str(largest_loss_pct) 
                              + ", " + str(largest_loss_bars) 
                              + ", " + str(max_wins) 
                              + ", " + str(max_losses) 
                              + ", " + str(sharpe) 
                              + ", " + str(sortino) 
                              + ", " + str(profit_factor) 
                              + ", " + str(ulcer_index) 
                              + ", " + str(upi) 
                              + ", " + str(equity_r2)                             
                              + ", " + str(std_error) + ")")
                
            conn.execute(insertsql)
                        
            return_order_df = result.orders
            return_order_df.to_sql(name="return_order", con=conn, index=False ,if_exists='append')
            
            return_positions_df = result.positions
            return_positions_df.to_sql(name="return_positions", con=conn, index=False ,if_exists='append')
            
            return_portfolio_df = result.portfolio
            return_portfolio_df.to_sql(name="return_portfolio", con=conn, index=False ,if_exists='append')
            
            return_trades_df = result.trades
            return_trades_df.to_sql(name="return_trades", con=conn, index=False ,if_exists='append')
            
            conn.commit()
            
        except Exception as error:
            print(symbolCode, stockName, "回测异常", error)
        else:
            print(symbolCode, stockName,'回测完成')
                    
    print("回测完成")


# 定义全局参数 "stock_code"（股票代码）
pb.param(name='stock_code', value='600000') 
# 定义全局参数 "start_date" 开始日期
pb.param(name='start_date', value='20230101') 
# 定义全局参数 "end_date" 结束日期
pb.param(name='end_date', value='20231231') 
    
# 定义全局参数 "percent"（持仓百分比） 1代表100% 0.25代表25%
pb.param(name='percent', value=0.25)
# 定义全局参数 "stop_loss_pct"（止损百分比）
pb.param(name='stop_loss_pct', value=10)
# 定义全局参数 "stop_profit_pct"（止盈百分比）
pb.param(name='stop_profit_pct', value=10)

# 创建策略配置，初始资金为 500000
my_config = pb.StrategyConfig(initial_cash=500000)


#数据库连接参数
hostname = "localhost" #数据库IP
dbname = "qtp" #数据库名
uname = "root" #用户名
pwd = "ASDFqwer1234" #密码    
engine = create_engine('mysql+pymysql://' + uname + ':' + pwd + '@' + hostname + '/' + dbname + '')
execute_backtest(engine)