#!/usr/bin/env bash

# 收集 Jetson 环境信息。单项命令不存在时继续检查后续项目。

run_check() {
  label="$1"
  shift
  printf "\n[%s]\n" "$label"
  if command -v "$1" >/dev/null 2>&1; then
    "$@"
  else
    echo "TBD (command not found: $1)"
  fi
}

run_check "Jetson release" cat /etc/nv_tegra_release
run_check "Kernel" uname -a
run_check "Architecture" uname -m
run_check "Python" python3 --version
run_check "CUDA" nvcc --version
run_check "NVIDIA tools" nvidia-smi
run_check "ROS2" ros2 --version

printf "\n[ROS_DISTRO]\n"
if [ -n "${ROS_DISTRO:-}" ]; then
  echo "$ROS_DISTRO"
else
  echo "TBD"
fi

printf "\n[Video devices]\n"
video_devices=$(ls /dev/video* 2>/dev/null || true)
if [ -n "$video_devices" ]; then
  echo "$video_devices"
else
  echo "TBD (no /dev/video* found)"
fi
