from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from trust_scoring.db_writer import generate_and_store_score
from utils.basic_web3.address_classifier import is_contract


class GetTrustScore(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        address = request.query_params.get("address")

        if not is_contract(address):
            return Response({"status": "Failed", "Message": "The address provided is not a smart contract"})

        response_dict = generate_and_store_score(address)

        return Response(response_dict)
