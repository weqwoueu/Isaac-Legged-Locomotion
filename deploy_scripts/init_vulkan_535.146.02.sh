#!/bin/bash
echo "开始注入 Vulkan 和 NVIDIA 图形驱动 (版本 535.146.02)..."

# 1. 安装所有必需的图形基础库
apt update && apt install -y vulkan-tools libegl1 libxext6 libxrender1 libxrandr2 libxi6 libxkbcommon0 libxt6 libglu1-mesa libglapi-mesa libopengl0 libglx-mesa0

# 2. 暴力覆盖 NVIDIA 专属动态库
cp -f /public/home/wsy1056448206/liu/NVIDIA-Linux-x86_64-535.146.02/*.so* /usr/lib/x86_64-linux-gnu/
ldconfig

# 3. 生成 Vulkan 户口本
mkdir -p /etc/vulkan/icd.d/
cat << 'JSON' > /etc/vulkan/icd.d/nvidia_icd.json
{
    "file_format_version" : "1.0.0",
    "ICD": {
        "library_path": "/usr/lib/x86_64-linux-gnu/libGLX_nvidia.so.535.146.02",
        "api_version" : "1.3.224"
    }
}
JSON

echo "注入完成！检查 Vulkan 状态："
vulkaninfo --summary | grep "deviceName"
