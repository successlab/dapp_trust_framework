def read_address_list():
	with open("address_list.txt", "r") as f:
		raw_str = f.read()

	addresses = raw_str.split("\n")
	return addresses


if __name__ == '__main__':
	addresses = read_address_list()
	print("Number of addresses read: ", len(addresses))
	print("Addresses:")
	print(addresses)
