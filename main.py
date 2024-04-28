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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_mainwindow.ui', self)  # Load the UI file
        
        self.sounds_dir = "pcs_sounds"
        
        self.point2 = ["Aortic Stenosis", "Bronchial breath sounds"]
        self.point3 = ["Splitting Second Heart Sound", "Fixed Splitting Second Heart Sound"]
        self.point4 = ["Aortic Regurgitation"]
        self.point5 = ["Innocent Murmur"]
        self.point6 = ["Coarse Crackles"]
        self.point7 = ["Normal Heart", "Third Heart", "Fourth Heart Sound", "Mid Systolic Click", "Mitral Valve Leaflet Prolapse",
                       "Mitral Regurgitation", "Mitral Stenosis", "Pleural Rubs"]
        self.point8 = ["Stridor"]
        self.point9 = ["Wheeze", "Rhonchi"]
        self.point10 = ["Fine Crackles", "Normal Vesicular"]
        
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
        self.stop_button.clicked.connect(lambda: self.media_player.stop())
        
        self.heart_sound_select.setChecked(True)
        self.point_selected = 'Heart'
        self.update_video_widget()

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
        
        self.lungs_sound_select.setChecked(True)
        self.play_button.setText("Play")
        
    def choose_bowel_sound(self):
        if self.bowel_sound_select.isChecked():
            self.update_image("11")
            
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
            
        if selected_combo_box:
            video_file = os.path.join(self.sounds_dir, self.point_selected.lower(), f"{selected_combo_box.currentText()}.mp4")
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_file)))
            
    def play_pause_video(self):
        if self.play_button.text() == "Play":
            self.media_player.play()
            self.play_button.setText("Pause")
        else:
            self.media_player.pause()
            self.play_button.setText("Play")

    def update_image(self, image):
        pixmap = QPixmap(r"pcs_images/" + image + r".jpg")
        self.manikin_icon.setPixmap(pixmap)
        
            
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.show()
    window.showMaximized()
    sys.exit(app.exec_())