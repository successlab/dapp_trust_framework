from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from trust_scoring.db_writer import find_links_and_store_in_db
from utils.trust_scoring.data_persistance import write_features_df_into_db
from utils.trust_scoring.feature_extractor import get_features_df
from utils.trust_scoring.ml_model_runner import get_prob_trust_score


class GetTrustScore(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        address = request.query_params.get("address")

        contract_attribs_df = get_features_df(address)

        prob_score = get_prob_trust_score(contract_attribs_df)

        write_features_df_into_db(
            address,
            contract_attribs_df,
            trust_score=prob_score,
        )

        response_dict = {
            "trust_score": prob_score,
            "contract_attributes": contract_attribs_df.iloc[0].to_dict(),
        }

        code_contracts = find_links_and_store_in_db(address)
        response_dict["links"] = code_contracts

        return Response(response_dict)
