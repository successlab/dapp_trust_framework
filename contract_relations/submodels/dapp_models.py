from django.db import models

from contract_relations.submodels.people_models import Person


class DApp(models.Model):
    name = models.CharField(max_length=250, null=True, default=None)
    website_url = models.CharField(max_length=1250, null=True, default=None)
    github_url = models.CharField(max_length=1250, null=True, default=None)


class DAppAssociate(models.Model):
    dapp = models.ForeignKey(DApp, on_delete=models.CASCADE)
    associate = models.ForeignKey(Person, on_delete=models.CASCADE)

    # This can be: "Developer", "Deployer", "Owner", or "Listed"
    association_type = models.CharField(max_length=120)
