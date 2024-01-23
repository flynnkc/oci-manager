#!/bin/python3.11

import logging

from modules.config import Config
from oci import pagination
from oci.resource_search import ResourceSearchClient
from oci.resource_search.models import StructuredSearchDetails
from oci.resource_search.models import ResourceSummaryCollection

class Search:

    search_types = [
        "instance",
        "instancepool",
        "dbsystem",
        "vmcluster",
        "cloudexadatainfrastructure",
        "cloudvmcluster",
        "autonomousdatabase",
        "odainstance",
        "analyticsinstance",
        "integrationinstance",
        "loadbalancer",
        "goldengatedeployment",
        "disworkspace",
        "visualbuilderinstance"
        ]

    def __init__(self, config: Config):
        self.log = logging.getLogger(f'{__name__}.Search')
        self.log.info(f'Initializing Search Object {self}')
        self.profile = config.profile
        self.signer = config.signer
        self.tag = config.args.tag
        self.compartment = config.args.compartment
        self.exclude = config.args.exclude


    def query(self) -> ResourceSummaryCollection:
        self.client = ResourceSearchClient(self.profile, signer=self.signer)
        self.log.debug(f'Initialized Search client: {self.client}')

        # Create structured search with parameters
        comma = ", "
        query = (f"query {comma.join(self.search_types)} resources where"
                 f" (definedTags.namespace = '{self.tag}')")
        query += f" && compartmentId  = '{self.compartment}'" if \
            self.compartment else ""
        query += f" && compartmentId  != '{self.exclude}'" if \
            self.exclude else ""
        self.log.debug(f'Search query: {query}')

        details = StructuredSearchDetails(query=query)
        response = pagination.list_call_get_all_results(self.client.search_resources, details)
        self.log.debug(f'Response Headers: {response.headers}\n\t'
                       f'Request ID: {response.request_id}\n\tRequest: '
                       f'{response.request}\n\tStatus: {response.status}')
        self.log.debug(f'Search Response subset: {response.data[0:2]}')
        self.log.info(f'Found {len(response.data)} Resources')
        
        return response.data