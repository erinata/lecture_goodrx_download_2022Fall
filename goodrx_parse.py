import pandas
from bs4 import BeautifulSoup

import os
import re

import glob

if not os.path.exists("parsed_files"):
	os.mkdir("parsed_files")

df = pandas.DataFrame()

for file_name in glob.glob("html_files/*.html"):
	# file_name = "./html_files/goodrx_zoloft_tablet_50mg_30_20220915154739.html"
	base_name = os.path.basename(file_name)

	name = re.findall('goodrx_(.*)_(.*)_(.*)_(.*)_', base_name)[0][0]
	form = re.findall('goodrx_(.*)_(.*)_(.*)_(.*)_', base_name)[0][1]
	dosage = re.findall('goodrx_(.*)_(.*)_(.*)_(.*)_', base_name)[0][2]
	quantity = re.findall('goodrx_(.*)_(.*)_(.*)_(.*)_', base_name)[0][3]

	scrape_time = re.findall('\\d{14}', base_name)[0]


	# print(name)
	# print(form)
	# print(dosage)
	# print(quantity)
	# print(scrape_time)


	f =  open(file_name, "r")
	soup = BeautifulSoup(f.read(), "html.parser")
	f.close()


	# print(soup)
	pharmacy_list = soup.find("div", {"aria-label": "List of pharmacy prices"})

	# print(pharmacy_list)
	pharmacy_row_box_list = pharmacy_list.find_all("div", {"data-qa": "pharmacy-row-box"})
	# print(pharmacy_row_box_list)

	for pharmacy_row in pharmacy_row_box_list:
		pharmacy_name = pharmacy_row.find("span", {"aria-hidden": "true"}).text
		# print(pharmacy_name)
		price = pharmacy_row.find("span", {"data-qa": "pharmacy-row-price"}).text
		price = price.replace(" ", "")
		# print(price)


		how_to_reg = pharmacy_row.find("span", {"class": "how_to_reg"})
		if how_to_reg is None:
			how_to_reg = "no-discount"
		else:
			how_to_reg = "with-discount"




		df = pandas.concat([df,  
		pandas.DataFrame.from_records([{
			"pharmacy_name": pharmacy_name,
			"price": price,
			"goodrx_discount": how_to_reg,
			"name": name,
			"form": form,
			"dosage": dosage,
			"quantity": quantity,
			"scrape_time": scrape_time
			}])
		])


df.to_csv("parsed_files/goodrx_dataset.csv", index=False)

print("done")




