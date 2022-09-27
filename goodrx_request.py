import requests
import os

import pandas
import time
import datetime

if not os.path.exists("html_files"):
	os.mkdir("html_files")

headers = {
 	'accept': '*/*',
 	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
	'accept-language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
	'referer': 'https://www.google.com/'
}



download_list = pandas.read_csv("download_list.csv")

for i in range(0,3):
	for index, row in download_list.iterrows():
		name = row["name"]
		form = row["form"]
		dosage = row["dosage"]
		quantity = str(row["quantity"])
		current_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")

		print(current_time, name, form, dosage, quantity)

		f = open("html_files/goodrx" + "_" + name + "_" + form + "_" + dosage + "_" + quantity + "_" + current_time + ".html", "w")

		response = requests.get("https://www.goodrx.com/" + name + "?form=" + form + "&dosage=" + dosage + "&quantity=" + quantity, headers=headers)
		html = response.text
		# print(html)
		f.write(html)
		f.close()
		print("waiting")
		time.sleep(60)
	time.sleep(60)


print("done")




