# Readme File

## Steps to install dashboard with caching

1. Clone the repository
    `git clone https://github.com/wendellswa06/commdashboard.git`

2. Create a python Environment (3.10) and activate it
    `source venv/bin/activate`

3. Install the dependencies
    `pip install -r requirements.txt`

4. Replace `blocks.py` file in `/commdashboard/venv/lib/python3.10/site-packages/gradio` to get the server address
    
4. Run the application locally for development purposes:
    `streamlit run main-v5.py --server.port=2510`

    This v5 version introduces caching to the dashboard.

The server will start running on localhost at port 2510