from google.cloud import translate

def google_translate(text="Hello, world!", project_id="tranquil-garage-399812"):

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": "jp",
        }
    )

    for translation in response.translations:
        print("Translated text: {}".format(translation.translated_text))

google_translate()