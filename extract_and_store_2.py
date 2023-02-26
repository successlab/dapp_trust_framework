import subprocess
import json
import time
from math import ceil

import requests


def run_securify(address, api_key_path):
	cmd = f"sudo docker run -it securify {address} --from-blockchain --key {api_key_path}"
	output = subprocess.check_output(cmd, shell=True).decode()
	# print(output)
	return output


def extract_securify_data(addresses, api_key_path):
	with open('tool_output.csv', 'w') as f:
		f.write("Address,tool_output\n")
		for address in addresses:
			print("Checking ", address)
			try:
				result = run_securify(address, api_key_path)
				result_dict = {"output": result}
				f.write(address + "," + json.dumps(result_dict) + '\n')
				print("Finished ", address)
			except:
				print("Failed ", address)

			time.sleep(2)


def extract_trust_score_output(addresses, out_csv_path="trust_score_output.csv"):
	with open(out_csv_path, "w+") as f:
		f.write("Address,trust_output\n")

		for address in addresses:
			print("Checking ", address)
			try:
				params = {
					'address': address,
				}

				response = requests.get('http://127.0.0.1:8000/trust_scoring/get_trust_score/',
										params=params)
				resp_data = response.json()
				f.write(address + "," + str(resp_data) + '\n')
				print("Finished ", address)

			except:
				print("Failed ", address)

			time.sleep(0.7)


def read_address_list(filename="address_list.txt"):
	with open(filename, "r") as f:
		raw_str = f.read()

	addresses = raw_str.split("\n")
	return addresses


def get_web3js_api_output(address):
	cookies = {
		'csrftoken': 'nMuzkziT2RUPVhHP9mee0Fmo2AfE7GsrohaT8F5SLtsSncaAa22Yi9dTtIuD9tFe',
	}

	headers = {
		'Content-Type': 'application/json',
		# 'Cookie': 'csrftoken=nMuzkziT2RUPVhHP9mee0Fmo2AfE7GsrohaT8F5SLtsSncaAa22Yi9dTtIuD9tFe',
	}

	json_data = {
		'address': addresses,
	}

	response = requests.get('http://localhost:8000/web3jstrust/web3js_stats/', cookies=cookies, headers=headers,
							json=json_data)

	return response.json()


def get_abi_output(address):
	cookies = {
		'csrftoken': 'nMuzkziT2RUPVhHP9mee0Fmo2AfE7GsrohaT8F5SLtsSncaAa22Yi9dTtIuD9tFe',
	}

	headers = {
		# 'Cookie': 'csrftoken=nMuzkziT2RUPVhHP9mee0Fmo2AfE7GsrohaT8F5SLtsSncaAa22Yi9dTtIuD9tFe',
	}

	params = {
		'address': address,
	}

	response = requests.get('http://localhost:8000/web3jstrust/abi_availability/', params=params, cookies=cookies,
							headers=headers)

	return response.json()


def extract_and_store_w3js_and_abi(addresses, out_csv_path):
	with open(out_csv_path, "w+") as f:
		f.write("Address,contains_w3js,contains_abi\n")

		for address in addresses:
			print("Checking: ", address)
			try:
				w3js_output = get_web3js_api_output(address)
				contains_w3js = 1 if len(w3js_output["web3js_uses"]) != 0 else 0
			except:
				print(f"Failed web3js check for {address}")
				contains_w3js = 0

			try:
				contains_abi = get_abi_output(address)
			except:
				print(f"Failed ABI check for {address}")
				contains_abi = 0

			f.write(address + "," + str(contains_w3js) + "," + str(contains_abi) + '\n')
			print("Finished ", address)


if __name__ == '__main__':
	address_list_file_name = "addresses_to_check.txt"
	addresses = read_address_list(address_list_file_name)
	api_key_path = '/sec/api_key.txt'
	# extract_securify_data(addresses, api_key_path)

	out_path_base = "/Users/administrator/Documents/w3js_abi_data_extraction/"
	addresses = addresses[4961:]
	part_len = 50
	last_part = ceil(len(addresses) / part_len)

	for i in range(last_part + 1):
		print("------------")
		print(f"PART {i} starting")
		print("------------\n")
		start_range = i * part_len
		ending_range = start_range + part_len

		out_csv_name = f"second_half_part{i}"
		chunk_addresses = addresses[start_range:ending_range]
		extract_and_store_w3js_and_abi(chunk_addresses, out_path_base + out_csv_name)

	# out_csv_path = "/Users/administrator/Documents/trust_score_output_dataset1.csv"
	# # starting_i = addresses.index("0x3A306a399085F3460BbcB5b77015Ab33806A10d5")
	# # print("Starting i: ", starting_i)
	# # extract_trust_score_output(addresses[(starting_i+1):], out_csv_path)
	# extract_trust_score_output(addresses, out_csv_path)

