from helpers.depends.db_session import get_db_session_context
from helpers.kafka.consumer import KafkaConsumerTopicsListeners

from src.kafka.db_client import make_db_client
from src.kafka.depends.services import get_car_service
from src.kafka.listings.schemas import UpdateScore
from src.settings import get_settings

listing_listener = KafkaConsumerTopicsListeners()


@listing_listener.add(get_settings().kafka.topic_car_score, UpdateScore)
async def update_score(
    message: UpdateScore,
) -> None:
    async with get_db_session_context(make_db_client()) as session:
        car_service = await get_car_service(session)
        await car_service.update_score(message.car_id, message.score)
