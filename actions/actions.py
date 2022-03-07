# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
import json
import re
import string
from sentence_transformers import SentenceTransformer, util

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

bert = SentenceTransformer('sentence-transformers/multi-qa-MiniLM-L6-cos-v1')
print('init')


class ActionMedical(Action):

    def name(self) -> Text:

        return "action_medical"

    def normalize_text(self, text):
        text = re.sub("&\w+;", "", text)  # remove punctuation encoding
        text = re.sub("&#\d+;", "", text)

        text = re.sub("gt", "", text)  # remove punctuation encoding
        text = re.sub("em", "", text)
        text = re.sub("lt", "", text)

        text = text.lower()  # lowercase
        text = text.replace(r"http\S+", "URL")  # remove URL addresses
        text = text.translate(str.maketrans(
            '', '', string.punctuation))  # remove punctuations
        text = re.sub(r"\s{2,}", " ", text)  # replace >= 2 spaces
        text = re.sub(r"^\s", "", text)  # remove starting spaces
        text = re.sub(r"\s$", "", text)  # remove ending spaces

        return text

    def compare(self, input, data_src):
        # encode  1
        emb_1 = bert.encode(input)
        # encode  2
        emb_2 = bert.encode(data_src)
        # get similarity score
        scores = util.dot_score(emb_1, emb_2)
        return scores

    def get_questions(self, text):
        questions = []
        pattern = re.compile(r'- -.*\?')
        matches = pattern.finditer(text)
        for match in matches:
            s = match.group(0)
            s = self.normalize_text(s)
            questions.append(s)
        return questions

    def get_answers(self, text):
        answers = []
        pattern = re.compile(r'  - .*\n')
        matches = pattern.finditer(text)
        for match in matches:
            s = match.group(0)
            s = self.normalize_text(s)
            answers.append(s)
        return answers

    def get_file(self, x):
        switcher = {
            'béo phì': '__beo_phi.yml',
            'covid': '__covid.yml',
            'da liễu': '__da_lieu.yml',
            'đau mắt đỏ': '__dau_mat_do.yml',
            'đau thần kinh tọa': '__dau_than_kinh_toa.yml',
            'hạ canxi máu': '__ha_canxi_mau.yml',
            'lao phổi': '__lao_phoi.yml',
            'mụn trứng cá': '__mun_trung_ca.yml',
            'quai bị, sâu răng': '__quai_bi_sau_rang.yml',
            'tai-mũi-họng': '__tai_mui_hong.yml',
            'tay-chân-miệng': '__tay_chan_mieng.yml',
            'thận': '__than.yml',
            'thủy đậu': '__thuy_dau.yml',
            'tim mạch': '__tim_mach.yml',
            'viêm đường hô hấp': '__viem_duong_ho_hap.yml',
            'viêm xoang': '__viem_xoang.yml',
        }
        return switcher.get(x, "nothing.yml")

    def get_answer(self, input, filename):
        with open(filename, encoding='utf-8') as f:
            text = f.read()
        data_src = self.get_questions(text)
        data_dest = self.get_answers(text)
        scores = self.compare(input, data_src)
        max_value = max(scores[0])
        max_index = scores[0].tolist().index(max_value)
        return data_dest[max_index]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get intent
        intent = tracker.latest_message.get("intent").get("name")
        # get message input
        message = tracker.latest_message.get("text")
        # get filename
        filename = './data/medical/'+self.get_file(intent)
        # get answer
        answer = self.get_answer(message, filename)
        dispatcher.utter_message(text=answer)
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
