from modeltranslation.translator import translator, TranslationOptions
from vqapps.faq.models import FAQ


class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer',)

translator.register(FAQ, FAQTranslationOptions)