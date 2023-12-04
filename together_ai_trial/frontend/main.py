import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
import together
from chainlit.input_widget import TextInput
import pandas as pd

from together_ai_trial.configuration.config import cfg
import together_ai_trial.backend.together_api_exec as exec_api
import together_ai_trial.services.pylint_services as pylint_services
import together_ai_trial.services.extract_code_service as code_service




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
    for model in cfg.updated_model_list:
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
        output_file = await pylint_services.lint_code(output, question['content'], model)
        f = open(output_file,'r')
        pylint_output = f.read()
        await cl.Message(
            content= f"Pylint code evaluation: {pylint_output}"
        ).send()
        if "fatal" in pylint_output or pylint_output == "":
            pylint_execution = 'no'
        else:
            pylint_execution = 'yes'
        data = {"Model": [model], 'Question': [question['content']], 'Model output': [output], 'Time for execution': [time_exec], 'Pylint result': [pylint_output], 'Is the code correct': [pylint_execution]}
        await exec_api.add_to_df(data)
        
        output_code = await exec_api.add_comments(model, output, question['content'])
        await cl.Message(
            content= f"code after adding comments: {output_code}"
        ).send()
    
    



@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)