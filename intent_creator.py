import json

from environs import Env
from google.cloud import dialogflow_v2 as dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrase_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrase_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print(f"✅ Добавлен интент: {response.display_name}")


def main():
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')

    with open("questions.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for intent_name, content in data.items():
        questions = content["questions"]
        answer = [content["answer"]]
        try:
            create_intent(project_id, intent_name, questions, answer)
        except Exception as e:
            print(f"⚠️ Ошибка при создании интента '{intent_name}': {e}")


if __name__ == "__main__":
    main()
