import subprocess
import json
import time


def run_securify(address, api_key_path):
	cmd = f"sudo docker run -it securify {address} --from-blockchain --key {api_key_path}"
	output = subprocess.check_output(cmd, shell=True).decode()
	# print(output)
	return output


def main(addresses, api_key_path):
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

			time.sleep(0.7)


def read_address_list():
	with open("address_list.txt", "r") as f:
		raw_str = f.read()

	addresses = raw_str.split("\n")
	return addresses


if __name__ == '__main__':
	addresses = read_address_list()
	api_key_path = '/sec/api_key.txt'
	main(addresses, api_key_path)

