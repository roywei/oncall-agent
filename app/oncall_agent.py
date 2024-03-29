from openai import OpenAI
import time
from dotenv import find_dotenv, dotenv_values
import os
config = dotenv_values(find_dotenv())


PROMPT = """
You are oncall agent, you job is to help provide solution to incidents. You will be asked with specific errors, based on your knowledge files, tell the user how to fix the problem. Reply in the following json format. File is the file to modify, area is the area of focus in the file, instruction is detailed instruction on how to fix the error, report name is the knowledge file name you used to find the solution. If you are not certain about the error, reply sorry, I cant find any existing solution from incident reports.
{
file: string
area: string
instruction: string
report_name: string
}
"""

class OnCallAgent():
    def __init__(self):
        self.client = OpenAI(api_key=config['OPENAI_API_KEY'])
        if not config["ASSISTANT_ID"]:
            directory = "../incident_reports"
            file_ids = []

            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    file = self.client.files.create(
                        file=open(os.path.join(directory, filename), "rb"),
                        purpose='assistants'
                    )
                    file_ids.append(file.id)
            
            assistant = self.client.beta.assistants.create(
                name="OncallAgent",
                instructions=PROMPT,
                tools=[{"type": "retrieval"}],
                model="gpt-4-turbo-preview",
                file_ids=file_ids
            )
            print(assistant)
            id = assistant.id
            with open('../.env', 'a') as env_file:
                env_file.write(f"ASSISTANT_ID={id}\n")
            self.assistant_id = id
        else:
            self.assistant_id = config["ASSISTANT_ID"]
            print('using existing id: ', self.assistant_id)


    def research_incident(self, error_message, stack_trace, additional_info):
        print(f"Agent id {self.assistant_id} is researching on the incident...")
        thread = self.client.beta.threads.create()
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Help me fix this error, remember your instructions and return in json format if solution found: {error_message}\n : {stack_trace}\n: {additional_info}"
        )
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
            tools=[{"type": "retrieval"}]
        )
        while run.status != 'completed':
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print(run.status)
            if run.status == 'failed':
                print('run failed!')
                break
            time.sleep(5)
        messages = self.client.beta.threads.messages.list(
            thread_id=thread.id
        )
        return messages.data[0]
