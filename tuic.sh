#!/bin/bash
set -e

# 检查必要工具
for cmd in wget uuidgen systemctl; do
  if ! command -v $cmd &>/dev/null; then
    echo "缺少命令 $cmd，尝试安装..."
    apt update
    if [ "$cmd" = "uuidgen" ]; then
      apt install -y uuid-runtime
    else
      apt install -y $cmd
    fi
  fi
done

# 参数
PORT=4433
UUID=$(uuidgen)
PASSWORD=$(openssl rand -base64 12)
CONFIG_DIR="/etc/tuic"
BINARY_PATH="/usr/local/bin/tuic-server"
SERVICE_FILE="/etc/systemd/system/tuic.service"

echo "📥 正在安装 TUIC (IPv6-only + 免证书)..."

# 创建目录
mkdir -p $CONFIG_DIR

# 下载 TUIC Server
wget -qO $BINARY_PATH https://github.com/EAimTY/tuic/releases/latest/download/tuic-server-linux-amd64
chmod +x $BINARY_PATH

# 写配置文件
cat > $CONFIG_DIR/config.json <<EOF
{
  "server": "[::]:$PORT",
  "users": {
    "$UUID": "$PASSWORD"
  },
  "congestion_control": "bbr",
  "udp_relay_ipv6": true,
  "zero_rtt_handshake": true,
  "alpn": ["h3"],
  "certificate": "",
  "private_key": "",
  "insecure": true
}
EOF

# 写 systemd 服务文件
cat > $SERVICE_FILE <<EOF
[Unit]
Description=TUIC Server (IPv6-only Insecure)
After=network.target

[Service]
ExecStart=$BINARY_PATH -c $CONFIG_DIR/config.json
Restart=on-failure
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
EOF

# 启动并开机自启
systemctl daemon-reload
systemctl enable --now tuic

echo "✅ TUIC 安装完成"
echo "监听端口: [::]:$PORT"
echo "UUID: $UUID"
echo "密码: $PASSWORD"
echo ""
echo "systemctl status tuic 可查看服务状态"
