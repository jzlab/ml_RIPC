import setuptools

setuptools.setup(
        name="jupyter-bokeh-server",
        py_modules=['untargeted'],
        entry_points={
                'jupyter_serverproxy_servers':[
                        'untargeted = untargeted:setup_untargeted'
                ]
        }
)

