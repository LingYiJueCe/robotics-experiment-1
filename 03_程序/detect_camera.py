# -*- coding: utf-8 -*-

import argparse
import sys
import time
from collections import deque
from pathlib import Path

import cv2
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(
        description="YOLOv8n 桌面物体实时检测"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="02_模型/models/best.pt",
        help="YOLO 模型路径"
    )

    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="摄像头编号，默认 0"
    )

    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="置信度阈值，默认 0.25"
    )

    parser.add_argument(
        "--imgsz",
        type=int,
        default=416,
        help="YOLO 输入尺寸，默认 416"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    model_path = Path(args.model)
    if not model_path.is_absolute():
        model_path = Path(__file__).resolve().parents[1] / model_path

    if not model_path.exists():
        print(f"[错误] 找不到模型：{model_path}")
        sys.exit(1)

    try:
        print(f"[INFO] 正在加载模型：{model_path}")

        model = YOLO(str(model_path))

    except Exception as exc:
        print(f"[错误] 模型加载失败：{exc}")
        sys.exit(1)

    print(f"[INFO] 正在打开摄像头：{args.camera}")

    cap = cv2.VideoCapture(args.camera)

    if not cap.isOpened():
        print("[错误] 无法打开摄像头。")
        sys.exit(1)

    # 保存最近 10 帧 FPS
    fps_history = deque(maxlen=10)

    previous_time = time.perf_counter()

    print("[INFO] 实时检测已启动")
    print("[INFO] 按 q 退出")

    try:
        while True:

            ret, frame = cap.read()

            if not ret:
                print("[错误] 无法读取摄像头画面。")
                break

            # YOLO 推理，类别由当前模型决定
            results = model(
                frame,
                conf=args.conf,
                imgsz=args.imgsz,
                verbose=False
            )

            result = results[0]

            # YOLO 自动绘制框、类别、confidence
            annotated_frame = result.plot()

            # FPS
            current_time = time.perf_counter()

            elapsed = current_time - previous_time

            previous_time = current_time

            if elapsed > 0:
                fps = 1.0 / elapsed
                fps_history.append(fps)

            average_fps = (
                sum(fps_history) / len(fps_history)
                if fps_history
                else 0.0
            )

            # 在画面左上角显示 FPS
            cv2.putText(
                annotated_frame,
                f"FPS: {average_fps:.1f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            cv2.imshow(
                "YOLOv8n Desktop Object Detection",
                annotated_frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    except KeyboardInterrupt:
        print("\n[INFO] 用户终止程序。")

    except Exception as exc:
        print(f"[错误] 实时检测发生异常：{exc}")

    finally:
        cap.release()
        cv2.destroyAllWindows()

        print("[INFO] 摄像头已关闭。")


if __name__ == "__main__":
    main()
