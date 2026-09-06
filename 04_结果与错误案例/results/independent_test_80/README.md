# 80 张独立实物测试

测试照片位于 `dataset/independent_test/`，共 80 张：mouse、laptop、cup、phone 各 20 张，均未用于训练。

使用 `models/best.pt`，置信度阈值 0.25。判定标准为每张照片至少检测到一个对应类别目标。

- 识别成功：72/80
- 识别率：90%
- cup：17/20
- laptop：19/20
- mouse：18/20
- phone：18/20

详细逐图结果见 `predictions.csv`，典型错误见 `errors/`。
