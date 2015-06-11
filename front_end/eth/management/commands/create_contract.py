# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.conf import settings

from eth.contracts import contract_code, eth_client


class Command(BaseCommand):
    help = "Creates a new ethereum contract. Keep in mind that this will cost `ether`."

    def handle(self, *args, **options):
        address = eth_client.create_contract(contract_code, settings.ETHEREUM_CONTRACT_VALUE)
        print(address)
