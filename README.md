# Woody Pipeline Tool

## Prerequisites

- **Python**: 3.10 or higher
- **MongoDB**: Database server (local or remote)
- **Poetry**: For dependency management (recommended)

## Installation

### Step 1: Install Poetry

Poetry is the package manager for Woody.

**Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

**Alternative (pip):**
```bash
pip install poetry
```

After installation, restart your terminal or add Poetry to your PATH as instructed.

**Verify Poetry installation:**
```bash
poetry --version
```

### Step 3: Install Woody

**Option A: Using Poetry**

```bash
# Clone the repository
git clone <repository-url>
cd woody

# Install dependencies
poetry install

# Activate the virtual environment
poetry run woody
```

**Option B: Using Pip**

```bash
# Clone repository
git clone <repository-url>
cd woody

# Create virtual environment
python -m venv woody-env

# Activate environment
# Windows:
woody-env\Scripts\activate
# macOS/Linux:
source woody-env/bin/activate

# Install dependencies
pip install -e .

# Verify installation
woody --help
```