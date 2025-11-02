
📧 Mailpit + Email CLI — Unified Dev/Test Email System

This repository provides a complete local and Kubernetes-ready Mailpit setup with a Python-based CLI email sender.
It’s ideal for development and staging environments where you need to capture, test, and inspect outgoing emails.

🧱 Folder Structure

.
├── config/
│   └── dev.env                # Environment variables for Mailpit / CLI
├── docker-compose.yml         # Docker Compose deployment
├── email_cli.py               # Python CLI tool for sending emails
├── k8s/
│   └── mailpit-deployment.yaml# Kubernetes manifest for Mailpit
└── requirements.txt           # Python dependencies


🚀 1. Quick Start — Docker Compose

Run Mailpit locally for testing SMTP + Web UI:

docker-compose up -d

Mailpit UI → http://localhost:8025
SMTP endpoint → localhost:1025

Check running containers:

docker ps

Stop and clean up:

docker-compose down -v


⚙️ 2. Configuration (config/dev.env)

Example content:

MAIL_FROM=no-reply@example.com
MAILPIT_HOST=localhost
MAILPIT_PORT=1025
SMTP_HOST=email-smtp.ap-southeast-1.amazonaws.com
SMTP_PORT=587
SMTP_USER=AKIAxxxxxx
SMTP_PASS=xxxxxxxxxxxx


💌 3. Sending Emails via CLI

Install dependencies

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Send plain text + HTML + attachment

python email_cli.py \
  --env dev \
  --to test@example.com \
  --subject "Mailpit Test" \
  --text "Hello plain text" \
  --html "<p>Hello <b>HTML</b></p>" \
  --attachments requirements.txt

✅ Message appears instantly in Mailpit’s Web UI (http://localhost:8025)


☁️ 4. Deploy to Kubernetes

Apply the manifest

kubectl apply -f k8s/mailpit-deployment.yaml

Access the UI
If using an Ingress:

http://mailpit.local

If using NodePort (Minikube or Kind):

http://localhost:38025

Check resources:

kubectl get all -n mailpit


🧹 5. Maintenance & Cleanup

Delete all messages (keep DB)

curl -X DELETE http://localhost:8025/api/v1/messages

Delete namespace completely

kubectl delete namespace mailpit


🧩 6. Tips for DevOps Integration

Use Case	Recommended Setup
CI/CD pipeline email testing	Run Mailpit as ephemeral service (Docker Compose or K8s Job)
Local testing	Use Mailpit via Compose (persistent volume ./data)
Staging environment	Deploy via Kubernetes manifest with PVC
Integration with AWS SES	Use email_cli.py --env prod for real SMTP/SES tests


🧠 Troubleshooting

Issue	Solution
ModuleNotFoundError: dotenv	Activate venv → source venv/bin/activate and run pip install python-dotenv
Connection refused	Ensure Mailpit is running and SMTP port (1025) exposed
UI empty after restart	If you use /data volume, Mailpit stores messages in mailpit.db
Kubernetes PVC error	Change storage class or delete stuck PVC using kubectl delete pvc mailpit-pvc -n mailpit

👤 Maintainer

Lumban Sopian
Strategic IT & DevOps Leader | Cloud | Security | Automation
📧 lumban.sopian@msn.com

