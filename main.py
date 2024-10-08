import asyncio

import os

from rabbitmq.rabbitmq import RabbitMQConsumer, RabbitMQProducer
from rabbitmq.constants import (REACTIVATION_1_QUEUE_NAME, REACTIVATION_2_QUEUE_NAME, REACTIVATION_3_QUEUE_NAME,
                                PARTNER_INSTALLED_APP_QUEUE_NAME, PARTNER_WAITING_QUEUE_NAME,
                                PARTNER_ANSWERED_QUEUE_NAME, PARTNER_NOT_INSTALLED_QUEUE_NAME, LOST_ONBO_QUEUE_NAME,
                                LOST_FIRST_QUESTION_QUEUE_NAME, STREAK_1_QUEUE_NAME, ANNIVERSARY_QUEUE_NAME,
                                QUESTION_REACTION_QUEUE_NAME, PARTNER_IS_WAITING_CARD_GAME_QUEUE_NAME,
                                PARTNER_ANSWERED_CARD_GAME_QUEUE_NAME, PARTNER_SENT_REACTION_CARD_GAME_QUEUE_NAME,
                                PARTNER_COMMENTED_CARD_GAME_QUEUE_NAME,
                                PARTNER_NUDGED_ABOUT_RELATIONSHIP_CHECKUP_QUEUE_NAME,
                                PARTNER_COMPLETED_CHECKUP_QUEUE_NAME, BOTH_PARTNERS_COMPLETED_CHECKUP_QUEUE_NAME,
                                PARTNER_STARTED_CHECKUP_QUEUE_NAME, PARTNER_INSTALLED_WIDGET_QUEUE_NAME,
                                PARTNER_COMPLETED_SETUP_QUEUE_NAME, PARTNER_SENT_PIC_QUEUE_NAME,
                                PARTNER_VIEWED_PIC_QUEUE_NAME, SEND_PIC_REMINDER_QUEUE_NAME,
                                PARTNER_SENT_PIC_LIVE_ACTIVITY_QUEUE_NAME, PARTNER_SENT_PIC_LIVE_ACTIVITY_END_QUEUE_NAME,
                                SEND_LIVE_ACTIVITY_PUSH_QUEUE_NAME, PARTNER_SET_MOOD_QUEUE_NAME)

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
from processors.partner_sent_reaction_card_game import partner_sent_reaction_card_game_process
from processors.partner_commented_card_game import partner_commented_card_game_process
from processors.partner_nudged_relationship_checkup import partner_nudged_about_checkup_process
from processors.both_partners_completed_checkup import both_partners_completed_checkup
from processors.patner_completed_checkup import partner_completed_checkup
from processors.partner_started_checkup import partner_started_checkup
from processors.partner_completed_setup import partner_completed_setup
from processors.partner_installed_widget import partner_installed_widget_process
from processors.partner_sent_pic import (partner_sent_pic_process, partner_sent_pic_live_activity_process,
                                         partner_sent_pic_live_activity_end_process)
from processors.partner_viewed_pic import partner_view_pic_process
from processors.send_pic_reminder import send_pic_reminder_process
from processors.update_live_activity import update_live_activity_process
from processors.partner_set_mood import partner_set_mood_proccess

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
        PARTNER_IS_WAITING_CARD_GAME_QUEUE_NAME: partner_is_waiting_card_game_process,
        PARTNER_SENT_REACTION_CARD_GAME_QUEUE_NAME: partner_sent_reaction_card_game_process,
        PARTNER_COMMENTED_CARD_GAME_QUEUE_NAME: partner_commented_card_game_process,
        PARTNER_NUDGED_ABOUT_RELATIONSHIP_CHECKUP_QUEUE_NAME: partner_nudged_about_checkup_process,
        PARTNER_COMPLETED_CHECKUP_QUEUE_NAME: partner_completed_checkup,
        BOTH_PARTNERS_COMPLETED_CHECKUP_QUEUE_NAME: both_partners_completed_checkup,
        PARTNER_STARTED_CHECKUP_QUEUE_NAME: partner_started_checkup,
        PARTNER_COMPLETED_SETUP_QUEUE_NAME: partner_completed_setup,
        PARTNER_INSTALLED_WIDGET_QUEUE_NAME: partner_installed_widget_process,
        PARTNER_SENT_PIC_QUEUE_NAME: partner_sent_pic_process,
        PARTNER_VIEWED_PIC_QUEUE_NAME: partner_view_pic_process,
        SEND_PIC_REMINDER_QUEUE_NAME: send_pic_reminder_process,
        PARTNER_SENT_PIC_LIVE_ACTIVITY_QUEUE_NAME: partner_sent_pic_live_activity_process,
        PARTNER_SENT_PIC_LIVE_ACTIVITY_END_QUEUE_NAME: partner_sent_pic_live_activity_end_process,
        SEND_LIVE_ACTIVITY_PUSH_QUEUE_NAME: update_live_activity_process,
        PARTNER_SET_MOOD_QUEUE_NAME: partner_set_mood_proccess
    }

    consumer = RabbitMQConsumer(rabbitmq_url=rabbitmq_url, queue_callbacks=queue_callbacks)
    await consumer.connect()
    await consumer.consume()

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
