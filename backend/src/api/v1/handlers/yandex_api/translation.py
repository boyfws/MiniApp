# from googletrans import Translator
#
#
# def get_rus_city(city: str) -> str:
#     city = city.strip().title()
#     try:
#         translator = Translator()
#         translation = translator.translate(city, src='en', dest='ru')
#         return translation.text
#     except Exception as e:
#         return f"Translation error: {e}"
