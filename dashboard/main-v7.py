import streamlit as st
import os
import asyncio
from functools import lru_cache

# Dictionary to keep track of Gradio app processes
modulelist = ['model.text2image', 'model.image2image', 'model.image2video', 'model.text2video', 'model.yolo',
              'model.video2text', 'model.image2text', 'model.vectorstore', 'model.stabletune', 'model.music_mixer',
              'model.ocr', 'model.musicgen', 'model.stock', 'model.sentence', 'model.langchain_agent',
              'model.imageupscaler']

modulenamelist = [element.split('.')[1] for element in modulelist]

if 'processes' not in st.session_state:
    st.session_state.processes = {}

st.set_page_config(layout="wide", page_title="Commune Module Dashboard", page_icon=":ðŸª:")

ms = st.session_state

if "themes" not in ms:
    ms.themes = {"current_theme": "light",
                 "refreshed": True,

                 "light": {"theme.base": "dark",
                           "theme.backgroundColor": "black",
                           "theme.primaryColor": "#c98bdb",
                           "theme.secondaryBackgroundColor": "#5591f5",
                           "theme.textColor": "white",
                           "theme.textColor": "white",
                           "button_face": "☀️"},

                 "dark": {"theme.base": "light",
                          "theme.backgroundColor": "white",
                          "theme.primaryColor": "#5591f5",
                          "theme.secondaryBackgroundColor": "#82E1D7",
                          "theme.textColor": "#0a1464",
                          "button_face": "🌙"},
                 }


def ChangeTheme():
    previous_theme = ms.themes["current_theme"]
    tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
    for vkey, vval in tdict.items():
        if vkey.startswith("theme"): st._config.set_option(vkey, vval)

    ms.themes["refreshed"] = False
    if previous_theme == "dark":
        ms.themes["current_theme"] = "light"
    elif previous_theme == "light":
        ms.themes["current_theme"] = "dark"


btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"][
    "button_face"]
st.button(btn_face, on_click=ChangeTheme)

if ms.themes["refreshed"] == False:
    ms.themes["refreshed"] = True
    st.rerun()


# Function to get the command for launching a Gradio app
def get_command(app_number):
    python_executable = "c"  # Adjust this path to your Python interpreter
    return [python_executable, modulelist[app_number - 1], 'gradio']


# Define a function to launch Gradio app
@lru_cache(maxsize=10)
async def launch_gradio_app(app_number):
    command = get_command(app_number)

    if app_number in st.session_state.processes:
        st.warning(f"Model {command[1][6:]} is already running.")
        return

    if os.path.exists('tmp.txt'):
        os.remove('tmp.txt')

    try:
        os.rmdir("frame-interpolation")
    except OSError as e:
        print("Error removing folder:", e)

    # Launch Gradio app as a subprocess
    process = await asyncio.create_subprocess_exec(*command)
    st.session_state.processes[app_number] = process

    # Wait for the server to start
    while not os.path.exists("tmp.txt"):
        await asyncio.sleep(1)

    with open("tmp.txt", "r") as file:
        server_address = file.read()

    # Removing tmp.txt after reading its contents
    os.remove('tmp.txt')

    return server_address


# Define a function to stop Gradio app
async def stop_gradio_app(app_number):
    if app_number in st.session_state.processes:
        process = st.session_state.processes.pop(app_number)
        process.terminate()
        st.success(f"Model {app_number} has been stopped.")
    else:
        st.warning(f"Model {app_number} is not running.")

async def stop_all_gradio_apps():
    # Create a copy of the keys to avoid modifying the dictionary during iteration
    process_keys = list(st.session_state.processes.keys())
    for app_number in process_keys:
        await stop_gradio_app(app_number)
# Define main function
async def main():
    st.title("Gradio Model Launcher")
    st.sidebar.title("Module Select")
    app_choice = st.sidebar.selectbox("Choose a Gradio app to manage:", ["Select", *modulenamelist])
    if app_choice != "Select":
        app_number = modulenamelist.index(app_choice) + 1
        if st.sidebar.button(f"Launch {app_choice}"):
            await stop_all_gradio_apps()
            st.warning(f"Starting {modulelist[app_number - 1].split('.')[1]} Model UI...")
            server_address = await launch_gradio_app(app_number)
            st.markdown(f"Model {app_choice} is starting... Access it at: {server_address}")
            st.markdown(f'<div><iframe src="{server_address}" width="100%" style="height: 100vh" ></iframe><div>',
                        unsafe_allow_html=True)
        if st.sidebar.button(f"Stop {app_choice}"):
            await stop_gradio_app(app_number)
    else:
        st.header(f"Welcome Module")
        st.text(f"select Any Module on the dropdown")


# Run the main function
if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())  # Set event loop to current loop
    asyncio.get_event_loop().run_until_complete(main())
