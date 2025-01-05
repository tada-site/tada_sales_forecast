from django.db import connections
import matplotlib.pyplot as plt
from io import StringIO
import calendar
from time import gmtime, strftime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

GROUP_BY_DAY = 11
GROUP_BY_MONTH = 12
GROUP_BY_YEAR = 13


def transpone(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]


def return_graph(periods, sales):
    fig = plt.figure()
    plt.plot(periods, sales)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def get_good_graph_data(good_code, group_by=GROUP_BY_DAY, is_category=False):
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

    if is_category:
        good_filer = "IN (select good_code from Goods where uuid in (select good_uuid from `Goods_ownerships`  \
        where category_uuid = '" + good_code + "'))"
    else:
        good_filer = "= " + str(good_code)

    cursor.execute("select count(*) as c, " + sort_str + " from Orders o \
        inner join Order_goods og on o.uuid = og.order_uuid \
        where o.`date` <= '" + date_to + "' and o.`date` >= '" + date_from_str + "' \
        and og.good_code " + str(good_filer) + " group by d")

    res = cursor.fetchall()
    res = transpone(res)
    return return_graph(res[1], res[0])
