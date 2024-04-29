import requests
from bs4 import BeautifulSoup
import os
import time

def download_file(url, path):
    """Downloads a file with safeguards against request errors and blocks."""
    with requests.Session() as session:
        session.verify = False  # Disables SSL verification

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}  # Mimic a standard browser

        try:
            response = session.get(url, timeout=10, headers=headers, verify=False)  # Disables SSL verification
            response.raise_for_status()  # Check for HTTP errors

            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"Arquivo baixado com sucesso: {path}")

        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP ao baixar o arquivo: {url} - Erro: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Erro de rede: {e}")

def main():
    base_url = 'https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior'

    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_='external-link')

        download_dir = 'Downloads'
        os.makedirs(download_dir, exist_ok=True)  # Ensure download directory exists

        for link in links:
            href = link.get('href')
            if href and 'microdados_censo_da_educacao_superior' in href and href.endswith('.zip'):
                file_name = href.split('/')[-1]
                download_path = os.path.join(download_dir, file_name)
                download_file(href, download_path)

                # Add a delay to avoid overwhelming the server
                time.sleep(2)  # Adjust sleep time as needed

    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP ao acessar a página: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Erro geral de rede: {e}")


if __name__ == '__main__':
    main()
