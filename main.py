import asyncio

import os

from rabbitmq.rabbitmq import RabbitMQConsumer, RabbitMQProducer
from rabbitmq.constants import (REACTIVATION_1_QUEUE_NAME, REACTIVATION_2_QUEUE_NAME, REACTIVATION_3_QUEUE_NAME,
                                PARTNER_INSTALLED_APP_QUEUE_NAME, PARTNER_WAITING_QUEUE_NAME,
                                PARTNER_ANSWERED_QUEUE_NAME, PARTNER_NOT_INSTALLED_QUEUE_NAME, LOST_ONBO_QUEUE_NAME,
                                LOST_FIRST_QUESTION_QUEUE_NAME, STREAK_1_QUEUE_NAME, ANNIVERSARY_QUEUE_NAME,
                                QUESTION_REACTION_QUEUE_NAME, PARTNER_IS_WAITING_CARD_GAME_QUEUE_NAME,
                                PARTNER_ANSWERED_CARD_GAME_QUEUE_NAME)

from processors.reactivation import reactivation_1_process, reactivation_2_process, reactivation_3_process
from processors.lost_onbo import lost_onbo_process
from processors.partner_answered import partner_answered_process
from processors.partner_installed_app import partner_installed_app_process
from processors.partner_is_waiting import partner_is_waiting_process
from processors.partner_not_installed import partner_not_installed_process
from processors.lost_first_question import lost_first_question_process
from processors.streak_1 import streak_1_process
from processors.anniversary import anniversary_process
from processors.question_reaction import partner_question_reaction_process
from processors.partner_answered_card_game import partner_answered_card_game_process
from processors.partner_is_waiting_card_game import partner_is_waiting_card_game_process

from dotenv import load_dotenv


async def main():
    rabbitmq_url = os.getenv("RABBITMQ_URL")

    print(rabbitmq_url)

    _ = RabbitMQProducer(rabbitmq_url=rabbitmq_url)

    queue_callbacks = {
        REACTIVATION_1_QUEUE_NAME: reactivation_1_process,
        REACTIVATION_2_QUEUE_NAME: reactivation_2_process,
        REACTIVATION_3_QUEUE_NAME: reactivation_3_process,
        LOST_ONBO_QUEUE_NAME: lost_onbo_process,
        PARTNER_ANSWERED_QUEUE_NAME: partner_answered_process,
        PARTNER_INSTALLED_APP_QUEUE_NAME: partner_installed_app_process,
        PARTNER_WAITING_QUEUE_NAME: partner_is_waiting_process,
        PARTNER_NOT_INSTALLED_QUEUE_NAME: partner_not_installed_process,
        LOST_FIRST_QUESTION_QUEUE_NAME: lost_first_question_process,
        STREAK_1_QUEUE_NAME: streak_1_process,
        ANNIVERSARY_QUEUE_NAME: anniversary_process,
        QUESTION_REACTION_QUEUE_NAME: partner_question_reaction_process,
        PARTNER_ANSWERED_CARD_GAME_QUEUE_NAME: partner_answered_card_game_process,
        PARTNER_IS_WAITING_CARD_GAME_QUEUE_NAME: partner_is_waiting_card_game_process
    }

    consumer = RabbitMQConsumer(rabbitmq_url=rabbitmq_url, queue_callbacks=queue_callbacks)
    await consumer.connect()
    await consumer.consume()

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
