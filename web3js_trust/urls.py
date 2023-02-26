from django.urls import path

from .apis import *

urlpatterns = [
    path('web3js_stats/', CheckWeb3JSStats.as_view(), name="webjs_stats"),
    path('extract_data/', ExtractData.as_view(), name="extract_data"),
    path('abi_availability/', CheckABIAvailability.as_view(), name="abi-availability"),
]