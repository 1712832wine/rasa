# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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


class ActionMedical(Action):

    def name(self) -> Text:
        return "action_medical"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']

        dispatcher.utter_message(text=text)
        return []

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

# def name_cap(text):
#     tarr = text.split()
#     for idx in range(len(tarr)):
#         tarr[idx] = tarr[idx].capitalize()
#     return ' '.join(tarr)


# class action_save_user_info(Action):
#     def name(self):
#         return 'action_save_user_info'

#     def run(self, dispatcher, tracker, domain):
#         # user_id = (tracker.current_state())["sender_id"]
#         # print(user_id)
#         # cust_name = next(tracker.get_latest_entity_values("cust_name"), None)
#         # cust_sex = next(tracker.get_latest_entity_values("cust_sex"), None)
#         # bot_position = "SHB"

#         # if (cust_sex is None):
#         #     cust_sex = "Quý khách"

#         # if (cust_sex == "anh") | (cust_sex == "chị"):
#         #     bot_position = "em"
#         # elif (cust_sex == "cô") | (cust_sex == "chú"):
#         #     bot_position = "cháu"
#         # else:
#         #     cust_sex = "Quý khách"
#         #     bot_position = "Sa"

#         if not cust_name:
#             return []

#         print(name_cap(cust_name))
#         return []
