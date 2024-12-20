import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from PySide2.QtCore import *
from PySide2.QtWidgets import *

class NODE(QThread, Node):
    message_received = Signal(str)

    def __init__(self, node_name='ros_subscriber_node'):
        QThread.__init__(self)
        Node.__init__(self, node_name)

        self.subscription = self.create_subscription(
            String, 'message', self.subscription_callback, 10)

    def subscription_callback(self, msg):
        message = msg.data
        self.get_logger().info(f'Received message: {message}')
        self.message_received.emit(message)

    def run(self):
        rclpy.spin(self)


class GUI(QMainWindow):
    def __init__(self, ros_thread):
        super().__init__()
        self.ros_thread = ros_thread
        self.ros_thread.message_received.connect(self.add_message)
        self.setupUi()

    def setupUi(self):
        self.window = QMainWindow()
        if not self.window.objectName():
            self.window.setObjectName(u"MainWindow")

        self.setObjectName("MainWindow")
        self.resize(375, 310)
        
        self.centralwidget = QWidget(self)
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QRect(60, 90, 256, 192))
        
        self.setCentralWidget(self.centralwidget)

    def add_message(self, message):
        self.textBrowser.append(message)


def main():
    rclpy.init()
    node = NODE()
    node.start()

    app = QApplication(sys.argv)
    gui = GUI(node)
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()