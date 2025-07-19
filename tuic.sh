#!/bin/bash

set -e

# 配置参数
PORT=4433
UUID=$(uuidgen)
PASSWORD=$(openssl rand -base64 12)
CONFIG_PATH="/etc/tuic"
BINARY_PATH="/usr/local/bin/tuic-server"
SERVICE_FILE="/etc/systemd/system/tuic.service"

echo "📥 正在安装 TUIC..."

# 下载 TUIC Server
mkdir -p "$CONFIG_PATH"
wget -qO "$BINARY_PATH" https://github.com/EAimTY/tuic/releases/latest/download/tuic-server-linux-amd64
chmod +x "$BINARY_PATH"

# 写入配置文件
cat > "$CONFIG_PATH/config.json" <<EOF
{
  "server": "0.0.0.0:${PORT}",
  "users": {
    "${UUID}": "${PASSWORD}"
  },
  "congestion_control": "bbr",
  "udp_relay_ipv6": false,
  "zero_rtt_handshake": true,
  "alpn": ["h3"],
  "certificate": "",
  "private_key": "",
  "insecure": true
}
EOF

# 设置 systemd 服务
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=TUIC Server (Insecure Mode)
After=network.target

[Service]
ExecStart=${BINARY_PATH} -c ${CONFIG_PATH}/config.json
Restart=on-failure
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
EOF

# 启用服务
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable --now tuic

echo
echo "✅ TUIC 安装完成 (免证书模式)"
echo "📌 端口: $PORT"
echo "📌 UUID: $UUID"
echo "📌 密码: $PASSWORD"
echo "🔧 配置文件路径: $CONFIG_PATH/config.json"
echo "🟢 TUIC 已启动并在开机时自动运行"