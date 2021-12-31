# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.events import UserUtteranceReverted
from rasa_core_sdk.events import AllSlotsReset
from rasa_core_sdk.events import Restarted

import requests
import json
from bs4 import BeautifulSoup
from pyvi import ViTokenizer, ViPosTagger


def name_cap(text):
    tarr = text.split()
    for idx in range(len(tarr)):
        tarr[idx] = tarr[idx].capitalize()
    return ' '.join(tarr)


class action_save_cust_info(Action):
    def name(self):
        return 'action_save_cust_info'

    def run(self, dispatcher, tracker, domain):
        user_id = (tracker.current_state())["sender_id"]
        print(user_id)
        user_name = next(tracker.get_latest_entity_values("user_name"), None)
        user_gender = next(
            tracker.get_latest_entity_values("user_gender"), None)
        bot_position = "SHB"

        if (user_gender is None):
            user_gender = "Quý khách"

        if (user_gender == "anh") | (user_gender == "chị"):
            bot_position = "em"
        elif (user_gender == "cô") | (user_gender == "chú"):
            bot_position = "cháu"
        else:
            user_gender = "Quý khách"
            bot_position = "Sa"

        if not user_name:
            # dispatcher.utter_template("utter_greet_name",tracker)
            return []

        print(name_cap(user_name))
        return [SlotSet('user_name', " "+name_cap(user_name)), SlotSet('user_gender', name_cap(user_gender)), SlotSet('bot_position', name_cap(bot_position))]


class action_save_mobile_no(Action):
    def name(self):
        return 'action_save_mobile_no'

    def run(self, dispatcher, tracker, domain):
        user_id = (tracker.current_state())["sender_id"]
        print(user_id)
        mobile_no = next(tracker.get_latest_entity_values("inp_number"), None)

        if not mobile_no:
            return [UserUtteranceReverted()]

        mobile_no = mobile_no.replace(" ", "")
        #print (user_name)
        return [SlotSet('mobile_no', mobile_no)]


class action_reset_slot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("transfer_nick", None), SlotSet("transfer_amount", None), SlotSet("transfer_amount_unit", None)]
