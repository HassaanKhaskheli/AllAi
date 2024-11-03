from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv('"OPENAI_API_KEY"'))

#----------------------------------------------------------------------------------------------------------------------------Declare and Initialize Assistant

assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4o",
)

"""assistants.create parameters
model Required
      gpt model to use
name
      assistant name
description
      assistant's description
instructions
      assistant's personality/role/goals
tools
      code_interpreter: important for assistant to be able to run python code to solve challenging code and math problems
      file_search: allows assistant to read files provided by user and create and store vector embeddings to then answer user questions
      function: to describe functions to the Assistants API and have it intelligently return the functions that need to be called along with their arguments, uusage shown below:
                {
                "type": "function",
                "function": {
                  "name": "get_current_temperature",
                  "description": "Get the current temperature for a specific location",
                  "parameters": {
                    "type": "object",
                    "properties": {
                      "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA"
                      },
                      "unit": {
                        "type": "string",
                        "enum": ["Celsius", "Fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the user's location."
                      }
                    },
                    "required": ["location", "unit"]
                  }
                }
              },
tool_resources
      code_interpreter tool requires a list of file IDs
      file_search tool requires a list of vector store IDs.
metadata
      Set of 16 key-value pairs that store additional information about the object in a structured format.
temperature
      Range is 0-2, defaults to 1
      Higher values like 0.8 will make the output more random
      lower values like 0.2 will make it more focused and deterministic
top_p
      can't understand, will document later
      alter this or temperature but not both.
"""

#----------------------------------------------------------------------------------------------------------------------------Declare and Initialize thread

thread = client.beta.threads.create()

"""threads.create parameters
messages
      A list of messages to start the thread with.
tool_resources
      code_interpreter tool requires a list of file IDs
      file_search tool requires a list of vector store IDs.
metadata
      Set of 16 key-value pairs that store additional information about the object in a structured format.
"""

#----------------------------------------------------------------------------------------------------------------------------Adding Message to Thread

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

"""messages.create parameters
thread_id Required
      thread.id
role Required
      user: user-generated messages
      assistant: to insert messages from the assistant into the conversation.
content Required
    string if one message or array
attachments
      A array of files attached to the message, and the tools they should be added to.
metadata
      Set of 16 key-value pairs that store additional information about the object in a structured format.
"""

#----------------------------------------------------------------------------------------------------------------------------EventHandler class to handle events in response stream

class EventHandler(AssistantEventHandler):
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)

#----------------------------------------------------------------------------------------------------------------------------Creating a Run 

#------------------------------------with streaming (streaming means you get response as it is generated)

with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account.",
  event_handler=EventHandler(),
) as stream:
  stream.until_done()

#------------------------------------without streaming

# run = client.beta.threads.runs.create_and_poll(
#   thread_id=thread.id,
#   assistant_id=assistant.id,
#   instructions="Please address the user as Jane Doe. The user has a premium account."
# )

# if run.status == 'completed': 
#   messages = client.beta.threads.messages.list(
#     thread_id=thread.id
#   )
#   print(messages)
# else:
#   print(run.status)

"""runs.stream parameters
assistant_id Required
      assistant id
thread_id Required
      thread.id
model
      overrides assistant.model
instructions
      overrides assistant.instructions
additional_instructions
      if you need additional instructions without overriding assistant.instructions
additional_messages
      Adds additional messages to the thread before creating the run.
tools
      overrides assistant.tools
metadata
      Set of 16 key-value pairs that store additional information about the object in a structured format.
temperature
      Range is 0-2, defaults to 1
      Higher values like 0.8 will make the output more random
      lower values like 0.2 will make it more focused and deterministic
top_p
      can't understand, will document later
      alter this or temperature but not both.
stream
      If true, returns a stream of events that happen during the Run as server-sent events, terminating when the Run enters a terminal state with a data: [DONE] message.
max_prompt_tokens
      The maximum number of prompt tokens that may be used over the course of the run
max_completion_tokens
      The maximum number of completion tokens that may be used over the course of the run. The run will make a best effort to use only the number of completion tokens specified, across multiple turns of the run. If the run exceeds the number of completion tokens specified, the run will end with status incomplete. See incomplete_details for more info.
truncation_strategy
      type Required
          The default is auto. 
           If set to last_messages, the thread will be truncated to the n most recent messages in the thread. 
          If set to auto, messages in the middle of the thread will be dropped to fit the context length of the model that is max_prompt_tokens.
      last_messages
          The number of most recent messages from the thread when constructing the context for the run.
tool_choice
      check openAi documentation
parallel_tool_calls
      Defaults to true
      Whether to enable parallel function calling during tool use.
response_format
      Defaults to "auto"
      { "type": "json_schema" } : check openAi documentation
      { "type": "text" }
      { "type": "json_object" }
"""

#----------------------------------------------------------------------------------------------------------------------------Submitting tool output to run

# stream = client.beta.threads.runs.submit_tool_outputs(
#   thread_id="thread_123",
#   run_id="run_123",
#   tool_outputs=[
#     {
#       "tool_call_id": "call_001",
#       "output": "70 degrees and sunny."
#     }
#   ],
#   stream=True
# )

# for event in stream:
#   print(event)

"""runs.submit_tool_outputs parameters
thread_id Required
      thread.id
run_id Required
      id of the run that requires the tool output submission
tool_outputs Required
      tool_call_id
            The ID of the tool call in the required_action object within the run object the output is being submitted for.
      output
            The output of the tool call to be submitted to continue the run.
stream
      If true, returns a stream of events that happen during the Run as server-sent events
"""