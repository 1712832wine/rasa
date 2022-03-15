# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
from rasa_sdk.types import DomainDict
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
import re
import string
from sentence_transformers import SentenceTransformer, util
import sqlite3
from datetime import datetime
import hashlib
from rasa_sdk.events import AllSlotsReset, SlotSet
from underthesea import word_tokenize
from nltk.corpus import stopwords

bert = SentenceTransformer('sentence-transformers/multi-qa-MiniLM-L6-cos-v1')


class ActionMedical(Action):

    def name(self) -> Text:
        return "action_medical"

    def remove_numbers(self, text):
        result = re.sub(r'\d+', '', text)
        return result

    def remove_whitespace(self, text):
        return " ".join(text.split())

    def remove_punctuation(self, text):
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def remove_stopwords(self, text):
        stop_words = set(stopwords.words("vietnamese"))
        word_tokens = word_tokenize(text, format='text').split(' ')
        filtered_text = [word.replace('_', ' ')
                         for word in word_tokens if word not in stop_words]
        if filtered_text:
            return ' '.join(filtered_text)
        else:
            return text

    def preprocess(self, text):
        text = text.strip().lower().rstrip('\n')
        text = self.remove_numbers(text)
        text = self.remove_whitespace(text)
        text = self.remove_punctuation(text)
        # text = self.remove_stopwords(text)
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
        pattern = re.compile(r'- -.*\n')
        matches = pattern.finditer(text)
        for match in matches:
            s = match.group(0)[4:]
            s = self.preprocess(s)
            questions.append(s)
        return questions

    def get_answers(self, text):
        answers = []
        pattern = re.compile(r'  - .*\n')
        matches = pattern.finditer(text)
        for match in matches:
            s = match.group(0)[4:]
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
        return switcher.get(x, "nothing")

    def get_answer(self, input, filename):
        with open(filename, encoding='utf-8') as f:
            text = f.read()
        data_src = self.get_questions(text)
        data_dest = self.get_answers(text)
        scores = self.compare(self.preprocess(input), data_src)
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
        temp = self.get_file(intent)

        if temp != 'nothing':
            # get filename
            filename = './data/medical/' + temp
            # get answer
            answer = self.get_answer(message, filename)
            dispatcher.utter_message(text=answer)
        else:
            dispatcher.utter_message(
                text='Xin lỗi mình không biết trả lời câu này')
        return []

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------


class ActionGetData(Action):

    def name(self) -> Text:
        return "action_get_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Define what the form has to do after all required slots are filled"""

        password = tracker.get_slot("password")
        con = sqlite3.connect('database.sqlite3')
        cur = con.cursor()
        password_hashed = hashlib.md5(password.encode()).hexdigest()
        cur.execute(
            'SELECT * FROM medical_records WHERE password=:password', {'password': password_hashed})
        result = cur.fetchall()
        con.close()
        if len(result) > 0:
            dispatcher.utter_message(
                text=f"Hồ sơ của bạn là: [{result[0][0]}] - [{result[0][1]}] - [{result[0][2]}] - [{json.loads(result[0][4])}] - [{result[0][5]}]!")
        else:
            dispatcher.utter_message(
                text=f"Không có hồ sơ của bạn trong danh sách!")
        return [SlotSet("password", None)]


class ActionSubmit(Action):

    def name(self) -> Text:
        return "action_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Define what the form has to do after all required slots are filled"""

        user_name = tracker.get_slot("user_name")
        user_gender = tracker.get_slot("user_gender")
        user_age = tracker.get_slot("user_age")
        password = tracker.get_slot("password")
        note = tracker.get_slot("note")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        # hashpassword
        password_hashed = hashlib.md5(password.encode()).hexdigest()
        # gender
        man = ['anh', 'chú']
        woman = ['chị', 'cô', 'dì']
        if user_gender in man:
            user_gender = 'nam'
        if user_gender in woman:
            user_gender = 'nữ'
        # save to db
        con = sqlite3.connect('database.sqlite3')
        cur = con.cursor()
        cur.execute("INSERT INTO medical_records VALUES (?,?,?,?,?,?)", (user_name, user_gender, user_age,
                                                                         password_hashed, json.dumps(note), dt_string))
        con.commit()
        con.close()

        # reset all slot

        dispatcher.utter_message(
            text=f"Hồ sơ đã hoàn thành, lưu các thông tin sau: [{user_name}] - [{user_gender}] - [{user_age}] - [{password}] - [{note}]")
        return [AllSlotsReset()]


class ValidateGetDataForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_get_data_form"

    @staticmethod
    def password_db() -> List[Text]:
        con = sqlite3.connect('database.sqlite3')
        cur = con.cursor()
        cur.execute(
            'SELECT password FROM medical_records')
        result = cur.fetchall()
        con.close()
        return result

    def validate_password(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if slot_value:
            return {'password': slot_value}
        else:
            return {'password': None}


class ValidateDiagnoseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_diagnose_form"

    def validate_user_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if slot_value:
            return {"user_name": slot_value}
        else:
            return {"user_name": None}

    def validate_user_gender(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if slot_value:
            return {"user_gender": slot_value}
        else:
            return {"user_gender": None}

    def validate_user_age(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if slot_value:
            return {"user_age": slot_value}
        else:
            return {"user_age": None}

    def validate_password(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if slot_value:
            password_hashed = hashlib.md5(slot_value.encode()).hexdigest()
            # save to db
            con = sqlite3.connect('database.sqlite3')
            cur = con.cursor()
            cur.execute("SELECT password FROM medical_records")
            result = cur.fetchall()
            con.commit()
            con.close()

            for password in result:
                if password[0] == password_hashed:
                    return {"password": None}
            return {"password": slot_value}
        else:
            return {"password": None}

    def validate_note(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if slot_value:
            return {"note": slot_value}
        else:
            return {"note": None}
