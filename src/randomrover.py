from typing import ClassVar, Mapping

from typing_extensions import Self

from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model
from viam.components.generic import Generic
from viam import logging

LOGGER = logging.getLogger(__name__)

class RandomRoverServer(Generic):
    MODEL: ClassVar[Model] = Model.from_string("ethanlook:rover:random")

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        randomrover = cls(config.name)
        randomrover.reconfigure(config, dependencies)
        return randomrover
