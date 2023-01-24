from django.urls import path

from .apis import *

urlpatterns = [
    path('web3js_stats/', CheckWeb3JSStats.as_view(), name="webjs_stats")
]