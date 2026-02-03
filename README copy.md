# AI-Assisted Emergency Coordination System

An AI-powered emergency response coordination system using Cerebras ultra-fast inference API for hurricane response operations in Florida.

## Quick Start

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**

   ```bash
   cp .env.example .env
   # Edit .env and add your Cerebras API key
   ```

3. **Run the server:**

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. **Open dashboard:**
   Navigate to <http://localhost:8000>

## Features

- Real-time situational awareness with interactive map
- Rapid multi-scenario simulation via Cerebras AI
- Prioritized action recommendations
- Cross-domain asset coordination (ground/air/maritime)
- Dynamic resource allocation
- Human-in-the-loop decision support

## API Documentation

Once running, visit <http://localhost:8000/docs> for interactive API documentation.
