import os
import time
import logging

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from utils.basic_web3.address_classifier import *
from utils.data_extractor import write_into_dataset
from utils.github_crawler import get_github_all_code_search_results, check_web3js_usage_parallel
from utils.trust_scoring.abi_availability_checker import contains_abi


class CheckWeb3JSStats(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        in_data = request.data
        search_address = in_data["address"]
        if settings.DEBUG is True and settings.ENV_TYPE == "DataExtraction":
            logging.info(f'Received address: {search_address} at {time.strftime(" % Y - % m - % d % H: % M: % S")}')

        # Checking bad input address
        if is_valid_eth_address(search_address) is False or is_contract(search_address) is False:
            return Response(
                {
                    "status": "unsuccessful",
                    "message": "Invalid contract address",
                }
            )

        res = get_github_all_code_search_results(search_address)
        found_web3js_import, found_metamask_trigger, web3js_uses = check_web3js_usage_parallel(res)

        out_data = {
            "status": "successful",
            "found_web3js_import": found_web3js_import,
            "found_metamask_trigger": found_metamask_trigger,
            "web3js_uses": web3js_uses,
            "all_github_code_search_results": res,
        }

        return Response(out_data)


class ExtractData(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        in_csv = os.path.join(settings.BASE_DIR, "final_combined_df2.csv")
        out_chunks_dir = os.path.join(settings.BASE_DIR, "out_chunks/")
        write_into_dataset(in_csv, out_chunks_dir)
        return Response({"Message": "Success"})


class CheckABIAvailability(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        address = request.query_params.get("address")
        result = 1 if contains_abi(address) else 0

        return Response({"result": result})
