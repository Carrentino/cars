from src.integrations.reviews import ReviewsClient


async def get_reviews_client() -> ReviewsClient:
    return ReviewsClient()
