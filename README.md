# TextComparer

A Python-based text comparison tool that analyzes and compares text using natural language processing techniques.

## Features

- Text similarity comparison using spaCy
- Support for multiple languages
- Easy-to-use Python interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/louisgoodnews/TextComparer.git
cd TextComparer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```python
from src.core.text_comparer import TextComparer

comparer = TextComparer()
similarity = comparer.compare("First text", "Second text")
print(f"Similarity score: {similarity}")
```

## Requirements

- Python 3.8+
- spaCy 3.8.2
- Additional dependencies listed in requirements.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Authors

- Louis Goodnews