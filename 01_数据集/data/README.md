# 数据集说明

本项目当前数据集包含 4 个目标类别：

```text
0: mouse
1: laptop
2: cup
3: phone
```

## 目录结构

```text
data/
├── data.yaml
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
├── samples/
├── manifest.csv
└── conversion_summary.json
```

当前数据划分：

| 划分 | 图片 | 标签 |
| --- | ---: | ---: |
| train | 421 | 421 |
| val | 87 | 87 |
| test | 87 | 87 |

图片和标签文件使用同名规则对应。YOLO 标签每行格式为：

```text
class_id center_x center_y width height
```

坐标均为相对于图片宽高归一化后的数值。

## 数据采集建议

后续增加数据时，尽量覆盖：

- 正面、侧面、斜视和俯视角度
- 近距离、中距离和远距离
- 不同光照和不同方向的光源
- 不同桌面、背景和摆放位置
- 单个目标和多个目标同时出现
- 轻微遮挡、截断和不同旋转角度

不要让训练集、验证集和测试集只包含同一角度或同一背景。

## 标注与导出

可以使用浏览器标注工具完成矩形框标注，再导出 YOLO 检测格式。
导出后需要检查：

1. `images` 和 `labels` 下都有 `train`、`val`，如使用独立测试集则还应有 `test`。
2. 图片和标签文件名能够一一对应。
3. `data.yaml` 中的类别编号和类别名称没有改变。
4. 所有框坐标都在 `0` 到 `1` 范围内。

本项目保留了 `manifest.csv` 和 `conversion_summary.json`，用于记录数据转换和划分信息。
