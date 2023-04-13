from web3 import Web3
import datetime
import concurrent.futures
import multiprocessing

w3_http_provider_url = "https://mainnet.infura.io/v3/abf2599d4d184669936ee3d302f8ce67"
out_file = "/Users/administrator/Documents/new_contract_addresses.txt"


def process_tx(tx):
    # Get the transaction receipt
    w3 = Web3(Web3.HTTPProvider(w3_http_provider_url))
    receipt = w3.eth.getTransactionReceipt(tx)

    # Check if the transaction is a contract creation
    if receipt.contractAddress:
        # Write the contract address to the file
        with open(out_file, "a") as f:
            f.write(receipt.contractAddress + "\n")


def extract_and_store(n=1, num_threads=4):
    # Connect to Ethereum node
    w3 = Web3(Web3.HTTPProvider(w3_http_provider_url))

    # Calculate the timestamp for n months ago
    n_months_ago = int((datetime.datetime.now() - datetime.timedelta(days=n * 30)).timestamp())

    # Get the latest block number
    latest_block = w3.eth.blockNumber

    # Create a thread pool executor
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)

    # Iterate through blocks from latest to oldest
    for block_num in range(latest_block, 0, -1):
        # Get the block data
        block = w3.eth.getBlock(block_num)

        # Check if the block timestamp is older than n months ago
        if block.timestamp < n_months_ago:
            break

        print(f"Checking block posted on: {datetime.datetime.fromtimestamp(block.timestamp)}")

        # Submit each transaction to the thread pool executor
        for tx in block.transactions:
            executor.submit(process_tx, tx)

    # Wait for all submitted tasks to complete
    executor.shutdown(wait=True)


if __name__ == '__main__':
    extract_and_store(n=600, num_threads=multiprocessing.cpu_count())
