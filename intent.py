import os
from google.cloud import dialogflow
import google.api_core.exceptions
import json
import sys
import argparse
import uuid
from environs import Env


env = Env()
env.read_env()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--action',
        dest='action',
        required=True,
        help='action to do'
    )

    parser.add_argument(
        '--path',
        dest='path',
        required=False,
        help='Path to json file with intents'
    )

    parser.add_argument(
        '--intent_id',
        dest='intent_id',
        required=False,
        help='id intent to delete'
    )

    return parser.parse_args()


def list_intents(project_id):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    intents = intents_client.list_intents(request={"parent": parent})

    for intent in intents:
        print("=" * 20)
        print(f"Intent name: {intent.name}")
        print(f"Intent display_name: {intent.display_name}")
        print(f"Action: {intent.action}\n")
        print(f"Root followup intent: {intent.root_followup_intent_name}")
        print(f"Parent followup intent: \
            {intent.parent_followup_intent_name}\n")

        print("Input contexts:")
        for input_context_name in intent.input_context_names:
            print("\tName: {}".format(input_context_name))

        print("Output contexts:")
        for output_context in intent.output_contexts:
            print("\tName: {}".format(output_context.name))


def create_intent(
    project_id,
    display_name,
    training_phrases_parts,
    message_texts
):

    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def delete_intent(project_id, intent_id):
    """Delete intent with the given intent type and intent value."""

    intents_client = dialogflow.IntentsClient()
    intent_path = intents_client.intent_path(project_id, intent_id)
    intents_client.delete_intent(request={"name": intent_path})


def read_file(filepath):
    with open(filepath, 'r') as file:
        file_content = json.load(file)
    return file_content


def main():
    project_id = env('PROJECT_ID')
    args = parse_arguments()

    if args.action == 'create' and os.path.exists(args.path):
        try:
            intent_content = read_file(args.path)
        except FileNotFoundError:
            sys.exit('File not found. Exit')

        for intent in intent_content:
            questions = intent_content[intent]['questions']
            answer = intent_content[intent]['answer']
            try:
                create_intent(project_id, intent, questions, [answer])
            except google.api_core.exceptions.ServiceUnavailable:
                sys.exit("Can't reach google service")
            except google.api_core.exceptions.FailedPrecondition:
                print(f'Failed precondition for intent with name "{intent}"')
                continue

    elif args.action == 'list':
        list_intents(project_id)

    elif args.action == 'delete' and args.intent_id:
        try:
            isinstance(uuid.UUID(args.intent_id), uuid.UUID)
        except ValueError:
            sys.exit('Invalid intent ID')
        delete_intent(project_id, args.intent_id)
    else:
        sys.exit('Invalid arguments')


if __name__ == '__main__':
    main()
