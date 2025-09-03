import os
import requests

from types import SimpleNamespace


from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder


class ChatHandler:
    def __init__(self) -> None:

        self.project = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]+'api/projects/firstProject')
        
        self.agent_master = self.project.agents.get_agent("asst_auBBqrhcSppyJ1wMJyY5qdmK")
        self.logging_agent = self.project.agents.get_agent("asst_23h0ZKTNIbJ99HzPqPRoVQUu")
        self.thread = self.project.agents.threads.create()
    
    def trigger_api_post_request(self,url, payload):
        headers = {
            "api-key": os.environ["AZURE_RBG_ADDRESS_KEY"],
            "Ocp-Apim-Subscription-Key": os.environ["AZURE_RBG_APIM_WS_KEY"],
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an error for bad responses (4xx/5xx)
        return response.json()
    
    def trigger_api_get_request(self,url):
        headers = {
            "Ocp-Apim-Subscription-Key": os.environ["AZURE_RBG_APIM_WS_KEY"],
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for bad responses (4xx/5xx)
        return response.json()
    
    def parse_conversation(self, conversation_str):
        messages = []
        lines = conversation_str.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            if line.startswith('User: '):
                # Extract user message (may span multiple lines)
                user_content = line[6:]  # Remove "User: " prefix
                i += 1
                while i < len(lines) and not (lines[i].startswith('User: ') or lines[i].startswith('Assistant: ')):
                    user_content += '\n' + lines[i]
                    i += 1
                messages.append(("human", user_content.strip()))
            elif line.startswith('Assistant: '):
                # Extract assistant message (may span multiple lines)
                ai_content = line[11:]  # Remove "Assistant: " prefix
                i += 1
                while i < len(lines) and not (lines[i].startswith('User: ') or lines[i].startswith('Assistant: ')):
                    ai_content += '\n' + lines[i]
                    i += 1
                messages.append(("ai", ai_content.strip()))
            else:
                i += 1
        
        return messages

    def call_agent(self, agent_id, input_text):
        latest_message = str(self.parse_conversation(input_text)[-1])
        message = self.project.agents.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=latest_message
        )

        run = self.project.agents.runs.create_and_process(
            thread_id=self.thread.id,
            agent_id=agent_id
        )

        messages = self.project.agents.messages.list(thread_id=self.thread.id, order=ListSortOrder.ASCENDING)

        response = next(
            (msg.text_messages[-1].text.value for msg in list(messages)[::-1] if msg.text_messages),
            None
        )

        return response

    def get_chat_response(self, input_text):

        response = self.call_agent(self.agent_master.id, input_text)

        return response

    def get_chat_summary(self, input_text):

        response = self.call_agent(self.logging_agent.id, input_text)

        return response
