from ner_v2.detectors.base_detector import BaseDetector
from ner_v2.detectors.numeral.number.number_detection import NumberDetector
from language_utilities.constant import ENGLISH_LANG
import re


class PhoneDetector(BaseDetector):

    def __init__(self, entity_name, language=ENGLISH_LANG):
        self._supported_languages = NumberDetector.get_supported_languages()
        super(PhoneDetector, self).__init__(language)
        self.language = language
        self.number_detector = NumberDetector(entity_name=entity_name, language=self.language)
        self.entity_name = entity_name
        self.text = ''
        self.tagged_text = ''
        self.processed_text = ''
        self.number = []
        self.original_number_text = []
        self.tag = '__' + self.entity_name + '__'

    @property
    def supported_languages(self):
        return self._supported_languages

    def get_number(self):
        self.number_detector.set_min_max_digits(min_digit=8, max_digit=14)
        self.number_detector.detect_entity(text=self.text)
        number_list, original_number_list = self.number_detector.detect_entity(text=self.text)
        return number_list, original_number_list

    def detect_entity(self, text, **kwargs):
        self.text = text
        # number_list, original_list = self.get_number()
        return self.get_phone_number()

    def get_phone_number(self):
        phone_number_original_list = self.get_number_regex()
        phone_number_original_list = [p[0] for p in phone_number_original_list]
        phone_number_list = [self.clean_phone_number(p) for p in phone_number_original_list]
        return phone_number_list, phone_number_original_list

    def clean_phone_number(self, number):
        clean_regex = re.compile('[\+()\sext]+')
        return clean_regex.sub(string=number, repl='')

    def get_number_regex(self):
        phone_number_regex = re.compile(
            r'((?:\(?\+(\d{1,2})\)?[\s\-\.]*)?((?=[\-\d()\s\.]{9,16}'
            r'(?:\s*e?xt?\.?\s*(?:\d{1,20}))?(?:[^\d]+|$))'
            r'(?:[\d(]{1,20}(?:[\-)\s\.]*\d{1,20}){0,20}){1,20})'
            r'(?:\s*e?xt?\.?\s*(\d{1,20}))?)')
        phone_number_list = phone_number_regex.findall(self.text)
        return phone_number_list