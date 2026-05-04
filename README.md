🏭 Manufacturing AI Platform
A multi-tool AI platform for manufacturing workflows — featuring multimodal product prototyping and multi-agent procurement research, deployed on AWS EC2 with Kubernetes.

Overview
Manufacturing AI Platform is a Streamlit-based web application that exposes two AI-powered tools via a central landing page:
  1:- Multimodal Creator — Enter a manufacturing concept and receive a detailed technical narrative + photorealistic visual prototype generated via GPT-4o-mini and DALL·E 3, with ChromaDB for vector storage.
  2:- Multi-Agent Research — Describe your procurement needs and a CrewAI pipeline (Researcher Agent + Writer Agent) autonomously searches the web, finds suppliers, compares pricing, and produces a full procurement report using Llama 3.3 via Groq.


Browser URL's
http://13.202.61.65:8080/main-app/
http://13.202.61.65:8080/manufacturing-creator/
http://13.202.61.65:8080/multi-agent-manufacturing/
