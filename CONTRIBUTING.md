# Contributing to AssetGuard

First off, thank you for considering contributing to AssetGuard! It's people like you that make AssetGuard such a great tool for Security Operations Centers (SOCs) and system administrators.

## 1. Where do I go from here?

If you've noticed a bug or have a feature request, please **open an issue** on GitHub. It's best if you can provide a clear and descriptive title, steps to reproduce the issue, and the expected outcome.

If you'd like to submit code, please follow the steps below.

## 2. Setting up your local environment

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/<your-username>/assetguard.git
   cd assetguard
   ```
3. **Set up a virtual environment** and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   Copy the example environment file and configure it:
   ```bash
   cp .env.example .env
   ```
   (Generate a secure `SECRET_KEY` and fill it in `.env`)
5. **Run migrations and create a superuser**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

## 3. Making a Pull Request

1. **Create a branch**: `git checkout -b feature/your-feature-name` or `bugfix/issue-description`
2. **Commit your changes**: Make sure your commit messages are descriptive.
3. **Push to your fork**: `git push origin feature/your-feature-name`
4. **Submit a Pull Request**: Go to the original AssetGuard repository and click "New Pull Request".

## 4. Code Style & Standards

- **Python**: We follow standard PEP 8 conventions for Django.
- **Frontend**: The project uses vanilla CSS with a glassmorphic Cyber-Enterprise design system (refer to `base.html` for CSS variables). Please reuse existing `.glass-card` classes where possible.

We look forward to reviewing your contributions!
