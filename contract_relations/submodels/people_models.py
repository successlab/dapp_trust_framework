from django.db import models


class Person(models.Model):
    # The person can be anonymous and can only be identified by the default ID
    name = models.CharField(max_length=250, null=True, default=None)
    github_profile = models.CharField(max_length=1024, null=True, default=None)


class Wallet(models.Model):
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    address = models.CharField(max_length=1024)
    chain_name = models.CharField(max_length=250, default="Ethereum")
