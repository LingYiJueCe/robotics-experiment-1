# -*- coding: utf-8 -*-

"""统计 20 次真实测试记录，不把空白记录当作正确。"""

import argparse
import csv
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args():
    parser = argparse.ArgumentParser(description="统计目标检测测试结果")
    parser.add_argument(
        "--csv",
        default="results/test_results.csv",
        help="测试结果 CSV 路径",
    )
    return parser.parse_args()


def resolve_path(value):
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def parse_bool(value):
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "pass", "正确", "是"}:
        return True
    if normalized in {"0", "false", "no", "n", "fail", "错误", "否"}:
        return False
    return None


def main():
    args = parse_args()
    csv_path = resolve_path(args.csv)
    if not csv_path.is_file():
        print(f"Test results CSV not found: {csv_path}")
        return 1

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    rows_with_ground_truth = [
        row for row in rows if str(row.get("ground_truth", "")).strip()
    ]
    evaluated_rows = [
        row
        for row in rows_with_ground_truth
        if str(row.get("prediction", "")).strip()
    ]

    correct = 0
    for row in evaluated_rows:
        recorded = parse_bool(row.get("correct", ""))
        if recorded is None:
            recorded = (
                row.get("ground_truth", "").strip().lower()
                == row.get("prediction", "").strip().lower()
            )
        correct += int(recorded)

    incorrect = len(evaluated_rows) - correct
    accuracy = (
        correct / len(evaluated_rows) * 100
        if evaluated_rows
        else None
    )

    fps_values = []
    for row in rows:
        value = str(row.get("fps", "")).strip()
        if not value:
            continue
        try:
            fps_values.append(float(value))
        except ValueError:
            print(f"忽略无法解析的 FPS: {value}")
    average_fps = sum(fps_values) / len(fps_values) if fps_values else None

    print(f"Total Samples: {len(rows_with_ground_truth)}")
    print(f"Evaluated Samples: {len(evaluated_rows)}")
    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(
        f"Accuracy: {accuracy:.2f}%"
        if accuracy is not None
        else "Accuracy: TBD"
    )
    print(
        f"Average FPS: {average_fps:.2f}"
        if average_fps is not None
        else "Average FPS: TBD"
    )

    if accuracy is None or average_fps is None:
        print("Result: TBD (真实测试记录尚未完整)")
    else:
        accuracy_result = "PASS" if accuracy >= 80.0 else "FAIL"
        fps_result = "PASS" if average_fps >= 5.0 else "FAIL"
        print(f"Accuracy requirement (>= 80%): {accuracy_result}")
        print(f"FPS requirement (>= 5): {fps_result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
