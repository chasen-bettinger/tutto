from typing import Any, Callable, Dict, Optional, Type
from abc import ABCMeta, abstractmethod
from signature import Signature
from create_signature import create_signature


class BaseSigner(metaclass=ABCMeta):
    @abstractmethod
    def sign(self, payload: bytes) -> Signature:
        """Signs a given payload by the key assigned to the Signer instance.

        Arguments:
            payload: The bytes to be signed.

        Returns:
            Returns a "Signature" class instance.
        """
        raise NotImplementedError


class Signer(BaseSigner):
    def __init__(self, key_dict: Dict):
        self.key_dict = key_dict

    def sign(self, payload: bytes) -> Signature:
        sig_dict = create_signature(self.key_dict, payload)
        return Signature.from_dict(sig_dict)
