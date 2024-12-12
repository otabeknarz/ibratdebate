from modeltranslation.translator import translator, TranslationOptions
from .models import Debate


class DebateTranslationOptions(TranslationOptions):
    fields = ("name", "description")


translator.register(Debate, DebateTranslationOptions)
