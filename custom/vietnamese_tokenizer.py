from __future__ import annotations
from typing import Any, Dict, List, Optional, Text

import regex

import rasa.shared.utils.io
import rasa.utils.io

from rasa.engine.graph import ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.constants import DOCS_URL_COMPONENTS
from rasa.shared.nlu.training_data.message import Message
from underthesea import word_tokenize
import re
import string


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER, is_trainable=False
)
class VietnameseTokenizer(Tokenizer):
    """Creates features for entity extraction."""

    @staticmethod
    def supported_languages() -> Optional[List[Text]]:
        """The languages that are supported."""
        return ["vi"]

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns the component's default config."""
        return {
            # Flag to check whether to split intents
            "intent_tokenization_flag": False,
            # Symbol on which intent should be split
            "intent_split_symbol": "_",
            # Regular expression to detect tokens
            "token_pattern": None,
        }

    def __init__(self, config: Dict[Text, Any]) -> None:
        """Initialize the tokenizer."""
        super().__init__(config)
        self.emoji_pattern = rasa.utils.io.get_emoji_regex()

        if "case_sensitive" in self._config:
            rasa.shared.utils.io.raise_warning(
                "The option 'case_sensitive' was moved from the tokenizers to the "
                "featurizers.",
                docs=DOCS_URL_COMPONENTS,
            )

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> VietnameseTokenizer:
        """Creates a new component (see parent class for full docstring)."""
        # Path to the dictionaries on the local filesystem.
        return cls(config)

    def remove_numbers(self, text):
        result = re.sub(r'\d+', '', text)
        return result

    def remove_punctuation(self, text):
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def remove_whitespace(self, text):
        return " ".join(text.split())

    def preprocess(self, text):
        text = text.strip().lower()
        text = self.remove_numbers(text)
        text = self.remove_punctuation(text)
        text = self.remove_whitespace(text)
        return text

    # def _convert_words_to_tokens(words: List[Text], text: Text) -> List[Token]:
    #     running_offset = 0
    #     tokens = []

    #     for word in words:
    #         word_offset = text.find(word)
    #         word_len = len(word)
    #         running_offset = word_offset + word_len
    #         tokens.append(Token(word, word_offset))

    #     return tokens

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)

        temp = self.preprocess(text)

        words = word_tokenize(temp)
        words = [w for w in words if w]
        if not words:
            words = [text]
        tokens = self._convert_words_to_tokens(words, text)

        return self._apply_token_pattern(tokens)
