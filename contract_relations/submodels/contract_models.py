from django.db import models

from contract_relations.submodels.dapp_models import DApp
from contract_relations.submodels.people_models import Person


class Address(models.Model):
    eth_address = models.CharField(max_length=1024, null=True, default=None)

    # Contract, EOA, or self-destructed contract
    type = models.CharField(max_length=50, null=True, default=None)


class Contract(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    dapp = models.ForeignKey(DApp, on_delete=models.CASCADE, null=True, default=None)
    github_repo = models.CharField(max_length=2048, null=True, default=None)
    code_location_url = models.CharField(max_length=2048, null=True, default=None)


# TODO: Check if we need to collect the individual contract deployer/owner info
class ContractAssociation(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    # This can be: "Developer", "Deployer", or "Owner"
    # Unlike DApp association, this cannot be "Listed"
    association_type = models.CharField(max_length=120)


class ContractRelation(models.Model):
    parent = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="parent"
    )
    child = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="child")

    # This can be: "Import" or "Mention"
    # CodeMention - Part of the logic
    # AttribVal - A value within the storage locations of the parent
    relation_type = models.CharField(max_length=120)
