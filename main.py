import requests
from bs4 import BeautifulSoup
import csv

# Fungsi untuk scrape data dari halaman
def scrape_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error mengakses {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Temukan semua elemen jurnal
    journals = soup.find_all('div', class_='list-item')

    data = []
    for journal in journals:
        try:
            # Ambil data yang diperlukan
            title_tag = journal.find('div', class_='affil-name').a
            title = title_tag.text.strip() if title_tag else ''

            website_tag = journal.find('div', class_='affil-abbrev').find(lambda tag: tag.name == 'a' and tag.has_attr('href') and 'Website' in tag.text)
            website = website_tag['href'] if website_tag else ''

            accreditation_tag = journal.find('span', class_='num-stat accredited')
            accreditation = accreditation_tag.text.strip() if accreditation_tag else ''

            #subject_area_tag = journal.find('div', class_='profile-id')
            #subject_area = subject_area_tag.text.strip().split(':')[-2].strip() if subject_area_tag else ''

            subject_area = journal.find('div', class_='profile-id').text.split('Subject Area :')[-1].strip()


            data.append([title, website, accreditation, subject_area])
        except AttributeError as e:
            print(f"Error mengambil data dari journal: {e}")

    return data

# Scrape data dari semua halaman
data = []
for page in range(1, 5):
    url = f'https://sinta.kemdikbud.go.id/journals?page={page}'
    print(f'Scraping {url}...')
    page_data = scrape_page(url)
    data.extend(page_data)

# Simpan data ke file CSV
try:
    with open('journals.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Nama Jurnal', 'Website Jurnal', 'Akreditasi Jurnal', 'Bidang Jurnal'])
        writer.writerows(data)
    print('Data telah disimpan ke file journals.csv')
except Exception as e:
    print(f"Error menyimpan data ke file CSV: {e}")
