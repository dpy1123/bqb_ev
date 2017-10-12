from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import requests
import sys
import platform
# import AppKit


TMP_FOLDER = '/var/tmp/bqb/'
HOST = 'http://45.76.4.17:8019'


def img2clipboard(img_id):
    resp = requests.get(HOST+"/get_file/"+img_id, stream=True)
    if resp.status_code == 200:
        filename = img_id + '.' + resp.headers.get('Content-Type').split('/')[1]
        print(filename)
        with open(os.path.join(TMP_FOLDER, filename), 'wb') as f:
            for chunk in resp.iter_content(1024*1024):
                f.write(chunk)
        if platform.system() == 'Darwin':
        #     pyobjc(TMP_FOLDER+filename)
        # else:
            write2clipboard('file://' + TMP_FOLDER + filename)


def write2clipboard(local_file_url):
    app = QApplication([])
    clipboard = app.clipboard()
    mine_data = QMimeData()
    mine_data.setUrls([QUrl(local_file_url)])
    clipboard.setMimeData(mine_data)

    # QTimer.singleShot(5000, Qt.CoarseTimer, app.quit)  #初始化一个单次 粗定时器
    # sys.exit(app.exec())


def pyobjc(local_file_url):
    pb = AppKit.NSPasteboard.generalPasteboard()
    pb.clearContents()
    nsurl = AppKit.NSURL.fileURLWithPath_isDirectory_(local_file_url, False)
    pb.writeObjects_([nsurl])


if __name__ == '__main__':
    os.makedirs(TMP_FOLDER, exist_ok=True)
    img2clipboard(sys.argv[1])
    print('copied!')
    # img2clipboard('e06ad7dea1e611e7b8dc784f438bc4be')
    # write2clipboard('file:///Users/dd/PycharmProjects/bqb_web/imgs/e069b692a1e611e78bee784f438bc4be.gif')
