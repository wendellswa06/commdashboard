# vizlaunch module

This is a dashboard for managing Gradio apps. It allows you to launch and stop Gradio apps by selecting them from a dropdown menu.

## Usage

1. Select a Gradio app from the dropdown menu.
2. Click the "Launch" button to start the app.
3. Once the app is running, you can access it by clicking on the URL displayed below the button.
4. If you want to stop the app, click the "Stop" button.

## How to install

To run all the modules listed in the dashboard(vizlaunch), install required dependecies.

```bash
pip install -r requirements.txt
```

Regarding the modules that require packages incompatible with the main environment, we dockerize them and add them to the dashboard.

Need to change some packages like gradio, image-tools and so on.