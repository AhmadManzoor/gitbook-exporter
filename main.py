import requests
from bs4 import BeautifulSoup
import argparse
from fpdf import FPDF
from tqdm import tqdm  # Importing tqdm for progress bar

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Chapter Content", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

class ChapterExtractor:
    def __init__(self, book_url, output_file, output_format):
        self.book_url = book_url
        self.output_file = output_file
        self.output_format = output_format
        self.chapter_links_elm_selector = 'body > div > div > aside > div > ul a'
        self.content_xpath = "body > div > div > div > div > main > div:nth-of-type(1)"

    def open_main_page(self):
        print('Opening URL:', self.book_url)
        response = requests.get(self.book_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text

    def get_chapters_meta_info(self):
        print('Getting Chapters Meta Info')
        html_content = self.open_main_page()
        soup = BeautifulSoup(html_content, 'html.parser')

        res = []
        # Find all anchor tags under the specified selector
        links_elm = soup.select(self.chapter_links_elm_selector)
        
        for link in links_elm:
            href = link.get('href')
            title = link.get_text(strip=True) or 'Untitled'
            if href:
                # Append the base URL to each chapter link
                res.append({'url': self.book_url + href, 'title': title})

        return res

    def extract_text(self, url):
        try:
            html_content = requests.get(url).text
            soup = BeautifulSoup(html_content, 'html.parser')
            main_content = soup.select_one(self.content_xpath)

            if main_content:
                text_elements = []
                # Collect all text from <h2>, <p>, and <ul> elements
                text_elements += [element.get_text(strip=True) for element in main_content.find_all(['h2', 'p'])]
                text_elements += [li.get_text(strip=True) for ul in main_content.find_all('ul') for li in ul.find_all('li')]

                return ' '.join(text_elements).strip()
            else:
                return ""

        except Exception as e:
            print(f"Error extracting text from {url}: {e}")
            return ""

    def save_as_text(self):
        chapters_info = self.get_chapters_meta_info()
        total_chapters = len(chapters_info)

        with open(self.output_file, "a", encoding="utf-8") as f:
            # Using tqdm to show a progress bar
            for chapter in tqdm(chapters_info, desc="Extracting text", unit="chapter", total=total_chapters):
                title = chapter['title']
                url = chapter['url']
                extracted_text = self.extract_text(url)

                if extracted_text:  # Only write if there is extracted text
                    f.write(f"Title: {title}\n{extracted_text}\n\n")

        print(f"All extracted content written to {self.output_file}.")

    def save_as_pdf(self):
        chapters_info = self.get_chapters_meta_info()
        total_chapters = len(chapters_info)
        
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        # Add both regular and bold Unicode fonts (ensure the font files are in the same directory)
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)

        pdf.set_font("DejaVu", size=12)

        for index, chapter in tqdm(enumerate(chapters_info, start=1), desc="Extracting text", unit="chapter", total=total_chapters):
            title = chapter['title']
            url = chapter['url']
            extracted_text = self.extract_text(url)


            if extracted_text:  # Only write if there is extracted text
                pdf.set_font("DejaVu", 'B', size=14)
                pdf.cell(0, 10, f"Title: {title}", ln=True)  # Title
                pdf.set_font("DejaVu", size=12)
                pdf.multi_cell(0, 10, extracted_text.encode('latin-1', 'replace').decode('latin-1'))  # Handle encoding issues
                pdf.cell(0, 10, "", ln=True)  # Add an empty line for spacing

        pdf.output(self.output_file)
        print(f"All extracted content written to {self.output_file}.")

    def scrape_and_write(self):
        if self.output_format == 'text':
            self.save_as_text()
        elif self.output_format == 'pdf':
            self.save_as_pdf()
        else:
            print("Invalid output format. Please choose 'text' or 'pdf'.")

def main(url, output_file, output_format):
    extractor = ChapterExtractor(url, output_file, output_format)
    extractor.scrape_and_write()

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Extract content from a given URL and save to a file.')
    parser.add_argument('url', type=str, help='The URL of the main page to scrape.')
    parser.add_argument('output_file', type=str, help='The output file to save the results.')
    parser.add_argument('output_format', type=str, choices=['text', 'pdf'], help='The format to save the results (text or pdf).')

    args = parser.parse_args()
    main(args.url, args.output_file, args.output_format)
