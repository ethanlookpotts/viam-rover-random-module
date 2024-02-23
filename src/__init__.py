"""
This file registers the model with the Python SDK.
"""

from viam.services.generic import Generic
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .random import random

Registry.register_resource_creator(Generic.SUBTYPE, random.MODEL, ResourceCreatorRegistration(random.new, random.validate))
