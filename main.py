# [START gae_python37_app]
from flask import Flask

import tkinter as tk
from template.editor import Editor


app = Flask(__name__)

@app.route('/')
def main():
    root = tk.Tk()
    app = Editor(root)
    root.title("Longclaw")
    root.minsize(950,550)
    root.configure()
    root.mainloop()

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error while processing a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
    
    
#if __name__ == '__main__':
 #   main()
