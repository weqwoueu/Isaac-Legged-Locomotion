#!/bin/bash
echo "开始注入 Vulkan 和 NVIDIA 图形驱动 (版本 550.142.02)..."
apt update && apt install -y vulkan-tools libegl1 libxext6 libxrender1 libxrandr2 libxi6 libxkbcommon0 libxt6 libglu1-mesa libglapi-mesa libopengl0 libglx-mesa0
cp -f /你的放英伟达对应版本驱动的地址/NVIDIA-Linux-x86_64-550.142/*.so* /usr/lib/x86_64-linux-gnu/
ldconfig
mkdir -p /etc/vulkan/icd.d/
cat << 'JSON' > /etc/vulkan/icd.d/nvidia_icd.json
{
    "file_format_version" : "1.0.0",
    "ICD": {
        "library_path": "/usr/lib/x86_64-linux-gnu/libGLX_nvidia.so.550.142",
        "api_version" : "1.3.224"
    }
}
JSON
echo "注入完成！"
vulkaninfo --summary | grep "deviceName"
