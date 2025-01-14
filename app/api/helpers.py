from django.db import connections
import matplotlib.pyplot as plt
from io import StringIO
import calendar
import numpy as np
from time import gmtime, strftime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from utilsforecast.plotting import plot_series

GROUP_BY_DAY = 11
GROUP_BY_MONTH = 12
GROUP_BY_YEAR = 13


def transpone(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]


def plot_predictions(series, predictions):
    fig = plot_series(series, predictions, max_ids=4, plot_random=False)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def return_graph(periods, sales):
    fig = plt.figure()

    plt.plot(periods, sales)

    if len(periods) > 20:
        plt.xticks(range(0, len(periods), 3), periods[::3], rotation=75)
    else:
        plt.xticks(rotation=75)


    fig.set_figwidth(15)
    fig.set_figheight(10)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def prepare_plot_data(mylist=[]):
    #mylist = [[123, "2023-02", "Полтава"], [236, "2023-01", "Полтава"], [23, "2023-02", "Харків"], [344, "2023-02", "Кременчук"],
    #            [111, "2023-03", "Полтава"], [236, "2023-01", "Кременчук"], [23, "2023-01", "Харків"], [344, "2023-01", "Лохвиця"],
    #          ]
    #
    periods = list(set(map(lambda x:x[1], mylist)))

    data_arrays = {}

    for data_gr in mylist:
        if data_gr[2] in data_arrays:
            data_arrays[data_gr[2]][data_gr[1]] = data_gr[0]
        else:
            data_arrays[data_gr[2]] = {}
            for period in periods:
                data_arrays[data_gr[2]][period] = 0
            data_arrays[data_gr[2]][data_gr[1]] = data_gr[0]

    return periods, data_arrays


def return_city_graph(periods, data_arr):
    fig = plt.figure()
    fig.set_figwidth(15)
    fig.set_figheight(20)

    n = len(periods)
    r = np.arange(n) 
    width = 0.05
    
    i = 0
    for label, points in data_arr.items():
        plt.bar(r + (i*width), list(points.values()), width = width, label=label) 
        i = i + 1
    
    plt.xlabel("Period") 
    plt.ylabel("Sales") 
    plt.title("Sales by cities") 
    
    plt.xticks(r + width/2, periods) 
    plt.legend() 

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def get_history_data(group_by=GROUP_BY_DAY):
    cursor = connections['proxy_db'].cursor()
    
    last_d = calendar.monthrange(int(strftime("%Y", gmtime())), int(strftime("%m", gmtime())))[1]
    date_to = datetime.today().replace(day=last_d).strftime("%Y-%m-%d")

    if group_by == GROUP_BY_MONTH:
        date_from = datetime.today().replace(day=1) - relativedelta(years=1)
        date_from_str = date_from.strftime("%Y-%m-%d")
    elif group_by == GROUP_BY_YEAR:
        date_from = datetime.today().replace(day=1, month=1) - relativedelta(years=5)
        date_from_str = date_from.strftime("%Y-%m-%d")
    else:
        date_from = datetime.today().replace(day=1)
        date_from_str = (date_from - timedelta(days=date_from.day)).replace(day=1).strftime("%Y-%m-%d")


    cursor.execute("select date(cds1.data_vrem) as day, cds1.sales_yesterday \
        from cd_sales cds1 left join cd_sales cds2 on \
        date(cds1.data_vrem) = date(cds2.data_vrem) and \
        cds1.data_vrem < cds2.data_vrem \
        where cds2.id is null \
        and cds1.data_vrem >= '" + date_from_str + "' \
        and cds1.data_vrem <='" + date_to + "' order by day asc")

    res = cursor.fetchall()
    return transpone(res)


def get_good_graph_data(good_code, group_by=GROUP_BY_DAY, is_category=False):
    cursor = connections['tada_api'].cursor()
    
    last_d = calendar.monthrange(int(strftime("%Y", gmtime())), int(strftime("%m", gmtime())))[1]
    date_to = datetime.today().replace(day=last_d).strftime("%Y-%m-%d")

    if group_by == GROUP_BY_MONTH:
        date_from = datetime.today().replace(day=1) - relativedelta(years=1)
        date_from_str = date_from.strftime("%Y-%m-%d")
        sort_str = "DATE_FORMAT(`date`, '%Y-%m') as d"
    elif group_by == GROUP_BY_YEAR:
        date_from = datetime.today().replace(day=1, month=1) - relativedelta(years=2)
        date_from_str = date_from.strftime("%Y-%m-%d")
        sort_str = "DATE_FORMAT(`date`, '%Y') as d"
    else:
        date_from = datetime.today().replace(day=1)
        date_from_str = (date_from - timedelta(days=date_from.day)).replace(day=1).strftime("%Y-%m-%d")
        sort_str = "DATE_FORMAT(`date`, '%Y-%m-%d') as d"

    if is_category:
        good_filer = " and og.good_code IN (select good_code from Goods where uuid in (select good_uuid from `Goods_ownerships`  \
        where category_uuid = '" + good_code + "'))"
    elif good_code == 0:
        good_filer = ""
    else:
        good_filer = " and og.good_code = " + str(good_code)

    cursor.execute("select count(*) as c, " + sort_str + " from Orders o \
        inner join Order_goods og on o.uuid = og.order_uuid \
        where o.`status` = 4 and o.`date` <= '" + date_to + "' and o.`date` >= '" + date_from_str + "' " 
        + str(good_filer) + " group by d")

    res = cursor.fetchall()

    if len(res) == 0:
        return False

    res = transpone(res)
    return return_graph(res[1], res[0])


def get_city_graph_data(group_by=GROUP_BY_DAY):
    cursor = connections['tada_api'].cursor()
    
    last_d = calendar.monthrange(int(strftime("%Y", gmtime())), int(strftime("%m", gmtime())))[1]
    date_to = datetime.today().replace(day=last_d).strftime("%Y-%m-%d")

    if group_by == GROUP_BY_MONTH:
        date_from = datetime.today().replace(day=1) - relativedelta(years=1)
        date_from_str = date_from.strftime("%Y-%m-%d")
        sort_str = "DATE_FORMAT(`date`, '%Y-%m') as d"
    elif group_by == GROUP_BY_YEAR:
        date_from = datetime.today().replace(day=1, month=1) - relativedelta(years=5)
        date_from_str = date_from.strftime("%Y-%m-%d")
        sort_str = "DATE_FORMAT(`date`, '%Y') as d"
    else:
        date_from = datetime.today().replace(day=1)
        date_from_str = (date_from - timedelta(days=date_from.day)).replace(day=1).strftime("%Y-%m-%d")
        sort_str = "DATE(`date`) as d"


    cursor.execute("select count(*) as c, " + sort_str + ", shipping_city from Orders o \
    inner join Order_goods og on o.uuid = og.order_uuid \
    where o.`date` <= '" + date_to + "' and o.`date` >= '" + date_from_str + "' \
    group by d, shipping_city order by c desc")

    res = cursor.fetchall()
    periods, data_arr = prepare_plot_data(res)
    return return_city_graph(periods, data_arr)

