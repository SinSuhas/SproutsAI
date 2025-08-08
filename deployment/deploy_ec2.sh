#!/bin/bash

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install python3-pip python3-venv -y

# Create application directory
sudo mkdir -p /opt/candidate-recommender
sudo chown ubuntu:ubuntu /opt/candidate-recommender

# Copy application files
cp -r ../backend /opt/candidate-recommender/
cp ../requirements.txt /opt/candidate-recommender/

# Create virtual environment
cd /opt/candidate-recommender
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service file
sudo tee /etc/systemd/system/candidate-recommender.service << EOF
[Unit]
Description=Candidate Recommender FastAPI Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/candidate-recommender
Environment="PATH=/opt/candidate-recommender/venv/bin"
ExecStart=/opt/candidate-recommender/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
EOF

# Start and enable service
sudo systemctl start candidate-recommender
sudo systemctl enable candidate-recommender