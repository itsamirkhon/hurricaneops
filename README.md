<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Cerebras-FF6B00?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIiIHI9IjEwIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==&logoColor=white" alt="Cerebras"/>
  <img src="https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge" alt="License"/>
</p>

<h1 align="center">🌀 HurricaneOps</h1>

<p align="center">
  <strong>AI-Powered Emergency Coordination System for Hurricane Response Operations</strong>
</p>

<p align="center">
  Real-time situational awareness, intelligent resource allocation, and rapid multi-scenario simulation powered by <strong>Cerebras</strong> ultra-fast inference.
</p>

---

## 🎯 Overview

**HurricaneOps** is an advanced emergency response coordination platform designed to assist first responders and emergency management teams during hurricane disasters. The system leverages AI to provide intelligent decision support, optimal resource allocation, and real-time situational awareness.

Built with modern web technologies and powered by Cerebras' wafer-scale compute for ultra-fast AI inference, HurricaneOps enables emergency coordinators to make data-driven decisions when every second counts.

---

## ✨ Features

### 🗺️ **Real-Time Situational Awareness**
- Interactive map with live incident tracking
- Asset positioning and status monitoring
- Weather condition overlays and flood zone visualization

### 🤖 **AI-Powered Decision Support**
- Intelligent action recommendations with confidence scores
- Multi-scenario simulation and optimization
- Natural language chat interface for emergency queries

### 🚁 **Cross-Domain Asset Coordination**
- Ground vehicles, boats, helicopters, and drones
- Medical and rescue team management
- Real-time ETA calculations and routing

### 📊 **Analytics Dashboard**
- Response time metrics and trends
- Resource utilization statistics
- Incident heatmaps and pattern analysis

### 🔄 **Dynamic Resource Allocation**
- Priority-based asset assignment
- Automated dispatch recommendations
- Capacity and constraint optimization

### 👤 **Human-in-the-Loop Decision Support**
- AI recommendations require human approval
- Confidence levels for all suggestions
- Explainable reasoning for each action

---

## 🏗️ Architecture

```
hurricaneops/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic data models
│   ├── database.py          # Database connection (SQLAlchemy)
│   ├── cerebras_client.py   # Cerebras AI client
│   ├── routers/             # API endpoints
│   │   ├── ai.py            # AI chat and analysis
│   │   ├── incidents.py     # Incident management
│   │   ├── assets.py        # Asset tracking
│   │   ├── actions.py       # Action recommendations
│   │   ├── auth.py          # Authentication
│   │   └── analytics.py     # Analytics data
│   ├── services/            # Business logic
│   │   ├── data_feeds.py    # Data feed management
│   │   ├── simulator.py     # Scenario simulation
│   │   ├── websocket.py     # Real-time updates
│   │   └── analytics.py     # Analytics processing
│   └── agents/              # AI agent system
│       ├── base.py          # Base agent class
│       ├── orchestrator.py  # Multi-agent orchestration
│       └── specialized.py   # Specialized AI agents
├── static/                  # Frontend assets
│   ├── index.html           # Main dashboard
│   ├── analytics.html       # Analytics page
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript modules
├── data/                    # Demo data and feeds
├── requirements.txt         # Python dependencies
└── .env                     # Environment configuration
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Cerebras API key ([Get one here](https://cloud.cerebras.ai))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/itsamirkhon/hurricaneops.git
   cd hurricaneops
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Cerebras API key:
   ```env
   CEREBRAS_API_KEY=your_api_key_here
   CEREBRAS_MODEL=llama-4-scout-17b-16e-instruct
   HOST=0.0.0.0
   PORT=8000
   DEBUG=false
   ```

5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. **Open the dashboard:**
   
   Navigate to [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📚 API Documentation

Once the server is running, interactive API documentation is available at:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/incidents` | GET | List all active incidents |
| `/api/incidents` | POST | Create a new incident |
| `/api/assets` | GET | List all available assets |
| `/api/ai/analyze` | POST | Get AI situation analysis |
| `/api/ai/recommend` | POST | Get AI action recommendations |
| `/api/ai/simulate` | POST | Run multi-scenario simulation |
| `/api/ai/chat` | POST | Natural language AI chat |
| `/ws` | WebSocket | Real-time updates |

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CEREBRAS_API_KEY` | Your Cerebras API key | Required |
| `CEREBRAS_MODEL` | AI model to use | `llama-4-scout-17b-16e-instruct` |
| `HOST` | Server host address | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Enable debug mode | `false` |

---

## 🧪 Testing

Run the verification scripts to ensure everything is working:

```bash
# Test authentication system
python verify_auth.py

# Test WebSocket connections
python verify_ws.py
```

---

## 📦 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI, Python 3.9+ |
| **AI Engine** | Cerebras Cloud SDK |
| **Database** | SQLAlchemy (SQLite/PostgreSQL) |
| **Real-time** | WebSockets |
| **Authentication** | JWT (python-jose), Passlib |
| **Frontend** | Vanilla HTML/CSS/JS |
| **HTTP Client** | HTTPX |

---

## 🗺️ Roadmap

- [x] **Phase 1-10:** Core platform development
- [x] **Phase 11:** Analytics Dashboard with charts and metrics
- [ ] **Phase 12:** Mobile-responsive design improvements
- [ ] **Phase 13:** Multi-agency coordination support
- [ ] **Phase 14:** Historical data analysis and reporting
- [ ] **Phase 15:** Integration with external weather APIs

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Cerebras](https://cerebras.ai) for providing ultra-fast AI inference
- [FastAPI](https://fastapi.tiangolo.com) for the excellent web framework
- First responders and emergency management professionals who inspired this project

---

<p align="center">
  <strong>Built with ❤️ for emergency responders everywhere</strong>
</p>

<p align="center">
  <a href="https://github.com/itsamirkhon/hurricaneops/issues">Report Bug</a>
  ·
  <a href="https://github.com/itsamirkhon/hurricaneops/issues">Request Feature</a>
</p>