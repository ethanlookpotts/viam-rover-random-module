import asyncio
import sys
from viam import logging

from viam.module.module import Module
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.components.generic import Generic

from randomrover import RandomRoverServer

LOGGER = logging.getLogger(__name__)
sys.path.append("..")


Registry.register_resource_creator(Generic.SUBTYPE, RandomRoverServer.MODEL, ResourceCreatorRegistration(RandomRoverServer.new, RandomRoverServer.validate_config))

async def main():
    LOGGER.info("Starting randomrover module...")
    module = Module.from_args()

    module.add_model_from_registry(Generic.SUBTYPE, RandomRoverServer.MODEL)
    await module.start()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Need socket path as command line argument")

    asyncio.run(main())
