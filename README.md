# AI Poet – Poem & Article Generation Web App

A Streamlit web application for generating poems and articles about any topic, using the ai_poet Python package and the Euron LLM API.

## Features

- ✍️  Generate poems or informative articles about any topic in seconds.
- 🎨  Simple, intuitive web interface with Streamlit.
- 🔄  Modular backend logic (`ai_poet` Python package) with easy local or Docker deployment.
- 💾  Intelligent caching using SQLite (disable or clear anytime).
- 👩‍💻  Optional CLI for power users and rapid testing.
- 🔒  Easy configuration with `.env` file (API key, cache, etc).

---

## Project Structure

ai_poet/
│
├── ai_poet/                 # Your python package
│   ├── __init__.py
│   ├── generator.py
│   ├── client.py
│   ├── prompts.py
│   ├── cache.py
│   └── config.py
├── requirements.txt         # All required python libs, see below
├── .env.example             # Shows required env vars
├── app.py           # The Streamlit app frontend
├── Dockerfile
└── README.md

## Local Installation

### 1. Clone & Setup

```bash
git clone <your-repo-url>
cd your_project
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the root directory with your Euron API key:

```bash
API_KEY=your_euron_api_key
```

### 3. Run the App

```bash
streamlit run ai_poet_app.py
```

## Docker Deployment (with Docker Compose)

1. Start the App and Redis with Docker Compose

```bash
docker compose up --build
```

## This builds and runs both your AI Poet app and the Redis cache server.
## Access the app at http://localhost:8501.

2. Check Redis Cache from Inside the Container (optional)

```bash
docker exec -it redis-ai-poet redis-cli
```

# In the prompt:
```bash
keys *
```

```bash
get <key-you-see-from-above>
```
## Example:

```bash
get b3708ca850eb42b0f3e76f9ea2156afdaa7bec3d...
```

## Delete All Cache (Careful!)
If you want to clear the entire Redis cache:

```bash
flushall
```

```bash
exit
```

3. Stop All Services

```bash
docker compose down
```
## This stops the app and Redis, while preserving all cached data!

4. (Optional) Remove all data (fresh cache next time)

```bash
docker compose down -v
```
## This deletes the Redis cache volume/data completely.

## Notes

1. Do not set REDIS_HOST=localhost in .env when using Docker Compose; use REDIS_HOST=redis or leave it default.
2. All cached answers persist between runs unless you use down -v.
3. For local docker run (not compose), see the single-container instructions above.

## CLI Usage

```bash
# Generate a poem
python -m ai_poet poem "machine learning"

# Generate an article
python -m ai_poet article "deep learning"
``` 

## Cache Management

```bash
python -m ai_poet.cli cache --help
```  

## Configuration

Edit the `.env` file to customize your project.

## Development & Testing

```bash
pip install pytest
pytest
```

## File Explanations

1. ai_poet/generator.py: Logic for poem and article generation.
2. ai_poet_app.py: Streamlit web app frontend logic.
3. Dockerfile: All-in-one Docker build file.
4. requirements.txt: Python and Streamlit/package dependencies.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.    


# Install Jupyter Kernel on uv
```bash
python -m ipykernel install --user --name=langgraph-workflows --display-name "langgraph-workflows"
```

# Run Jupyter Notebook
```bash
jupyter notebook
```


