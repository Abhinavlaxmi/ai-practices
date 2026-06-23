Self-Hosted AI Chat Stack (Ollama + Open WebUI + FastAPI)
A fully self-hosted, privacy-focused AI Chat ecosystem running entirely on your local infrastructure. This project eliminates reliance on third-party APIs by leveraging Ollama for local LLM inference, Open WebUI for a slick user interface, and FastAPI to expose custom API endpoints.

🚀 Features
100% Local & Private: No data leaves your machine/server.

Dockerized Deployment: Simplified container management for Windows, Linux, or macOS.

ChatGPT-like UI: Powered by Open WebUI for a premium chat experience.

Custom API Layer: FastAPI integration to bridge local LLMs with external applications.

🛠️ Prerequisites
Before getting started, ensure you have the following installed on your host system:

Docker Desktop (If running on Windows, ensure WSL2 backend is enabled)

Python 3.10+ (for the FastAPI backend)

📦 Setup & Deployment Steps
Step 1: Run Ollama via Docker
Ollama serves as the local inference engine. Run the following command to download the Ollama image (~2GB) and spin up the container with a persistent volume:

Bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
-d: Runs the container in detached mode (in the background).

-v ollama:/root/.ollama: Creates a persistent volume so downloaded models aren't lost when the container stops.

-p 11434:11434: Exposes Ollama's default API port to your local machine.

Step 2: Deploy Open WebUI
To interact with Ollama via a clean, web-based chat interface, deploy Open WebUI.

Pull the latest image:

Bash
docker pull ghcr.io/open-webui/open-webui:main
Run the Open WebUI container:

Bash
docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
-p 3000:8080: Maps the web interface to http://localhost:3000.

-v open-webui:/app/backend/data: Persists your chats, users, and settings.

Step 3: Access the UI and Download a Model
Open your browser and navigate to http://localhost:3000.

Create your administrator account on the initial login screen (stored completely locally).

Browse the Ollama Model Library to choose a model (e.g., llama3, mistral, or phi3).

Import the model into the UI:

Go to Admin Panel ➔ Settings ➔ Models.

Click on the Import Model icon.

Paste the model name exactly as it appears on the Ollama site (e.g., llama3).

Click Download.

Once the download completes, go back to the chat dashboard, select your model from the dropdown, and start chatting!

🔌 Custom API Development (FastAPI)
If you want to build custom integrations or mobile/web applications instead of using the Open WebUI frontend, you can route requests through a custom FastAPI wrapper that communicates directly with the local Ollama container.

