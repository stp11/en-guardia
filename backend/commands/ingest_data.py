import json
from datetime import datetime

import requests
from database import get_session
from logger import logger
from models import Episode, IngestionPosition

BASE_URL = (
    "https://api.3cat.cat/audios?programaradio_id=944&ordre=-data_publicacio"
)


def parse_date(date_str):
    # API format: "09/09/2001 00:01:00"
    return datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")


def create_episode_from_data(data: dict) -> Episode:
    """Maps API data dictionary to an Episode object."""
    return Episode(
        id=data["id"],
        title=data.get("titol"),
        slug=data.get("nom_friendly"),
        description=data.get("entradeta"),
        published_at=(
            parse_date(data["data_publicacio"])
            if data.get("data_publicacio")
            else None
        ),
    )


def ingest_data():
    """
    Ingests episode data from a paginated API.

    Handles initial bulk ingestion and subsequent incremental updates.
    It processes pages until it finds an episode
    that has already been ingested, then stops.

    It uses the IngestionPosition model to track the last episode id
    and the total number of episodes ingested.
    """
    logger.info("Starting episode ingestion task.")

    with next(get_session()) as session:
        position = session.get(IngestionPosition, 1) or IngestionPosition(id=1)

        known_last_id = position.last_episode_id
        newest_id_this_run = None
        total_episodes_ingested = 0
        page = 1

        while True:
            url = f"{BASE_URL}&pagina={page}"
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                data = response.json().get("resposta", {})
                items = data.get("items", {}).get("item", [])

                if not items:
                    logger.info(f"No more items found on page {page}")
                    break

            except (
                requests.RequestException,
                json.JSONDecodeError,
                KeyError,
            ) as e:
                logger.error(f"Failed to fetch or parse page {page}: {e}")
                break  # Stop the process on any critical error

            episodes_to_add = []
            stop_processing = False

            for ep_data in items:
                if newest_id_this_run is None:
                    newest_id_this_run = ep_data["id"]

                if ep_data["id"] == known_last_id:
                    stop_processing = True
                    break

                episodes_to_add.append(create_episode_from_data(ep_data))

            if episodes_to_add:
                for episode in episodes_to_add:
                    session.merge(episode)
                total_episodes_ingested += len(episodes_to_add)

            if stop_processing:
                logger.info(
                    "Found last known episode. Ingestion is up-to-date."
                )
                break

            total_pages = data.get("paginacio", {}).get("total_pagines", 0)
            if page >= total_pages:
                logger.info("Reached the final page of the API.")
                break

            page += 1

        if newest_id_this_run and newest_id_this_run != known_last_id:
            position.last_episode_id = newest_id_this_run
            session.add(position)
            session.commit()
            logger.info(
                f"Successfully ingested {total_episodes_ingested} episodes. Last ID set to {newest_id_this_run}."  # noqa: E501
            )
        else:
            logger.info("No new episodes were ingested.")


if __name__ == "__main__":
    ingest_data()
