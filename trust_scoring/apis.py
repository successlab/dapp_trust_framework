from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from trust_scoring.db_writer import generate_and_store_score


class GetTrustScore(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        address = request.query_params.get("address")
        response_dict = generate_and_store_score(address)

        return Response(response_dict)
