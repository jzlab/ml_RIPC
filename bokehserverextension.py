from subprocess import Popen

# Copied from https://github.com/binder-examples/bokeh

def load_jupyter_server_extension(nbapp):
    """serve the bokeh-app directory with bokeh server"""
    Popen(["bokeh", "serve", "bokeh-app", "--allow-websocket-origin=*"])
