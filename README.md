# Experiment 1 Acceptance Materials

## Required deliverables

| Requirement | Included material | Location in this package |
|---|---|---|
| Dataset and annotations | 595 YOLO images/labels plus 80 independent photographs | `01_数据集/` |
| Model | Final four-class `best.pt` | `02_模型/models/best.pt` |
| Programs | Training, evaluation, real-time detection, ROS2 and Jetson deployment scripts | `03_程序/` |
| Results and typical errors | Curves, confusion matrix, independent-test records and failure images | `04_结果与错误案例/` |
| Result video | Jetson demonstration with approximately 15 FPS overlay | `05_结果视频/` |
| Running instructions | Jetson and ROS2 setup and verification commands | `06_运行说明/` |
| Experiment report | English PDF for submission; LaTeX source retained as supplementary material | `07_实验报告/` |

## Final acceptance evidence

- Four classes: mouse, laptop, cup and phone.
- Independent physical-object test: 72/80 images passed (90%).
- Jetson demonstration: approximately 15 FPS, above the 5 FPS requirement.
- ROS2 publisher: `vision_msgs/Detection2DArray` on `/detections`.
- Training starts from `yolov8n.yaml` with random initialization; no COCO or other external pretrained checkpoint is used.
