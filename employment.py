import pandas as pd
import requests
import json
import prettytable
from collections import defaultdict
import matplotlib.pyplot as plt
from data import BLS_ID_MAP_SA
ids = [key for key in BLS_ID_MAP_SA]
sectors = [BLS_ID_MAP_SA[key] for key in BLS_ID_MAP_SA]
df_all = pd.DataFrame()

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ids,"startyear":"2010", "endyear":"2023", "registrationkey": "92236dd12f5d4ca4a57067720b68285c"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)
for series in json_data['Results']['series']:
    date_tmp = []
    value_tmp = []
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        date = year + period
        value = float(item['value'])
        date_tmp.append(date)
        value_tmp.append(value)
    df_tmp = pd.DataFrame({"date": date_tmp, seriesId: value_tmp})
    if df_all.empty:
        df_all = df_tmp.copy()
    else:
        df_all = df_all.merge(df_tmp, how="inner", on="date")
df_all.rename(columns=BLS_ID_MAP_SA, inplace=True)
df_all_perc = df_all.copy()
df_all_perc.sort_values(by=["date"], ascending=True, inplace=True)
df_all_perc.set_index("date", inplace=True)
df_all_perc.drop(columns=["Total Nonfarm"], inplace=True)
data_perc = df_all_perc.divide(df_all_perc.sum(axis=1), axis=0)
for sector in sectors:
    # df_all[sector + "_previous"] = df_all[sector].shift(-1)
    df_all[sector + "_MOMCHG"] = df_all[sector].diff(periods=-1)
df_all.sort_values(by=["date"], ascending=True, inplace=True)
print ("done")
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('employment_all.pdf')
for sector in sectors:
    plot_tmp = df_all.plot(x="date", y=sector + "_MOMCHG", rot=90, fontsize=10, figsize=(30, 18), kind='bar', color="red")
    plot_tmp.legend(loc=2, fontsize=20)
    plot_tmp.set_ylabel('Thousands', fontdict={'fontsize': 20})

    plot_tmp2 = plot_tmp.twinx()
    plot_tmp3 = df_all.plot(x="date", y=sector, rot=90, fontsize=10, figsize=(30, 18), kind='line', color="blue", ax=plot_tmp2)
    plot_tmp3.legend(loc=1, fontsize=20)
    plot_tmp3.set_ylabel('Thousands', fontdict={'fontsize': 20})
    pp.savefig(plot_tmp3.get_figure())
pp.close()
# ax = df_all_perc.plot.area(rot=90, fontsize=10, figsize=(30, 18))
# pp2 = PdfPages('employment_total.pdf')
# for sector in sectors:
#     plot_tmp = df_all.plot(x="date", y=sector, rot=90, fontsize=10, figsize=(30, 18), kind='bar', color="red")
#     plot_tmp.legend(loc=2, fontsize=20)
#     plot_tmp.set_ylabel('Thousands', fontdict={'fontsize': 20})
#     pp2.savefig(plot_tmp.get_figure())
# pp2.close()
