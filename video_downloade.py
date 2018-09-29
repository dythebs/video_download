import sys
import youtube_dl
from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget\
	,QPushButton, QLabel, QLineEdit, QComboBox

class MyLogger(object):
	def __init__(self, msgLabel):
		self._msgLabel = msgLabel
		
	def debug(self, msg):
		msg = msg.replace('\n', '')
		self._msgLabel.setText(msg)
		self._msgLabel.adjustSize()

	def warning(self, msg):
		msg = msg.replace('\n', '')
		self._msgLabel.setText(msg)
		self._msgLabel.adjustSize()

	def error(self, msg):
		msg = msg.replace('\n', '')
		self._msgLabel.setText(msg)
		self._msgLabel.adjustSize()

class Downloader():
	def download(url, port, model, msgLabel):
		if url == '':
			return
		opt = {'outtmpl': '%(title)s.%(ext)s',
				'logger':MyLogger(msgLabel)}
		if model == '均衡':
			opt['format'] = 'best[height<=?480]'
		elif model == '画质优先':
			opt['format'] = 'best'
		elif model == '速度优先':
			opt['format'] = 'worst'
		if port != '':
			opt['proxy'] = '127.0.0.1:' + port

		ydl_opts = (opt)
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			video = ydl.download([url])

class VideoDownLoadUi(QWidget):
	def __init__(self):
		super().__init__()
		self._port = ''
		self._url = ''
		self._model = '均衡'
		self.initUI()

	def initUI(self):
		self.setWindowTitle('Video Download')
		self.setFixedSize(600, 190)

		startBtn = QPushButton('下载', self)
		startBtn.resize(startBtn.sizeHint())
		startBtn.move(450, 73)
		startBtn.clicked.connect(self.startClicked)

		lbl1 = QLabel('视频地址', self)
		lbl1.move(10, 40)
		lbl2 = QLabel('本地代理端口', self)
		lbl2.move(10, 80)

		lbl3 = QLabel('模式', self)
		lbl3.move(250, 80)

		msgLabel = QLabel('空闲', self)
		msgLabel.move(10, 120)
		self._msgLabel = msgLabel

		urlEdit = QLineEdit(self)
		urlEdit.textChanged[str].connect(self.urlChanged)
		urlEdit.move(100, 38)
		urlEdit.setFixedSize(490, 22)

		portEdit = QLineEdit(self)
		portEdit.textChanged[str].connect(self.portChanged)
		portEdit.move(120, 78)
		portEdit.setFixedSize(100, 22)
		
		combo = QComboBox(self)
		combo.addItem("画质优先")
		combo.addItem("均衡")
		combo.addItem("速度优先")
		combo.setCurrentIndex(1)
		combo.move(300, 78)
		combo.activated[str].connect(self.onActivated)

		self.show()

	def startClicked(self):
		Thread(target=Downloader.download, args=(self._url, self._port, self._model, self._msgLabel)).start()

	def portChanged(self, text):
		self._port = text

	def urlChanged(self, text):
		self._url = text

	def onActivated(self, text):
		self._model = text


app = QApplication(sys.argv)
ex = VideoDownLoadUi()
sys.exit(app.exec_())