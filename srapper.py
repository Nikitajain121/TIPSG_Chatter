import html2text
import requests

def do_webscraping(link):
    try:
        response = requests.get(link)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        html_content = response.text
        clean_content = html2text.html2text(html_content)

        # Write content to a text file
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(clean_content)

        # Optionally, you can also save the content as a PDF file
        # import pdfkit
        # pdfkit.from_string(clean_content, 'output.pdf')

        return {
            'summary': html_content,
            'title': response.url,
            'metadata': response.headers,
            'clean_content': clean_content
        }
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    result = do_webscraping('https://tipsg.in/')
    if result:
        print("Scraping successful!")
    else:
        print("Scraping failed.")

if __name__ == "__main__":
    main()