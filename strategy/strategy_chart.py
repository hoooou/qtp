# -*- coding: utf-8 -*-
"""
图表函数
"""

from pyecharts import options as opts
from pyecharts.charts import Kline, Page, Grid, Bar, Line
from pyecharts.components import Table
from pyecharts.globals import ThemeType

import pandas as pd


def create_marker_value_chart( result) -> Line:
    line = Line(init_opts=opts.InitOpts(width="100%", height="400px"))

    # 获取日期和市值数据
    dates = result.portfolio.index.strftime(
        "%Y-%m-%d"
    ).tolist()  # 日期格式调整为可读的格式
    market_values = result.portfolio["market_value"].values.tolist()  # 市值数据

    # 添加 X 轴和 Y 轴数据
    line.add_xaxis(dates)
    line.add_yaxis(
        series_name="市值",
        y_axis=market_values,
        is_smooth=True,  # 曲线平滑显示
        linestyle_opts=opts.LineStyleOpts(width=2, color="blue"),
        label_opts=opts.LabelOpts(is_show=False),  # 隐藏数据点标签
    )

    # 设置全局配置
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="市值走势"),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            boundary_gap=False,  # 使得折线图从坐标轴开始
            axislabel_opts=opts.LabelOpts(rotate=45),  # 旋转日期标签避免重叠
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            is_scale=True,  # 根据数据自适应
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross",  # 设置十字线
            background_color="rgba(245, 245, 245, 0.8)",
            border_width=1,
            border_color="#ccc",
            textstyle_opts=opts.TextStyleOpts(color="#000"),
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                is_show=True,
                type_="inside",
                xaxis_index=[0, 1, 2, 3],  # 确保和K线图、MACD1共享同一组X轴索引
                range_start=0,
                range_end=100,
            ),
            opts.DataZoomOpts(
                is_show=True,
                type_="slider",
                xaxis_index=[0, 1, 2, 3],  # 确保和K线图、MACD1共享同一组X轴索引
                range_start=0,
                range_end=100,
            ),
        ],
    )

    return line


def create_KLine_Chart(data, result) -> Kline:
    xdf = data[["date"]]
    xdf.index = pd.to_datetime(xdf.date)

    ydf = data[["open", "close","low", "high"]]

    all_points = result.orders[["type", "date", "fill_price"]]

    buy_points = all_points[all_points["type"] == "buy"]
    sell_points = all_points[all_points["type"] == "sell"]

    buy_points = buy_points[["date", "fill_price"]]
    sell_points = sell_points[["date", "fill_price"]]

    buy_points["date"] = pd.to_datetime(buy_points["date"], unit="s").dt.strftime(
        "%Y%m%d"
    )
    sell_points["date"] = pd.to_datetime(sell_points["date"], unit="s").dt.strftime(
        "%Y%m%d"
    )

    buy_points = dict(zip(buy_points["date"], buy_points["fill_price"]))
    sell_points = dict(zip(sell_points["date"], sell_points["fill_price"]))

    kline = Kline(init_opts=opts.InitOpts(width="100%", height="400px"))
    kline.add_xaxis(xdf.index.strftime("%Y%m%d").tolist())
    kline.add_yaxis(
        "kline",
        y_axis=ydf.values.tolist(),
        markpoint_opts=opts.MarkPointOpts(
            # 标记点数据
            data=[
                *[
                    # MarkPointItem：标记点数据项
                    opts.MarkPointItem(
                        # 标注名称
                        name=value,
                        type_=None,
                        value_index=None,
                        value_dim=None,
                        coord=[day, value],
                        value="买",
                        x=None,  # 一般默认就好
                        y=None,  # 一般默认就好
                        symbol=None,  # 一般默认就好
                        symbol_size=None,  # 一般默认就好
                        itemstyle_opts={"color": "RED"},
                    )
                    for day, value in buy_points.items()
                ],
                *[
                    # MarkPointItem：标记点数据项
                    opts.MarkPointItem(
                        # 标注名称
                        name=value,
                        type_=None,
                        value_index=None,
                        value_dim=None,
                        coord=[day, value],
                        value="卖",
                        x=None,  # 一般默认就好
                        y=None,  # 一般默认就好
                        symbol=None,  # 一般默认就好
                        symbol_size=None,  # 一般默认就好
                        itemstyle_opts={"color": "GREEN"},
                    )
                    for day, value in sell_points.items()
                ],
            ],
            symbol=None,  # 一般默认就好
            symbol_size=None,  # 一般默认就好
            label_opts=opts.LabelOpts(position="inside", color="#fff"),
        ),
    )

    kline.set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                is_show=True,
                type_="inside",
                xaxis_index=[0, 1, 2, 3],  # 确保和K线图、MACD1共享同一组X轴索引
                range_start=0,
                range_end=100,
            ),
            opts.DataZoomOpts(
                is_show=True,
                type_="slider",
                xaxis_index=[0, 1, 2, 3],  # 确保和K线图、MACD1共享同一组X轴索引
                range_start=0,
                range_end=100,
            ),
        ],
        title_opts=opts.TitleOpts(title="回测图表"),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross",  # 设置十字线
            background_color="rgba(245, 245, 245, 0.8)",
            border_width=1,
            border_color="#ccc",
            textstyle_opts=opts.TextStyleOpts(color="#000"),
        ),
    )
    # kline.render("K线图.html")
    # kline.overlap(create_MACD_Chart(data,result))
    return kline


def create_MACD_Chart(data, result) -> Line:
    xdf = data[["date"]]
    xdf.index = pd.to_datetime(xdf.date)
    ydf_dif = data[["macd"]]
    ydf_dea = data[["macdsignal"]]

    line = (
        Line()
        .add_xaxis(xdf.index.strftime("%Y%m%d").tolist())
        .add_yaxis("macd", y_axis=ydf_dif.values.tolist())
        .add_yaxis("macdsignal", y_axis=ydf_dea.values.tolist())
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross",  # 设置十字线
            background_color="rgba(245, 245, 245, 0.8)",
            border_width=1,
            border_color="#ccc",
            textstyle_opts=opts.TextStyleOpts(color="#000"),
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                is_show=True,
                type_="inside",
                xaxis_index=[0, 1, 2, 3],  # 确保和K线图、MACD1共享同一组X轴索引
                range_start=0,
                range_end=100,
            ),
            opts.DataZoomOpts(
                is_show=True,
                type_="slider",
                xaxis_index=[0, 1, 2, 3],  # 确保和K线图、MACD1共享同一组X轴索引
                range_start=0,
                range_end=100,
            ),
        ],
    )
    return line


def create_MFI_Chart(data, result) -> Line:
    xdf = data[["date"]]
    xdf.index = pd.to_datetime(xdf.date)
    ydf_dif = data[["MFI"]]

    line = (
        Line()
        .add_xaxis(xdf.index.strftime("%Y%m%d").tolist())
        .add_yaxis("MFI", y_axis=ydf_dif.values.tolist())
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross",  # 设置十字线
            background_color="rgba(245, 245, 245, 0.8)",
            border_width=1,
            border_color="#ccc",
            textstyle_opts=opts.TextStyleOpts(color="#000"),
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                is_show=True,
                type_="inside",
                xaxis_index=[0, 1, 2, 3],  # 确保和K线图、MACD1共享同一组X轴索引
                range_start=0,
                range_end=100,
            ),
            opts.DataZoomOpts(
                is_show=True,
                type_="slider",
                xaxis_index=[0, 1, 2, 3],  # 确保和K线图、MACD1共享同一组X轴索引
                range_start=0,
                range_end=100,
            ),
        ],
    )
    return line

def create_SMA_Chart(data, result) -> Line:
    xdf = data[["date"]]
    xdf.index = pd.to_datetime(xdf.date)
    ydf_dif = data[["SMA250"]]

    line = (
        Line()
        .add_xaxis(xdf.index.strftime("%Y%m%d").tolist())
        .add_yaxis("SMA250", y_axis=ydf_dif.values.tolist())
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross",  # 设置十字线
            background_color="rgba(245, 245, 245, 0.8)",
            border_width=1,
            border_color="#ccc",
            textstyle_opts=opts.TextStyleOpts(color="#000"),
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                is_show=True,
                type_="inside",
                xaxis_index=[0, 1, 2, 3],  # 确保和K线图、MACD1共享同一组X轴索引
                range_start=0,
                range_end=100,
            ),
            opts.DataZoomOpts(
                is_show=True,
                type_="slider",
                xaxis_index=[0, 1, 2, 3],  # 确保和K线图、MACD1共享同一组X轴索引
                range_start=0,
                range_end=100,
            ),
        ],
    )
    return line


def create_strategy_bar(result) -> Grid:
    #    all_points = result.portfolio[['date','cash','equity','pnl']]
    #    all_points['date'] = pd.to_datetime(all_points['date'], unit='s').dt.strftime('%Y%m%d')
    #    all_points = dict(zip(all_points['date'], all_points['cash']))
    ydf = result.portfolio[["pnl"]]
    #    y=[88, 102, 47, 107, 130, 31, 58]

    buy_points = {"周二": 0, "周三": 100}

    bar = Bar(
        init_opts=opts.InitOpts(theme=ThemeType.DARK, width="100%",height="300px")
    )
    bar.add_xaxis(result.portfolio.index.strftime("%Y%m%d").tolist())

    bar.add_yaxis(
        "收益(Profit & Loss)",
        ydf.pnl.tolist(),
        # MarkPointOpts：标记点配置项
        markpoint_opts=opts.MarkPointOpts(
            # 标记点数据
            data=[
                *[
                    # MarkPointItem：标记点数据项
                    opts.MarkPointItem(
                        # 标注名称
                        name="自定义标记点",
                        type_=None,
                        value_index=None,
                        value_dim=None,
                        coord=[day, value],  # 这里是直角坐标系x轴第三个，y轴第三个
                        value=value,
                        x=None,  # 一般默认就好
                        y=None,  # 一般默认就好
                        symbol=None,  # 一般默认就好
                        symbol_size=None,  # 一般默认就好
                        itemstyle_opts=None,
                    )
                    for day, value in buy_points.items()
                ],
            ],
            symbol=None,  # 一般默认就好
            symbol_size=None,  # 一般默认就好
            label_opts=opts.LabelOpts(position="inside", color="#fff"),
        ),
    )
    # bar.add_yaxis("商家B", Faker.values())
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=""),
        legend_opts=opts.LegendOpts(
            type_="plain",
            selected_mode=True,
            is_show=False,
            pos_left=None,
            pos_right=None,
            pos_top=None,
            pos_bottom=None,
            orient="horizontal",
            align="auto",
            padding=5,
            item_gap=10,
            item_width=25,
            item_height=14,
            inactive_color="#ccc",
            textstyle_opts=None,
            legend_icon=None,
        ),
    )
    bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示标签
    # bar.render("bar_markpoint_custom.html")
    grid = Grid()
    grid.add(
        bar,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%"),  # 设置左右边距
    )

    return grid


def printResult(df: pd.DataFrame):
    import pandas as pd

    # 假设 result.metrics_df 已经存在，并且包含您的数据
    # 中文名称映射字典
    zh_names = {
        "total_return_pct": "总回报率",
        "benchmark_return": "股票基准收益率",
        "max_drawdown_pct": "最大回撤（百分比）",
        "win_rate": "胜率",
        "largest_win_pct": "最大盈利交易（百分比）",
        "largest_loss_pct": "最大亏损交易（百分比）",
        "trade_count": "交易次数",
        "sharpe": "夏普比率",
        "profit_factor": "盈亏比",
        "initial_market_value": "初始市值",
        "end_market_value": "期末市值",
        "total_pnl": "总盈亏",
        "unrealized_pnl": "未实现盈亏",
        "annual_return_pct": "年化总回报率",
        "total_profit": "总盈利",
        "total_loss": "总亏损",
        "total_fees": "总手续费",
        "max_drawdown": "最大回撤（现金）",
        "loss_rate": "亏损率",
        "winning_trades": "盈利交易次数",
        "losing_trades": "亏损交易次数",
        "avg_pnl": "每笔交易平均盈亏",
        "avg_return_pct": "每笔交易平均回报率",
        "avg_trade_bars": "每笔交易平均K线数",
        "avg_profit": "每笔交易平均盈利",
        "avg_profit_pct": "每笔交易平均盈利率",
        "avg_winning_trade_bars": "盈利交易的平均K线数",
        "avg_loss": "每笔交易平均亏损",
        "avg_loss_pct": "每笔交易平均亏损率",
        "avg_losing_trade_bars": "亏损交易的平均K线数",
        "largest_win": "最大盈利交易",
        "largest_win_bars": "最大盈利交易的K线数",
        "largest_loss": "最大亏损交易",
        "largest_loss_bars": "最大亏损交易的K线数",
        "max_wins": "最大连续盈利交易次数",
        "max_losses": "最大连续亏损交易次数",
        "sortino": "索提诺比率",
        "calmar": "卡尔玛比率",
        "ulcer_index": "溃疡指数",
        "upi": "溃疡表现指数",
        "equity_r2": "净值R²",
        "std_error": "标准误差",
        "annual_std_error": "年化标准误差",
        "annual_volatility_pct": "年化波动率（百分比）",
    }
    # 过滤并重排 DataFrame 中的行顺序
    df = df[df['name'].isin(zh_names.keys())]  # 只保留在 zh_names 中定义的行
    df['zh_name'] = df['name'].map(zh_names)  # 添加中文名称列
    df = df.set_index('name').reindex(zh_names.keys()).reset_index()  # 按 zh_names 键顺序重新排序

    # 调整列顺序，使 'zh_name' 列紧挨着 'name' 列
    df = df[['zh_name', 'name'] + [col for col in df.columns if col not in ['name', 'zh_name']]]
    return df

def create_strategy_info(result,benchmark_return) -> Table:
    table = Table()
    df=result.metrics_df
    new_row = pd.DataFrame({"name": ["benchmark_return"], "value": [benchmark_return]})
    df = pd.concat([result.metrics_df, new_row], ignore_index=True)
    metrics = printResult(df).round(2)
    # metrics = result.metrics_df
    headers = metrics.columns.tolist()
    rows = [list(row) for row in metrics.values]
    # print(headers)
    # print(rows)
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="回测绩效")
    )
    return table


def create_strategy_orders(result) -> Table:
    table = Table()

    metrics = result.orders

    headers = metrics.columns.tolist()
    rows = [list(row) for row in metrics.values]
    # print(headers)
    # print(rows)
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="订单")
    )
    return table


def create_strategy_positions(result) -> Table:
    table = Table()
    metrics = result.positions
    metrics["时间"] = metrics.index.get_level_values("date")
    metrics = metrics[["时间"] + [col for col in metrics.columns if col != "时间"]]
    headers = metrics.columns.tolist()
    rows = [list(row) for row in metrics.values]
    # print(headers)
    # print(rows)
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="持仓")
    )
    return table


def create_strategy_portfolio(result) -> Table:
    table = Table()

    metrics = result.portfolio
    metrics["时间"] = metrics.index.get_level_values("date")
    metrics = metrics[["时间"] + [col for col in metrics.columns if col != "时间"]]
    headers = metrics.columns.tolist()
    rows = [list(row) for row in metrics.values]
    # print(headers)
    # print(rows)
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="投资组合")
    )
    return table


def create_strategy_trades(result) -> Table:
    table = Table()

    metrics = result.trades

    headers = metrics.columns.tolist()
    rows = [list(row) for row in metrics.values]
    # print(headers)
    # print(rows)
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="交易")
    )
    return table


# 图表聚合
def create_strategy_charts(df, result,benchmark_return):
    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width="100%",
            height="1200px",
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    # 添加K线图表
    marker_chart = create_marker_value_chart( result)
    # 添加K线图表
    kline_chart = create_KLine_Chart(df, result)
    # 第一个MACD图表
    macd_chart_1 = create_MACD_Chart(df, result)
    # 第二个MFI图表
    mfi_chart = create_MFI_Chart(df, result)
    # 第三个SMA图表
    # mfi_chart = create_SMA_Chart(df, result)
    # 添加图表到Grid布局中
    grid_chart.add(
        marker_chart,
        grid_opts=opts.GridOpts(
            pos_left="5%", pos_right="10%", height="300px", width="90%"
        ),
    )
    grid_chart.add(
        kline_chart,
        grid_opts=opts.GridOpts(
            pos_left="5%", pos_right="10%", pos_top="450px", height="300px", width="90%"
        ),
    ).add(
        macd_chart_1,
        grid_opts=opts.GridOpts(
            pos_left="5%", pos_right="10%", pos_top="780px", height="150px", width="90%"
        ),
    ).add(
        mfi_chart,
        grid_opts=opts.GridOpts(
            pos_left="5%", pos_right="10%", pos_top="950px", height="150px", width="90%"
        ),
    )

    # 渲染页面
    page1 = Page(layout=opts.PageLayoutOpts(
        justify_content="flex-start", display="flex", flex_wrap="wrap"
    ))
    page1.add(
        grid_chart,
        create_strategy_bar(result),
        create_strategy_info(result,benchmark_return),
        create_strategy_trades(result),
        create_strategy_orders(result),
        create_strategy_portfolio(result),
        create_strategy_positions(result),
    ).render("K线图.html")

# 图表聚合
def create_strategy_result_charts(result):
    grid_chart = Grid(
        init_opts=opts.InitOpts(
            width="100%",
            height="400px",
            animation_opts=opts.AnimationOpts(animation=False),
        )
    )
    # 添加K线图表
    marker_chart = create_marker_value_chart( result)
    # 添加图表到Grid布局中
    grid_chart.add(
        marker_chart,
        grid_opts=opts.GridOpts(
            pos_left="5%", pos_right="10%", height="300px", width="90%"
        ),
    )
    # 渲染页面
    page1 = Page(layout=opts.PageLayoutOpts(
        justify_content="flex-start", display="flex", flex_wrap="wrap"
    ))
    page1.add(
        grid_chart,
        create_strategy_bar(result),
        create_strategy_info(result,0),
        create_strategy_trades(result),
        create_strategy_orders(result),
        create_strategy_portfolio(result),
        create_strategy_positions(result),
    ).render("result_K线图.html")
