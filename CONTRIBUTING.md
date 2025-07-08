# Contributing to YT Leechr

Thank you for your interest in contributing to YT Leechr! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a welcoming environment for all contributors

## Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/buggerman/yt-leechr.git
   cd yt-leechr
   ```

2. **Set up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

3. **Verify Setup**
   ```bash
   make test  # Run all tests
   make run   # Start the application
   ```

## Development Workflow

### Branch Strategy

- `main` - Stable release branch
- `develop` - Development integration branch
- `feature/feature-name` - Feature development
- `bugfix/issue-description` - Bug fixes
- `hotfix/critical-fix` - Critical production fixes

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style and patterns
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   make test           # Run all tests
   make test-unit      # Unit tests only
   make lint           # Check code style
   make format         # Auto-format code
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

### Commit Message Format

We use conventional commits for clear history:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(ui): add dark mode theme support
fix(download): resolve progress bar update issues
docs(readme): update installation instructions
test(manager): add download queue tests
```

## Code Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://github.com/psf/black) for code formatting
- Run `make format` before committing
- Maximum line length: 100 characters

### Code Quality

- **Type Hints**: Use type hints for function parameters and return values
- **Documentation**: Add docstrings for classes and functions
- **Error Handling**: Handle exceptions appropriately
- **Testing**: Write tests for new features and bug fixes

### Example Code Style

```python
from typing import Optional, Dict, Any

class DownloadManager:
    """Manages video download operations.
    
    This class handles the queue management and coordination
    of multiple download workers.
    """
    
    def add_download(self, url: str, settings: Dict[str, Any]) -> Optional[str]:
        """Add a new download to the queue.
        
        Args:
            url: The video URL to download
            settings: Download configuration options
            
        Returns:
            Download ID if successful, None if failed
            
        Raises:
            ValueError: If URL is invalid
        """
        if not url.strip():
            raise ValueError("URL cannot be empty")
            
        # Implementation here
        return download_id
```

## Testing Guidelines

### Test Structure

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **GUI Tests**: Test user interface functionality

### Writing Tests

1. **Test File Naming**: `test_module_name.py`
2. **Test Function Naming**: `test_function_description`
3. **Test Organization**: Group related tests in classes

```python
import pytest
from unittest.mock import Mock, patch

class TestDownloadManager:
    def test_add_download_success(self):
        """Test successful download addition."""
        manager = DownloadManager()
        download_id = manager.add_download("https://example.com", {})
        assert download_id is not None
        
    def test_add_download_invalid_url(self):
        """Test download addition with invalid URL."""
        manager = DownloadManager()
        with pytest.raises(ValueError):
            manager.add_download("", {})
```

### Test Coverage

- Aim for high test coverage (80%+)
- Test both success and failure cases
- Mock external dependencies (yt-dlp, file system, etc.)
- Use `make test` to run all tests

## Documentation

### Code Documentation

- **Docstrings**: All public classes and functions
- **Comments**: Explain complex logic and algorithms
- **Type Hints**: Use for better code understanding

### User Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md for version releases
- Include usage examples for new features

## Submitting Changes

### Pull Request Process

1. **Push Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Use a clear, descriptive title
   - Reference related issues: "Fixes #123"
   - Provide detailed description of changes
   - Include screenshots for UI changes

3. **Pull Request Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Code refactoring
   
   ## Testing
   - [ ] All tests pass
   - [ ] New tests added
   - [ ] Manual testing completed
   
   ## Screenshots (if applicable)
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   ```

### Review Process

- All PRs require review before merging
- Address reviewer feedback promptly
- Keep PRs focused and reasonably sized
- Maintain clean commit history

## Issue Reporting

### Bug Reports

Include the following information:

```markdown
**Describe the bug**
Clear description of the issue

**To Reproduce**
Steps to reproduce the behavior

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable, add screenshots

**Environment:**
- OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
- Python version: [e.g. 3.9.7]
- YT Leechr version: [e.g. 1.0.0]

**Additional context**
Any other relevant information
```

### Feature Requests

```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
Clear description of desired feature

**Describe alternatives you've considered**
Alternative solutions or features

**Additional context**
Any other relevant information
```

## Development Guidelines

### Architecture

- **Separation of Concerns**: Keep UI, business logic, and data separate
- **SOLID Principles**: Follow object-oriented design principles
- **Dependency Injection**: Use dependency injection for testability
- **Event-Driven**: Use signals/slots for component communication

### Performance

- **Threading**: Use QThread for long-running operations
- **Memory Management**: Avoid memory leaks with proper cleanup
- **Responsive UI**: Keep UI thread free from blocking operations
- **Resource Usage**: Optimize for reasonable resource consumption

### Security

- **Input Validation**: Validate all user inputs
- **File Handling**: Use secure file operations
- **External Processes**: Safely handle external process execution
- **Data Storage**: Secure handling of user data and settings

## Release Process

### Version Management

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Build and test executables
- [ ] Create release notes
- [ ] Tag release in Git
- [ ] Deploy to distribution channels

## Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community discussion
- **Code Review**: Pull request reviews and feedback

### Resources

- [PyQt6 Documentation](https://doc.qt.io/qtforpython/)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [Python Testing Guide](https://docs.python.org/3/library/unittest.html)
- [Git Best Practices](https://git-scm.com/book)

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors page

Thank you for contributing to YT Leechr! 🎉