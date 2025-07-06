# Contributing to Crew United Scraper

Thank you for your interest in contributing to the Crew United Scraper project! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/crew-united-scraper.git
   cd crew-united-scraper
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/crew-united-scraper.git
   ```

## 🛠️ Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

## 🔄 Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Test your changes** thoroughly

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

## 📤 Submitting Changes

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots (if applicable)
   - Testing information

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and under 50 lines when possible

### Example Function Documentation

```python
def extract_company_data(item_element):
    """
    Extract company information from a DOM element.
    
    Args:
        item_element: Playwright element containing company data
        
    Returns:
        dict: Dictionary containing company name, location, and email
        
    Raises:
        Exception: If required elements are not found
    """
    # Implementation here
```

### Commit Message Format

Use the following format for commit messages:

```
Type: Brief description (50 chars max)

Optional longer description explaining the change in detail.
Include motivation and contrast with previous behavior.

- Bullet points for multiple changes
- Reference issues with #123
```

**Types:**
- `Add:` New features
- `Fix:` Bug fixes
- `Update:` Updates to existing functionality
- `Remove:` Removing code or features
- `Docs:` Documentation changes
- `Style:` Code style changes (formatting, etc.)
- `Test:` Adding or updating tests

## 🧪 Testing

### Manual Testing

Before submitting changes:

1. **Test the scraper** with different configurations
2. **Verify CSV output** format and content
3. **Test error handling** scenarios
4. **Check pagination** functionality

### Test Scenarios

- [ ] Login with valid credentials
- [ ] Handle invalid credentials gracefully
- [ ] Scrape companies successfully
- [ ] Scrape freelancers successfully
- [ ] Handle network timeouts
- [ ] Process pagination correctly
- [ ] Generate properly formatted CSV files

## 📚 Documentation

### Code Documentation

- Add docstrings to all functions
- Include type hints where appropriate
- Comment complex logic sections
- Update README.md for new features

### Documentation Updates

When adding new features:

1. Update the main README.md
2. Add relevant sections to this CONTRIBUTING.md
3. Update code comments and docstrings
4. Consider adding examples

## 🐛 Reporting Issues

When reporting bugs:

1. **Use the issue template** (if available)
2. **Provide detailed steps** to reproduce
3. **Include error messages** and logs
4. **Specify your environment**:
   - Operating system
   - Python version
   - Playwright version
   - Browser version

## 💡 Feature Requests

For new features:

1. **Check existing issues** first
2. **Describe the problem** you're trying to solve
3. **Propose a solution** if you have one
4. **Consider backwards compatibility**

## 🔧 Development Tips

### Debugging

- Use `headless=False` in browser launch for visual debugging
- Add `page.pause()` for interactive debugging
- Use `page.screenshot()` to capture page state
- Enable verbose logging for troubleshooting

### Performance Considerations

- Minimize DOM queries
- Use appropriate wait strategies
- Implement reasonable delays between requests
- Consider memory usage for large datasets

## 📋 Pull Request Checklist

Before submitting a PR:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No sensitive data is committed
- [ ] Changes are backwards compatible (or noted)

## 🙏 Recognition

Contributors will be recognized in:
- Project README.md
- Release notes for significant contributions
- GitHub contributors list

## 📞 Getting Help

If you need help:

1. Check existing documentation
2. Search through existing issues
3. Create a new issue with the "question" label
4. Join project discussions (if available)

Thank you for contributing to make this project better! 🎉 