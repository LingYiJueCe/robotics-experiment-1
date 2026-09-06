# -*- coding: utf-8 -*-

"""使用摄像头和固定帧数统计真实推理 FPS。"""

import argparse
import sys
import time
from pathlib import Path

import cv2
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args():
    parser = argparse.ArgumentParser(description="YOLO 摄像头 FPS 测试")
    parser.add_argument(
        "--model",
        type=str,
        default="02_模型/models/best.pt",
        help="YOLO 模型路径",
    )
    parser.add_argument("--camera", type=int, default=0, help="摄像头编号")
    parser.add_argument("--conf", type=float, default=0.4, help="置信度阈值")
    parser.add_argument("--imgsz", type=int, default=416, help="输入尺寸")
    parser.add_argument("--warmup", type=int, default=20, help="预热帧数")
    parser.add_argument("--frames", type=int, default=200, help="正式测试帧数")
    return parser.parse_args()


def resolve_project_path(value):
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def main():
    args = parse_args()
    model_path = resolve_project_path(args.model)

    if not model_path.is_file():
        print(f"Model file not found: {model_path}")
        return 1
    if args.warmup < 0 or args.frames <= 0:
        print("warmup must be >= 0 and frames must be > 0")
        return 1

    try:
        model = YOLO(str(model_path))
    except Exception as exc:
        print(f"Model load failed: {exc}")
        return 1

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"Cannot open camera: {args.camera}")
        return 1

    try:
        for _ in range(args.warmup):
            ok, frame = cap.read()
            if not ok:
                print("Cannot read camera frame during warmup")
                return 1
            model(frame, conf=args.conf, imgsz=args.imgsz, verbose=False)

        measured_frames = 0
        start = time.perf_counter()
        while measured_frames < args.frames:
            ok, frame = cap.read()
            if not ok:
                print("Cannot read camera frame during test")
                return 1
            model(frame, conf=args.conf, imgsz=args.imgsz, verbose=False)
            measured_frames += 1
        total_time = time.perf_counter() - start
    except Exception as exc:
        print(f"FPS test failed: {exc}")
        return 1
    finally:
        cap.release()

    average_fps = measured_frames / total_time if total_time > 0 else 0.0
    result = "PASS" if average_fps >= 5.0 else "FAIL"
    print(f"Total frames: {measured_frames}")
    print(f"Total time: {total_time:.3f} seconds")
    print(f"Average FPS: {average_fps:.2f}")
    print("Requirement: >= 5 FPS")
    print(f"Result: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
