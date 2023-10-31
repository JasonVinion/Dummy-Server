import sys
import threading
from flask import Flask, jsonify, request
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QCheckBox
from PyQt5.QtCore import pyqtSlot, QMutex, QMutexLocker, Qt
from PyQt5.QtGui import QPalette, QColor
import requests
import psutil


app = Flask(__name__)
server_thread = None
mutex = QMutex()

@app.route('/')
def home():
    return jsonify(message='Dummy Server is Running')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        with QMutexLocker(mutex):
            if hasattr(server_thread, 'shutdown'):
                server_thread.shutdown()
            else:
                return jsonify(message='Error: Server not running with Werkzeug or manual shutdown not available')
    else:
        func()
    return jsonify(message='Server shutting down...')

@app.route('/connections')
def connections():
    connections = []
    for conn in psutil.net_connections():
        if conn.status == 'ESTABLISHED' and conn.laddr.ip == '127.0.0.1' and conn.laddr.port == 5000:
            connections.append(conn.raddr.ip)
    return jsonify(connections=connections)

@app.route('/kill', methods=['GET'])
def kill():
    killed_connections = 0
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == 'ESTABLISHED' and conn.laddr.ip == '127.0.0.1' and conn.laddr.port == 5000 and conn.raddr.ip != '127.0.0.1':
            process = psutil.Process(conn.pid)
            process.terminate()
            killed_connections += 1

    return jsonify(message=f'Killed {killed_connections} connections')

class ServerThread(threading.Thread):
    def run(self):
        def shutdown():
            with QMutexLocker(mutex):
                print('Shutting down gracefully...')
                request.environ.get('werkzeug.server.shutdown')()
        
        self.shutdown = shutdown
        app.run(port=5000, use_reloader=False)

class ServerControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Dummy Server Control')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.status_label = QLabel('Server Status: Stopped', self)
        layout.addWidget(self.status_label)

        self.start_btn = QPushButton('Start Server', self)
        self.start_btn.clicked.connect(self.start_server)
        layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton('Stop Server', self)
        self.stop_btn.clicked.connect(self.stop_server)
        layout.addWidget(self.stop_btn)

        self.connections_btn = QPushButton('Check Connections', self)
        self.connections_btn.clicked.connect(self.check_connections)
        layout.addWidget(self.connections_btn)

        self.kill_connections_btn = QPushButton('Kill All Connections', self)
        self.kill_connections_btn.clicked.connect(self.kill_all_connections)
        layout.addWidget(self.kill_connections_btn)

        self.dark_mode_toggle = QCheckBox('Dark Mode', self)
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)
        layout.addWidget(self.dark_mode_toggle)

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.close_application)
        layout.addWidget(self.quit_button)  # Adding the Quit button to the layout

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    @pyqtSlot()
    def start_server(self):
        global server_thread
        if server_thread is None:
            server_thread = ServerThread()
            server_thread.start()
            self.status_label.setText('Server Status: Running on http://127.0.0.1:5000')

    @pyqtSlot()
    def stop_server(self):
        global server_thread
        if server_thread is not None:
            try:
                response = requests.post('http://127.0.0.1:5000/shutdown', timeout=3)  # increased timeout
                self.status_label.setText(f'Server Status: {response.json().get("message", "Stopped")}')
            except requests.ConnectionError:
                self.status_label.setText('Server Status: Server is not running.')
            except requests.Timeout:
                self.status_label.setText('Server Status: Timeout while stopping server.')
            finally:
                server_thread = None

    @pyqtSlot()
    def check_connections(self):
        # Get the list of connections from the Flask server
        try:
            response = requests.get('http://127.0.0.1:5000/connections', timeout=5)
            connections = response.json().get('connections', [])
            self.status_label.setText(f'Server Status: Connections - {", ".join(connections) if connections else "None"}')
        except requests.ConnectionError:
            self.status_label.setText('Server Status: Server is not running.')
        except requests.Timeout:
            self.status_label.setText('Server Status: Timeout while checking connections.')

    @pyqtSlot()
    def kill_all_connections(self):
        # Send request to kill all connections
        try:
            response = requests.get('http://127.0.0.1:5000/kill', timeout=5)
            message = response.json().get('message', 'Error occurred')
            self.status_label.setText(f'Server Status: {message}')
        except requests.ConnectionError:
            self.status_label.setText('Server Status: Server is not running.')
        except requests.Timeout:
            self.status_label.setText('Server Status: Timeout while killing connections.')

    @pyqtSlot(int)
    def toggle_dark_mode(self, state):
        app = QApplication.instance()
        palette = app.palette()

        if state == Qt.Checked:
            # Updated dark mode color palette
            palette.setColor(QPalette.Window, QColor(40, 40, 40))
            palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
            palette.setColor(QPalette.Base, QColor(30, 30, 30))
            palette.setColor(QPalette.AlternateBase, QColor(50, 50, 50))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, QColor(220, 220, 220))
            palette.setColor(QPalette.Button, QColor(50, 50, 50))
            palette.setColor(QPalette.ButtonText, QColor(200, 200, 200))
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            palette = app.style().standardPalette()

        app.setPalette(palette)

    @pyqtSlot()
    def close_application(self):
        self.close()

def main():
    app = QApplication(sys.argv)
    ex = ServerControlApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
