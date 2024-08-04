from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

SCRIPT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')

def run_script(script_name):
    script_path = os.path.join(SCRIPT_FOLDER, script_name)
    if os.path.exists(script_path):
        subprocess.run(["powershell", "-File", script_path])
    else:
        print(f"Script {script_name} does not exist.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_command', methods=['POST'])
def run_command_route():
    command = request.form['command']
    script_mapping = {
        'top_command': 'script_top.ps1',
        'command_1': 'script1.ps1',
        'command_2': 'script2.ps1',
        'command_3': 'script3.ps1',
        'command_4': 'script4.ps1',
        'command_5': 'script5.ps1',
        'command_6': 'script6.ps1'
    }
    if command in script_mapping:
        run_script(script_mapping[command])
    return 'Command executed successfully'

if __name__ == '__main__':
    app.run(debug=True)
