import os
import openai
import random

API_KEY = 'OPENAI_API_KEY'
os.environ['OPENAI_Key'] = API_KEY
openai.api_key = os.environ['OPENAI_Key']


def main():
    scenarios = ["a patient with symptoms of the flu that have been developing over the past week during a doctor examination.",
                 "a patient with chronic high blood pressure during a doctor examination.",
                 "a patient with a wrist that was broken in a soccer game during a doctor examination.",
                 "a patient who has been suffering from depression for the past year during an examination with their doctor",
                 "a patient during their post-surgery follow-up with their doctor after their successful hip surgery"]

    keep_prompting = True
    scenario = random.randint(0, 4)
    while keep_prompting:
        user_input = input('What is your question for the patient? Please type \'complete\' when done.\n')

        if user_input == 'complete':
            keep_prompting = False
        else:
            response = openai.Completion.create(
                model="text-curie-001",
                prompt=user_input + 'Please respond as if you are ' + scenarios[scenario],
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print(response["choices"][0]["text"])


if __name__ == "__main__":
    main()
