
# League

A brief description of what this project does. For example: "A tool for analyzing League of Legends games and augments."

## Installation

### Prerequisites
- Python 3.14 or higher

### Install UV
UV is a fast Python package installer and resolver. To install UV, run the following command:

**On Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**On macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For more installation options, visit the [UV installation guide](https://docs.astral.sh/uv/getting-started/installation/).

### Set Up the Project
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd league
   ```

2. Install dependencies using UV:
   ```bash
   uv sync
   ```

   This will create a virtual environment and install all required packages as specified in `pyproject.toml`.

## Usage

Provide instructions on how to run the project. For example:

To run the main application:
```bash
uv run python main.py
```

Or if using FastAPI:
```bash
uv run fastapi dev main.py
```

## Contributing

Guidelines for contributing to the project.

## License

Specify the license here.