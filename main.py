import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup,QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap

# 'pyrcc5 -o resources.py resources.qrc'
import resources

import paho.mqtt.client as mqtt
import threading

MQTT_BROKER_IP = "192.168.8.110"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_mainwindow.ui', self)  # Load the UI file
        
        self.sounds_dir = "pcs_sounds"
        
        self.point2 = ["H02_Aortic Stenosis", "L01_Bronchial breath sounds"]
        self.point3 = ["H11_Splitting Second Heart Sound", "H03_Fixed Splitting Second Heart Sound"]
        self.point4 = ["H01_Aortic Regurgitation"]
        self.point5 = ["H05_Innocent Murmur"]
        self.point6 = ["L02_Coarse Crackles"]
        self.point7 = ["H10_Normal Heart", "H12_Third Heart", "H04_Fourth Heart Sound", "H06_Mid Systolic Click", "H09_Mitral Valve Leaflet Prolapse",
                       "H07_Mitral Regurgitation", "H08_Mitral Stenosis", "L05_Pleural Rubs"]
        self.point8 = ["L07_Stridor"]
        self.point9 = ["L08_Wheeze", "L06_Rhonchi"]
        self.point10 = ["L03_Fine Crackles", "L04_Normal Vesicular"]
        
        self.populate_combo_box(self.heart_sounds_list, self.sounds_dir+r"\heart")
        self.populate_combo_box(self.lungs_sounds_list, self.sounds_dir+r"\lungs")
        self.populate_combo_box(self.bowel_sounds_list, self.sounds_dir+r"\bowel")
        
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget(self.cardiogram)
        
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QMediaContent())
        
        layout = QtWidgets.QVBoxLayout(self.cardiogram)
        layout.addWidget(self.video_widget)
        
        self.heart_sound_select.toggled.connect(self.heart_select)
        self.lungs_sound_select.toggled.connect(self.lungs_select)
        self.bowel_sound_select.toggled.connect(self.bowel_select)
        self.heart_sounds_list.currentIndexChanged.connect(self.choose_heart_sound)
        self.lungs_sounds_list.currentIndexChanged.connect(self.choose_lungs_sound)
        self.bowel_sounds_list.currentIndexChanged.connect(self.choose_bowel_sound)
        
        self.play_button.clicked.connect(self.play_pause_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.play_device_button.clicked.connect(self.play_on_device)
        
        self.heart_sound_select.setChecked(True)
        self.point_selected = 'Heart'
        self.update_video_widget()
        
        self.client_topic_name = 'ascultation/sounds'
        
        self.mqtt_client_thread = threading.Thread(target=self.client_thread, daemon=True)
        self.mqtt_client_thread.start()
        
    def client_thread(self):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        
        self.mqtt_client.connect(MQTT_BROKER_IP, 1883, 60)
        
        self.mqtt_client.loop_forever()

    def populate_combo_box(self, combo_box, directory):
        files = os.listdir(directory)
        for file in files:
            if file.endswith(".mp4"):
                filename = os.path.splitext(file)[0]
                combo_box.addItem(filename)
                
    def choose_heart_sound(self):
        if self.heart_sound_select.isChecked():
            text = self.heart_sounds_list.currentText()
            
            if text in self.point7:
                self.update_image("7")
            elif text in self.point2:
                self.update_image("2")
            elif text in self.point3:
                self.update_image("3")
            elif text in self.point4:
                self.update_image("4")
            else:
                self.update_image("5")
                
            self.update_video_widget()
        
        self.heart_sound_select.setChecked(True)
        self.play_button.setText("Play")
        
    def choose_lungs_sound(self):
        if self.lungs_sound_select.isChecked():
            text = self.lungs_sounds_list.currentText()
            
            if text in self.point2:
                self.update_image("2")
            elif text in self.point6:
                self.update_image("6")
            elif text in self.point7:
                self.update_image("7")
            elif text in self.point8:
                self.update_image("8")
            elif text in self.point9:
                self.update_image("9")
            else:
                self.update_image("10")
                
            self.update_video_widget()
        
        self.lungs_sound_select.setChecked(True)
        self.play_button.setText("Play")
        
    def choose_bowel_sound(self):
        if self.bowel_sound_select.isChecked():
            self.update_image("11")
            
            self.update_video_widget()
            
        self.bowel_sound_select.setChecked(True)
        self.play_button.setText("Play")
        
    def heart_select(self):
        if self.heart_sound_select.isChecked():
            self.point_selected = 'Heart'
            self.update_video_widget()
            
            text = self.heart_sounds_list.currentText()
            
            if text in self.point7:
                self.update_image("7")
            elif text in self.point2:
                self.update_image("2")
            elif text in self.point3:
                self.update_image("3")
            elif text in self.point4:
                self.update_image("4")
            else:
                self.update_image("5")
            
    def lungs_select(self):
        if self.lungs_sound_select.isChecked():
            self.point_selected = 'Lungs'
            self.update_video_widget()
            
            text = self.lungs_sounds_list.currentText()
            
            if text in self.point2:
                self.update_image("2")
            elif text in self.point6:
                self.update_image("6")
            elif text in self.point7:
                self.update_image("7")
            elif text in self.point8:
                self.update_image("8")
            elif text in self.point9:
                self.update_image("9")
            else:
                self.update_image("10")
            
    def bowel_select(self):
        if self.bowel_sound_select.isChecked():
            self.point_selected = 'Bowel'
            self.update_video_widget() 
            
            self.update_image("11")
            
    def update_video_widget(self):
        # Get the selected video file path based on the point selected
        selected_combo_box = None
        if self.point_selected == 'Heart':
            selected_combo_box = self.heart_sounds_list
        elif self.point_selected == 'Lungs':
            selected_combo_box = self.lungs_sounds_list
        elif self.point_selected == 'Bowel':
            selected_combo_box = self.bowel_sounds_list
            
        self.sound_selected = selected_combo_box.currentText()
            
        if selected_combo_box:
            video_file = os.path.join(self.sounds_dir, self.point_selected.lower(), f"{self.sound_selected}.mp4")
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_file)))
            self.media_player.play()
            self.media_player.pause()
            
    def play_pause_video(self):
        if self.play_button.text() == "Play":
            self.media_player.play()
            self.play_button.setText("Pause")
        else:
            self.media_player.pause()
            self.play_button.setText("Play")
            
    def stop_video(self):
        self.media_player.stop()
        if self.play_button.text() == "Pause":
            self.play_button.setText("Play")
            
    def play_on_device(self):
        self.mqtt_client.publish(self.client_topic_name, self.sound_selected[0:3])

    def update_image(self, image):
        pixmap = QPixmap(r"pcs_images/" + image + r".jpg")
        self.manikin_icon.setPixmap(pixmap)
        
    # Define callback functions
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.mqtt_client.subscribe("test/topic")  # Subscribe to the topic

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))  # Print received message
        
            
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.show()
    window.showMaximized()
    sys.exit(app.exec_())