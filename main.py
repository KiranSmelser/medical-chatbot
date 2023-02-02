import os
import openai

API_KEY = 'sk-GhzkOOxKuygy400G9pJCT3BlbkFJXQ45JOTDdJACldfWgE1HH'
os.environ['OPENAI_Key'] = API_KEY
openai.api_key = os.environ['OPENAI_Key']


def main():
    keep_prompting = True
    while keep_prompting:
        user_input = input('What is your question for the patient? Please type \'complete\' when done.')

        if user_input == 'complete':
            keep_prompting = False
        else:
            response = openai.Completion.create(
                model="text-curie-001",
                prompt=user_input + 'Please respond as if a patient with a migraine during a doctor examination.',
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print(response["choices"][0]["text"])


if __name__ == "__main__":
    main()