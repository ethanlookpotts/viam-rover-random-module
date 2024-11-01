import asyncio
from typing import ClassVar, Mapping, Optional, Sequence

from typing_extensions import Self
from viam.module.module import Module
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.services.generic import Generic
from viam.components.base import Base
from threading import Thread, Event
from viam import logging
from viam.utils import ValueTypes
from random import random


LOGGER = logging.getLogger(__name__)

class Randomrover(Generic, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("ethanlook", "randomrover"), "randomrover"
    )
    thread = None
    event = Event()

    base: Base

    sleep_s = 1
    distance_mm = 500
    velocity_mm_s = 100
    angle_deg = 360
    velocity_deg_s = 90

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Generic service.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Sequence[str]: A list of implicit dependencies
        """
        if "base" not in config.attributes.fields:
            raise Exception('base is required for randomrover')
        return []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """
        if len(dependencies.values()) == 0:
            raise Exception("A base is a required dependency. Make sure a base is added as a dependency and is of the Base type.")

        base_dep = next(iter(dependencies.values()))
        if base_dep is None or base_dep.SUBTYPE != Base.SUBTYPE:
            raise Exception("A base is a required dependency. Make sure a base is added as a dependency and is of the Base type.")
        self.base = base_dep

        if "sleep_s" in config.attributes.fields:
            self.sleep_s = int(config.attributes.fields["sleep_s"].number_value)

        if "distance_mm" in config.attributes.fields:
            self.distance_mm = int(config.attributes.fields["distance_mm"].number_value)

        if "velocity_mm_s" in config.attributes.fields:
            self.velocity_mm_s = int(config.attributes.fields["velocity_mm_s"].number_value)

        if "angle_deg" in config.attributes.fields:
            self.angle_deg = int(config.attributes.fields["angle_deg"].number_value)

        if "velocity_deg_s" in config.attributes.fields:
            self.velocity_deg_s = int(config.attributes.fields["velocity_deg_s"].number_value)

        return super().reconfigure(config, dependencies)

    def thread_run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.looper())

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.event.clear()
            self.thread = Thread(target=self.thread_run)
            self.thread.start()

    def stop(self):
        if self.thread is not None and self.event is not None:
            self.event.set()
            self.thread.join()
            self.thread = None

    async def looper(self):
        while not self.event.is_set():
            await self.do_loop()
            await asyncio.sleep(0)  # Yield control to the event loop

    async def do_loop(self):
        distance_mm = int((2 * random() - 1) * self.distance_mm)
        LOGGER.info("moving forward")
        await self.base.move_straight(distance_mm, self.velocity_mm_s)
        await asyncio.sleep(self.sleep_s)
        LOGGER.info("moving backward")
        await self.base.move_straight(-distance_mm, self.velocity_mm_s)
        await asyncio.sleep(self.sleep_s)
        LOGGER.info("spinning")
        await self.base.spin(int((2 * random() - 1) * self.angle_deg), self.velocity_deg_s)
        await asyncio.sleep(self.sleep_s)

    async def do_command(self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None, **kwargs) -> Mapping[str, ValueTypes]:
        LOGGER.info("do_command called")
        result = {key: False for key in command.keys()}
        for name, _ in command.items():
            if name == 'start':
                self.start()
                result[name] = True
            if name == 'stop':
                self.stop()
                result[name] = True
        return result

    def __del__(self):
        self.stop()


if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())

