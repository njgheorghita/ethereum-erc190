from typing import Dict, ItemsView, List

from eth_utils import to_canonical_address
from web3 import Web3
from web3.eth import Contract

from ethpm.exceptions import ValidationError
from ethpm.utils.contract import validate_contract_name


class Deployments:
    """
    Deployment object to access instances of
    deployed contracts belonging to a package.
    """

    def __init__(
        self,
        deployment_data: Dict[str, Dict[str, str]],
        contract_factories: Dict[str, Contract],
        w3: Web3,
    ) -> None:
        self.deployment_data = deployment_data
        self.contract_factories = contract_factories
        self.w3 = w3

    def __getitem__(self, key: str) -> Dict[str, str]:
        return self.get(key)

    def __contains__(self, key: str) -> bool:
        return key in self.deployment_data

    def get(self, key: str) -> Dict[str, str]:
        self._validate_name_and_references(key)
        return self.deployment_data.get(key)

    def items(self) -> ItemsView[str, Dict[str, str]]:
        item_dict = {name: self.get(name) for name in self.deployment_data}
        return item_dict.items()

    def values(self) -> List[Dict[str, str]]:
        values = [self.get(name) for name in self.deployment_data]
        return values

    def get_deployment_instance(self, contract_name: str) -> None:
        """
        Fetches a contract instance belonging to deployment
        after validating contract name.
        """
        self._validate_name_and_references(contract_name)
        factory = self.contract_factories[contract_name]
        address = to_canonical_address(self.deployment_data[contract_name]["address"])
        contract_kwargs = {
            "abi": factory.abi,
            "bytecode": factory.bytecode,
            "bytecode_runtime": factory.bytecode_runtime,
        }
        return self.w3.eth.contract(address=address, **contract_kwargs)

    def _validate_name_and_references(self, name: str) -> None:
        validate_contract_name(name)

        if name not in self.deployment_data:
            raise KeyError("Contract name not found in deployment data")

        if name not in self.contract_factories:
            raise ValidationError("Contract name not found in contract_factories.")
