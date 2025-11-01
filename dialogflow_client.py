import os

from environs import Env
from google.cloud import dialogflow_v2 as dialogflow


def detect_intent_text(text: str, user_id: str, lang: str = "ru"):
    env = Env()
    env.read_env()

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env.str("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = env.str("PROJECT_ID")

    client = dialogflow.SessionsClient()
    session = client.session_path(project_id, str(user_id))

    text_input = dialogflow.TextInput(text=text, language_code=lang)
    query_input = dialogflow.QueryInput(text=text_input)

    response = client.detect_intent(request={"session": session, "query_input": query_input})
    result = response.query_result

    return result.fulfillment_text, getattr(result.intent, "is_fallback", False)
