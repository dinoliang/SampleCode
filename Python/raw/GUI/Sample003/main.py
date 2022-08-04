import sys, os
from PySide2.QtWidgets import QApplication, QLabel
from PySide2.QtCore    import Qt

import numpy as np

sys.path.append('/home/dino/PythonShared/raw/')
import cp_wafermap as cpwafer

if __name__ == "__main__":

    result = cpwafer.ResultHandler()
    
    # 下面指令是告訴QT，我要設計一個600(w)x100(h)大小的Label widget，上面顯示著`OKLA`
    app = QApplication(sys.argv)
    label = QLabel('OKLA')
    label.setFixedSize(300, 100)
    label.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
    label.show()

    sys.exit(app.exec_())
