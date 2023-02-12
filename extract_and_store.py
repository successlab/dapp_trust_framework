import subprocess
import json
import time
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


def read_address_list():
	with open("address_list.txt", "r") as f:
		raw_str = f.read()

	addresses = raw_str.split("\n")
	return addresses


if __name__ == '__main__':
	addresses = read_address_list()
	api_key_path = '/sec/api_key.txt'
	# extract_securify_data(addresses, api_key_path)

	out_csv_path = "/Users/administrator/Documents/trust_score_output.csv"
	extract_trust_score_output(addresses, out_csv_path)

