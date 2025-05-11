#!/bin/bash

# --------- CONFIGURATION ---------
ENV_NAME="myenv"
APP_PATH="streamlit_app.py"
CONFIG_PATH="$HOME/.streamlit/config.toml"
# ---------------------------------

echo "🔁 Activating Conda environment: $ENV_NAME..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

echo "🔧 Ensuring Streamlit config suppresses watcher issues..."
mkdir -p "$(dirname "$CONFIG_PATH")"
cat > "$CONFIG_PATH" <<EOF
[server]
headless = true
runOnSave = true
watchFileSystem = false
EOF

echo "🚀 Launching Streamlit app from $APP_PATH..."
python -m streamlit run "$APP_PATH"

