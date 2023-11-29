import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
import together
from chainlit.input_widget import TextInput

from together_ai_trial.configuration.config import cfg
import together_ai_trial.backend.together_api_exec as exec_api




async def ask_user_msg(question):
    ans = None
    while ans == None:
        ans = await cl.AskUserMessage(
            content=f"{question}", timeout=cfg.ui_timeout, raise_on_timeout=True
        ).send()
    return ans


@cl.on_chat_start
async def start():
    question = await ask_user_msg("Enter the question that you want to ask")
    for model in cfg.model_list:
        output, time_exec = await exec_api.run_model(model, question['content'])
        await cl.Message(
            content=output
        ).send()
        await cl.Message(
            content=f"Model selected: {model}"
        ).send()
        await cl.Message(
            content= f"Time of execution: {time_exec}"
        ).send()
        await exec_api.save_to_file(model, output, time_exec, question['content'])

@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)