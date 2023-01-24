from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from utils.basic_web3.address_classifier import *
from utils.github_crawler import get_github_all_code_search_results, check_web3js_usage_parallel


class CheckWeb3JSStats(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        in_data = request.data
        search_address = in_data["address"]

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
        }

        return Response(out_data)