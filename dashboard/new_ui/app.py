import os
from flask import Flask, render_template, redirect
import subprocess
import time
import shutil
import psutil
from functools import lru_cache
app = Flask(__name__)

processes = {}

modulelist = ['model.text2image', 'model.image2image', 'model.image2video', 'model.text2video', 'model.yolo',
              'model.video2text', 'model.image2text', 'model.vectorstore', 'model.stabletune', 'model.music_mixer',
              'model.ocr', 'model.musicgen', 'model.stock', 'model.sentence', 'model.langchain_agent',
              'model.imageupscaler']

modulenamelist = [element.split('.')[1] for element in modulelist]

@lru_cache(maxsize=32)
def get_command(app_number):
    python_executable = "c"  # Adjust this path to your Python interpreter
    return [python_executable, modulelist[app_number-1], 'gradio']

# Function to launch the specified gradio app
def launch_gradio_app(app_number):
    command = get_command(app_number)
    
    if app_number in processes:
        print(f"Model {command[1][6:]} is already running.")
        return
    print(f"Starting {command[1][6:]}")
    if os.path.exists('tmp.txt'):
        os.remove('tmp.txt')

    try:
        shutil.rmtree("frame-interpolation")
    except OSError as e:
        print("Error removing folder: ", e)
        
        
    # Launch gradio process as a subprocess
    process = subprocess.Popen(command)
    processes[app_number] = process
    
    # Wait for the server to start
    while not os.path.exists("tmp.txt"):
        time.sleep(1)

    # copy the link after the creation of tmp.txt
    with open("tmp.txt", "r") as file:
        server_address = file.read()
        
        
    # Removing tmp.txt after reading it contents
    os.remove('tmp.txt')
    
    return server_address



# Define a function to stop Gradio app
def stop_gradio_app(app_number):
    if app_number in processes:
        process = processes.pop(app_number)
        parent = psutil.Process(process.pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        parent.kill()
        print(f"Model {modulenamelist[app_number]} has been stopped.")
    else:
        print(f"Model {modulenamelist[app_number]} is not running.")
        
        
def stop_all_gradio_apps():
    # Create a copy of the keys to avoid modifying the dictionary using iteration
    process_keys = list(processes.keys())
    for app_number in process_keys:
        process = processes.pop(app_number)
        parent = psutil.Process(process.pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        parent.kill()
        print(f"Model {modulenamelist[app_number-1]} has been stopped.")
    processes.clear()
            
        

  
@app.route('/launch/<int:app_number>')
def launch_app(app_number):
    server_address = launch_gradio_app(app_number)

    # Render the template with the custom navbar and iframe for the server address
    return render_template('launch.html', server_address=server_address, name=modulenamelist[app_number-1])

@app.route("/loading/<int:app_number>")
def loading(app_number):
    return render_template("loader.html", app_number=app_number, name=modulenamelist[app_number-1])


@app.route('/stopall')
def stopall():
    stop_all_gradio_apps()
    return "Stop all previously running Gradio apps"

@app.route('/stop/<app_number>')
def stop_app(app_number):
    app_number = int(app_number)
    stop_gradio_app(app_number)
    return redirect('/launcher')


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/launcher")
def launcher():
    return render_template("launcher.html")

if __name__ == "__main__":
    extra_dirs = ["dashboard/new_ui/frame-interpolation"]
    app.run(host='0.0.0.0', debug=False, port=2520)
