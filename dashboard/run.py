import streamlit as st
import subprocess
import os
import signal

# Customizing the page
st.set_page_config(page_title="Gradio Model Launcher", layout="wide")

# Dictionary to keep track of Gradio app processes
processes = {}

# Function to get the command for launching a Gradio app
def get_command(app_number):
    # python_executable = "/usr/bin/python3"
    python_executable = "c"
    # Adjust these paths and ports according to your setup
    # apps = [
    #     {'path': '/home/shane/commune/commune/modules/model/text2image/model_text2image.py', 'port': 7860},
    #     {'path': '/home/shane/commune/commune/modules/model/image2image/model_image2image.py', 'port': 7860},
    #     {'path': '/home/shane/commune/commune/modules/model/image2video/model_image2video.py', 'port': 7860},
    #     {'path': '/home/shane/commune/commune/modules/model/text2video/model_text2video.py', 'port': 7860},
    #     {'path': '/home/shane/commune/commune/modules/model/zapier/model_zapier.py', 'port': 7860},
    #     {'path': '/home/shane/commune/commune/modules/model/yolo/yolo.py', 'port': 7860},
    #     {'path': '/home/shane/commune/commune/modules/model/video2text/video2text.py', 'port': 7860},
    #     {'path': '/home/shane/commune/commune/modules/model/vectorstore/vectorstore.py', 'port': 7860},
    #     {'path': '/home/shane/commune/commune/modules/model/translation/model_translation.py', 'port': 7860}
        


    #     # Add other apps here with their respective paths and ports
    # ]
    apps = [
        {'path': 'model.text2image', 'function': 'gradio', 'port': 7860},
        {'path': 'model.image2image', 'function': 'gradio', 'port': 7860},
        {'path': 'model.image2video', 'function': 'gradio', 'port': 7860},
        {'path': 'model.text2video', 'function': 'gradio', 'port': 7860},
        {'path': 'model.zapier', 'function': 'gradio', 'port': 7860},
        {'path': 'model.yolo', 'function': 'gradio', 'port': 7860},
        {'path': 'model.video2text', 'function': 'gradio', 'port': 7860},
        {'path': 'model.vectorstore', 'function': 'gradio', 'port': 7860},
        {'path': 'model.translation', 'function': 'gradio', 'port': 7860}        


        # Add other apps here with their respective paths and ports
    ]
    app = apps[app_number - 1]
    return [python_executable, app['path'], app['function'], '--server.port', str(app['port'])]


# Enhanced UI for launching and stopping apps
def ui_launch_stop_app(app_number, app_name):
    col1, col2 = st.columns([1, 1], gap="small")
    with col1:
        if st.button(f"Launch {app_name}", key=f"launch_{app_number}"):
            launch_gradio_app(app_number)
    with col2:
        if st.button(f"Stop {app_name}", key=f"stop_{app_number}"):
            stop_gradio_app(app_number)

# Launch Gradio app in a separate process
def launch_gradio_app(app_number):
    if app_number in processes:
        st.warning(f"Model {app_number} is already running.")
        return
    command = get_command(app_number)
    process = subprocess.Popen(command)
    processes[app_number] = process
    # Assuming your server's IP address or hostname is known and fixed
    server_address = "http://127.0.0.1"  # Replace "localhost" with your server's IP address or hostname
    port = command[-1]  # The last element in the command list is the port
    st.markdown(f"Model {app_number} is starting... Access it at: {server_address}:{port}")

# Stop a running Gradio app
def stop_gradio_app(app_number):
    if app_number in processes:
        process = processes.pop(app_number)
        os.kill(process.pid, signal.SIGTERM)
        st.success(f"Model {app_number} has been stopped.")
    else:
        st.warning(f"Model {app_number} is not running.")

# Main UI
st.title("Gradio Model Launcher")
st.markdown("Select a Gradio app to manage. Launch or stop any model with ease.")

app_options = ["Select", "Text2Image", "Image2Image", "Image2Video", "Text2Video", "Zapier", "YOLO", "Video2Text", "Image2Text", "Vectorstore", "Translation"]
app_choice = st.selectbox("Choose a Gradio app to manage:", app_options)

if app_choice != "Select":
    app_number = app_options.index(app_choice)
    ui_launch_stop_app(app_number, app_choice)
