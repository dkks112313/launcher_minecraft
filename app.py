from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QSlider, QCheckBox, QFileDialog, QApplication
from PyQt6.QtCore import QSettings, QThread, Qt
import minecraft_launcher_lib
import subprocess
import file_work

version = ''
options = {
    'username': '',
    'uuid': '',
    'token': '',
    'jvmArguments': []
}
settings = {
    'snapshoot': bool(),
    'alpha': bool(),
    'console': bool(),
    'data': bool(),
    'license': bool(),
}
minecraft_directory = ''


class Launcher(QThread):
    def run(self):
        global minecraft_directory
        if options['username'] == '':
            return

        if minecraft_directory == '':
            tramp = False
            for i in minecraft_launcher_lib.utils.get_version_list()[678:]:
                if i['id'] == version:
                    tramp = True
                    break

            if tramp:
                minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', 'launch\\1.5l')
            else:
                minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', 'launch\\1.5h')

        file = file_work.FileLog(version=version)

        if file.read():
            minecraft_launcher_lib.install.install_minecraft_version(versionid=version, minecraft_directory=minecraft_directory)
            file.write()

        if version == '1.16.5':
            options['jvmArguments'].append('-Dminecraft.api.env=custom')
            options['jvmArguments'].append('-Dminecraft.api.auth.host=https://invalid.invalid/')
            options['jvmArguments'].append('-Dminecraft.api.account.host=https://invalid.invalid/')
            options['jvmArguments'].append('-Dminecraft.api.session.host=https://invalid.invalid/')
            options['jvmArguments'].append('-Dminecraft.api.services.host=https://invalid.invalid/')

        command = minecraft_launcher_lib.command.get_minecraft_command(version=version, minecraft_directory=minecraft_directory, options=options)

        if settings['console']:
            subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.jvm_box = QLineEdit()
        self.license_checkbox = QCheckBox()
        self.console_checkbox = QCheckBox()
        self.main_interface_layout = None
        self.data_checkbox = QCheckBox()
        self.alpha_checkbox = QCheckBox()
        self.ram_slider = QSlider(Qt.Orientation.Horizontal)
        self.snapshot_checkbox = QCheckBox()
        self.path_box = QLineEdit()
        self.settings_button = QPushButton("Settings")
        self.launch_button = QPushButton("Launch")
        self.version_select = QComboBox()
        self.username_edit = QLineEdit()
        self.ram_box = QLineEdit()
        self.launcher = Launcher()

        self.settings = QSettings("MyCompany", "MyApp")

        self.setGeometry(0, 0, 900, 700)
        self.setWindowTitle("Launcher")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_interface = QWidget()
        self.settings_interface = QWidget()

        self.main_layout.addWidget(self.main_interface)
        self.main_layout.addWidget(self.settings_interface)

        self.ui_init()

    def ui_init(self):
        self.main_interface_layout = QVBoxLayout()
        self.main_interface.setLayout(self.main_interface_layout)

        self.username_edit = QLineEdit()
        self.version_select = QComboBox()
        self.launch_button = QPushButton("Launch")
        self.settings_button = QPushButton("Settings")

        self.launch_button.clicked.connect(self.launch_minecraft)
        self.settings_button.clicked.connect(self.show_settings)

        for i in minecraft_launcher_lib.utils.get_version_list():
            self.version_select.addItem(i["id"])

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(QLabel("Version:"))
        bottom_layout.addWidget(self.version_select)
        bottom_layout.addWidget(self.launch_button)
        bottom_layout.addWidget(self.settings_button)

        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Username:"))
        user_layout.addWidget(self.username_edit)

        self.main_interface_layout.addStretch(1)
        self.main_interface_layout.addLayout(user_layout)
        self.main_interface_layout.addLayout(bottom_layout)

        self.load_settings()

        self.username_edit.textChanged.connect(self.save_settings)
        self.version_select.currentTextChanged.connect(self.save_settings)

        self.main_interface.setVisible(True)
        self.settings_interface.setVisible(False)

        self.init_settings_interface()

    def init_settings_interface(self):
        settings_layout = QVBoxLayout()

        path = QHBoxLayout()
        path_label = QLabel("Path")
        path_choice = QPushButton("Choice")
        path_choice.clicked.connect(self.select_directory)

        path.addWidget(path_label)
        path.addWidget(self.path_box)
        path.addWidget(path_choice)

        ram = QHBoxLayout()
        ram_slider_label = QLabel(f"RAM: {self.ram_slider.value()}")

        ram.addWidget(ram_slider_label)
        ram.addWidget(self.ram_slider)
        ram.addWidget(self.ram_box)

        jvm = QHBoxLayout()
        jvm_label = QLabel("JVM")

        jvm.addWidget(jvm_label)
        jvm.addWidget(self.jvm_box)

        licensed = QHBoxLayout()
        license_label = QLabel("License")

        licensed.addWidget(license_label)
        licensed.addWidget(self.license_checkbox)

        console = QHBoxLayout()
        console_label = QLabel("Console")

        console.addWidget(console_label)
        console.addWidget(self.console_checkbox)

        snapshot = QHBoxLayout()
        snapshot_label = QLabel("Snapshot")

        snapshot.addWidget(snapshot_label)
        snapshot.addWidget(self.snapshot_checkbox)

        alpha = QHBoxLayout()
        alpha_label = QLabel("Alpha")

        alpha.addWidget(alpha_label)
        alpha.addWidget(self.alpha_checkbox)

        data = QHBoxLayout()
        data_label = QLabel("Data")

        data.addWidget(data_label)
        data.addWidget(self.data_checkbox)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_main)

        settings_layout.addStretch(1)
        settings_layout.addLayout(path)
        settings_layout.addLayout(ram)
        settings_layout.addLayout(jvm)
        settings_layout.addLayout(licensed)
        settings_layout.addLayout(console)
        settings_layout.addLayout(snapshot)
        settings_layout.addLayout(alpha)
        settings_layout.addLayout(data)
        settings_layout.addWidget(back_button)

        self.settings_interface.setLayout(settings_layout)

        self.path_box.textChanged.connect(self.save_settings)
        self.ram_slider.valueChanged.connect(self.save_settings)
        self.ram_box.textChanged.connect(self.save_settings)
        self.snapshot_checkbox.stateChanged.connect(self.save_settings)
        self.alpha_checkbox.stateChanged.connect(self.save_settings)
        self.data_checkbox.stateChanged.connect(self.save_settings)
        self.console_checkbox.stateChanged.connect(self.save_settings)
        self.license_checkbox.stateChanged.connect(self.save_settings)
        self.jvm_box.textChanged.connect(self.save_settings)

    def show_settings(self):
        self.load_settings()
        self.main_interface.setVisible(False)
        self.settings_interface.setVisible(True)

    def show_main(self):
        self.save_settings()
        self.main_interface.setVisible(True)
        self.settings_interface.setVisible(False)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.path_box.setText(directory)

    def load_settings(self):
        self.username_edit.setText(self.settings.value("username", ""))
        self.version_select.setCurrentText(self.settings.value("version", "latest"))
        self.ram_slider.setValue(int(self.settings.value("slider_value", 0)))
        self.ram_box.setText(self.settings.value("ram", ""))
        self.snapshot_checkbox.setChecked(self.settings.value("snapshot_checkbox", "False") == "True")
        self.alpha_checkbox.setChecked(self.settings.value("alpha_checkbox", "False") == "True")
        self.path_box.setText(self.settings.value("directory", "No directory selected"))
        self.console_checkbox.setChecked(self.settings.value("console_checkbox", "False") == "True")
        self.license_checkbox.setChecked(self.settings.value("license_checkbox", "False") == "True")
        self.data_checkbox.setChecked(self.settings.value("data_checkbox", "False") == "True")
        self.jvm_box.setText(self.settings.value("jvm_box", ""))

    def save_settings(self):
        self.settings.setValue("username", self.username_edit.text())
        self.settings.setValue("version", self.version_select.currentText())
        self.settings.setValue("slider_value", self.ram_slider.value())
        self.settings.setValue("ram", self.ram_box.text())
        self.settings.setValue("snapshot_checkbox", "True" if self.snapshot_checkbox.isChecked() else "False")
        self.settings.setValue("alpha_checkbox", "True" if self.alpha_checkbox.isChecked() else "False")
        self.settings.setValue("directory", self.path_box.text())
        self.settings.setValue("console_checkbox", "True" if self.console_checkbox.isChecked() else "False")
        self.settings.setValue("license_checkbox", "True" if self.license_checkbox.isChecked() else "False")
        self.settings.setValue("data_checkbox", "True" if self.data_checkbox.isChecked() else "False")
        self.settings.setValue("jvm_box", self.jvm_box.text())

    def closeEvent(self, event):
        event.accept()

    def launch_minecraft(self):
        global version
        version = self.version_select.currentText()
        options["username"] = self.username_edit.text()

        if self.jvm_box.text():
            for arg in self.jvm_box.text().split(" "):
                options['jvmArguments'].append(arg)

        settings['console'] = self.console_checkbox.isChecked()
        settings['alpha'] = self.alpha_checkbox.isChecked()
        settings['snapshoot'] = self.snapshot_checkbox.isChecked()
        settings['data'] = self.data_checkbox.isChecked()
        settings['license'] = self.license_checkbox.isChecked()

        self.launcher.start()
