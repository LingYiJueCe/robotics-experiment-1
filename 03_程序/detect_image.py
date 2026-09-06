# -*- coding: utf-8 -*-

import argparse
import sys
from pathlib import Path

import cv2
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args():
    parser = argparse.ArgumentParser(
        description="YOLOv8n 桌面物体图片检测"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="02_模型/models/best.pt",
        help="YOLO 模型路径"
    )

    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="待检测图片路径"
    )

    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="置信度阈值，默认 0.25"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    model_path = Path(args.model)
    image_path = Path(args.source)

    if not model_path.is_absolute():
        model_path = PROJECT_ROOT / model_path
    if not image_path.is_absolute():
        image_path = PROJECT_ROOT / image_path

    # 检查模型
    if not model_path.exists():
        print(f"[错误] 找不到模型：{model_path}")
        print("请确认模型文件已放入 models/ 目录。")
        sys.exit(1)

    # 检查图片
    if not image_path.exists():
        print(f"[错误] 找不到图片：{image_path}")
        sys.exit(1)

    try:
        print(f"[INFO] 正在加载模型：{model_path}")

        model = YOLO(str(model_path))

        print("[INFO] 开始检测")

        results = model(
            str(image_path),
            conf=args.conf,
            verbose=False
        )

        result = results[0]

        # 输出检测结果
        if result.boxes is None or len(result.boxes) == 0:
            print("[结果] 未检测到目标。")
        else:
            print(f"[结果] 共检测到 {len(result.boxes)} 个目标：")

            for i, box in enumerate(result.boxes, start=1):

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                class_name = model.names[class_id]

                print(
                    f"{i}. "
                    f"class={class_name}, "
                    f"confidence={confidence:.2f}, "
                    f"box=({int(x1)}, {int(y1)}, "
                    f"{int(x2)}, {int(y2)})"
                )

        # 生成带检测框的图像
        annotated = result.plot()

        output_dir = PROJECT_ROOT / "results" / "predictions"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{image_path.stem}_detected.jpg"

        cv2.imwrite(str(output_path), annotated)

        print(f"[完成] 检测结果已保存：{output_path}")

    except Exception as exc:
        print(f"[错误] 图片检测失败：{exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
