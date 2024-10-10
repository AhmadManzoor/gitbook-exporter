
# GitBook Exporter

A simple command-line tool for exporting GitBook content to PDF or text formats. This tool allows users to easily convert GitBook chapters into well-formatted documents for offline reading, sharing, or printing.

## Features

- Export GitBook chapters to PDF format.
- Export GitBook chapters to plain text format.
- Handle Unicode characters, including emojis and special symbols, when generating PDFs.
- Progress tracking during the export process.

## Prerequisites

Before using this tool, ensure you have the following installed:

- Python 3.x
- pip (Python package installer)
- Git (for installing certain dependencies)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AhmadManzoor/gitbook-exporter.git
   cd gitbook-exporter
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the tool, run the following command in your terminal:

```bash
python main.py <url> <output_file> <output_format>
```

### Parameters

- `<url>`: The URL of the GitBook main page to scrape.
- `<output_file>`: The name of the output file (e.g., `output.pdf` or `output.txt`).
- `<output_format>`: The format to save the results. Choose either `text` or `pdf`.

### Example

To export a GitBook to PDF:

```bash
python main.py "https://wiki.krown.network" "output.pdf" "pdf"
```

To export a GitBook to text:

```bash
python main.py "https://wiki.krown.network" "output.txt" "text"
```

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push to the branch.
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping.
- [FPDF](http://www.fpdf.org/) for generating PDF documents.
- [tqdm](https://tqdm.github.io/) for displaying progress bars.


