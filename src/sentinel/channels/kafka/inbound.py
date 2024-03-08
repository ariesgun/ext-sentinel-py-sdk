import logging

from aiokafka.structs import ConsumerRecord
from aiokafka import AIOKafkaConsumer as KafkaConsumer

from sentinel.channels.kafka.common import KafkaChannel


logger = logging.getLogger(__name__)


class InboundKafkaChannel(KafkaChannel):
    """
    Inbound Kafka Channel
    """

    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        """
        Inbound Kafka Channel
        """
        super().__init__(name, record_type, **kwargs)
        # Setting default values for auto_offset_reset
        self.config["auto_offset_reset"] = self.config.get("auto_offset_reset", "latest")

    async def run(self):
        """
        Run Inbound Kafka Channel
        """
        logger.info(f"{self.name} -> Subscribing to Kafka topics: {self.topics}")
        self.consumer = KafkaConsumer(*self.topics, **self.config)

        logger.info(f"{self.name} -> Starting consuming messages fromn Kafka channel: {self.name}")
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                await self.on_message(msg)
        finally:
            await self.consumer.stop()

    async def on_message(self, message: ConsumerRecord) -> None:
        """
        Handle consumer message
        """
        pass
