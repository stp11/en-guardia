import os

from openai import OpenAI
from sqlmodel import select

from database import get_session
from logger import logger
from models import Episode
from repositories import CategoriesRepository, EpisodesRepository
from services import ClassificationService


def classify_episodes(batch_size: int = 50, max_total: int = None):
    """Classify episodes that haven't been classified yet, processing in batches."""  # noqa: E501

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    total_processed = 0
    total_successful = 0
    total_failed = 0

    logger.info(
        f"Starting classification with batch_size={batch_size}, max_total={max_total}"  # noqa: E501
    )

    while max_total is None or total_processed < max_total:
        with next(get_session()) as session:
            episodes_repository = EpisodesRepository(session)
            categories_repository = CategoriesRepository(session)
            classifier = ClassificationService(
                client, episodes_repository, categories_repository
            )

            # Calculate remaining episodes to process
            remaining = (
                None if max_total is None else max_total - total_processed
            )
            current_batch_size = (
                min(batch_size, remaining) if remaining else batch_size
            )

            unclassified = session.exec(
                select(Episode)
                .where(Episode.description.isnot(None))
                .where(~Episode.categories.any())
                .order_by(Episode.published_at.desc())
                .limit(current_batch_size)
            ).all()

            if not unclassified:
                logger.info("No more episodes to classify")
                break

            logger.info(f"Processing batch of {len(unclassified)} episodes")

            batch_successful = 0
            batch_failed = 0

            for episode in unclassified:
                try:
                    logger.info(
                        f"Classifying episode {episode.id}: {episode.title}"
                    )

                    classification = classifier.classify_episode(episode)
                    classifier.save_categories_to_episode(
                        episode, classification
                    )

                    batch_successful += 1
                    logger.info(
                        f"Successfully classified episode {episode.id}"
                    )

                except Exception as e:
                    logger.error(
                        f"Failed to classify episode {episode.id}: {e}"
                    )
                    batch_failed += 1
                    session.rollback()
                    continue

            try:
                session.commit()
                logger.info(
                    f"Committed batch: {batch_successful} successful, {batch_failed} failed"  # noqa: E501
                )
            except Exception as e:
                logger.error(f"Failed to commit batch: {e}")
                session.rollback()
                batch_failed += len(unclassified)
                batch_successful = 0

            total_successful += batch_successful
            total_failed += batch_failed
            total_processed += len(unclassified)

            logger.info(
                f"Progress: {total_processed} processed, {total_successful} successful, {total_failed} failed"  # noqa: E501
            )

            # If we processed fewer episodes than requested, we're done
            if len(unclassified) < current_batch_size:
                break

    logger.info(
        f"Classification complete: {total_successful} successful, {total_failed} failed, {total_processed} total"  # noqa: E501
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Classify episodes using OpenAI"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Number of episodes to process per batch (default: 50)",
    )
    parser.add_argument(
        "--max-total",
        type=int,
        default=None,
        help="Maximum total episodes to process (default: all)",
    )

    args = parser.parse_args()
    classify_episodes(batch_size=args.batch_size, max_total=args.max_total)
