import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider

model_list = [
    "togethercomputer/alpaca-7b",
    "Austism/chronos-hermes-13b",
    "togethercomputer/CodeLlama-7b-Python",
    "togethercomputer/CodeLlama-7b",
    "togethercomputer/CodeLlama-13b-Python",
    "togethercomputer/CodeLlama-34b-Python",
    "togethercomputer/llama-2-7b-chat",
    "togethercomputer/llama-2-13b-chat",
    "togethercomputer/llama-2-70b-chat",
    "togethercomputer/llama-2-70b",
    "mistralai/Mistral-7B-v0.1",
    "Gryphe/MythoMax-L2-13b",
    "NousResearch/Nous-Hermes-Llama2-13b",
    "NousResearch/Nous-Hermes-Llama2-70b",
    "NousResearch/Nous-Hermes-llama-2-7b",
    "teknium/OpenHermes-2p5-Mistral-7B",
    "togethercomputer/Qwen-7B-Chat",
    "Undi95/ReMM-SLERP-L2-13B",
    "lmsys/vicuna-13b-v1.5-16k",
    "lmsys/vicuna-13b-v1.5",
    "lmsys/vicuna-7b-v1.5",
    "WizardLM/WizardCoder-15B-V1.0",
    "WizardLM/WizardLM-70B-V1.0"
]

@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI - Model",
                values=model_list,
                initial_index=0,
            ),
            Switch(id="Streaming", label="OpenAI - Stream Tokens", initial=True),
            Slider(
                id="Temperature",
                label="OpenAI - Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
            Slider(
                id="SAI_Steps",
                label="Stability AI - Steps",
                initial=30,
                min=10,
                max=150,
                step=1,
                description="Amount of inference steps performed on image generation.",
            ),
            Slider(
                id="SAI_Cfg_Scale",
                label="Stability AI - Cfg_Scale",
                initial=7,
                min=1,
                max=35,
                step=0.1,
                description="Influences how strongly your generation is guided to match your prompt.",
            ),
            Slider(
                id="SAI_Width",
                label="Stability AI - Image Width",
                initial=512,
                min=256,
                max=2048,
                step=64,
                tooltip="Measured in pixels",
            ),
            Slider(
                id="SAI_Height",
                label="Stability AI - Image Height",
                initial=512,
                min=256,
                max=2048,
                step=64,
                tooltip="Measured in pixels",
            ),
        ]
    ).send()


@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)