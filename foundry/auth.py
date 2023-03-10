"""Utilities related to storing authentication credentials"""

from dataclasses import dataclass
from typing import Dict

from globus_sdk import TransferClient, AuthClient


@dataclass
class PubAuths:
    """Collection of the authorizers needed for publication

    Attributes:
        transfer_client: Client with credentials to perform transfers
        auth_client_openid: Client with permissions to get users IDs
        endpoint_auth_clients: Mapping between endpoint ID and client that can authorize access to it
    """

    transfer_client: TransferClient
    auth_client_openid: AuthClient
    endpoint_auth_clients: Dict[str, AuthClient]
