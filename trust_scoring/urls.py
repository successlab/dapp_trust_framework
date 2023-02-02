from django.urls import path
from .apis import GetTrustScore

urlpatterns = [
	path("get_trust_score/", GetTrustScore.as_view(), name="get_trust_score"),
]
