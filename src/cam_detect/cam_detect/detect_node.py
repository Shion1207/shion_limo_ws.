
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO

class CameraDetect(Node):
    def __init__(self):
        super().__init__('camera_detect')
        self.bridge = CvBridge()
        
        self.get_logger().info("Đang khởi tạo Model YOLOv8...")

        self.model = YOLO('yolov8n.pt') 

        self.subscription = self.create_subscription(
            Image,
            '/cam1/image_raw',   
            self.image_callback,
            10)

        self.get_logger().info("YOLOv8 Tracking Node đã khởi động và đang đợi ảnh!")

    def image_callback(self, msg):
        # Chuyển đổi từ ROS Image sang OpenCV
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        results = self.model.track(frame, persist=True, conf=0.5, iou=0.5, verbose=False)


        if results[0].boxes.id is not None:
            annotated_frame = results[0].plot()
        else:
            annotated_frame = frame

        # Show
        cv2.imshow("YOLOv8 Real-time Tracking", annotated_frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = CameraDetect()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
