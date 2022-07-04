from django.db import models

from contract_relations.submodels.dapp_models import DApp
from contract_relations.submodels.people_models import Person


class Contract(models.Model):
    address = models.CharField(max_length=1024)
    dapp = models.ForeignKey(DApp, on_delete=models.CASCADE)
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
    parent = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="parent")
    child = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="child")

    # This can be: "Import" or "Mention"
    # Import - Means that the child (contract in focus) is using the parent to be able to run
    # Mention - The parent (contract in focus) address is mentioned in the child contract
    relation_type = models.CharField(max_length=120)
