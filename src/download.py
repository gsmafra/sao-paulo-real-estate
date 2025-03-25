import os
import requests

def download_files(links, download_dir):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for key, link in links.items():
        try:
            response = requests.get(link, stream=True)
            response.raise_for_status()
            filename = os.path.join(download_dir, f"{key}.xlsx")
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {link}: {e}")

if __name__ == "__main__":
    # https://capital.sp.gov.br/web/fazenda/w/acesso_a_informacao/31501
    links = {
        # "2025": "https://capital.sp.gov.br/documents/d/fazenda/guias-de-itbi-pagas-2025-",
        # to-do: 2024 file is in google sheets, so need a different way to download it
        # "2023": "https://www.prefeitura.sp.gov.br/cidade/secretarias/upload/fazenda/arquivos/XLSX/GUIAS-DE-ITBI-PAGAS-2023.xlsx",
        # "2022": "https://www.prefeitura.sp.gov.br/cidade/secretarias/upload/fazenda/arquivos/XLSX/GUIAS_DE_ITBI_PAGAS_12-2022.xlsx",
        "2021": "https://www.prefeitura.sp.gov.br/cidade/secretarias/upload/fazenda/arquivos/itbi/ITBI_Setembro_2022/GUIAS_DE_ITBI_PAGAS_(2021).xlsx",
        "2020": "https://www.prefeitura.sp.gov.br/cidade/secretarias/upload/fazenda/arquivos/itbi/ITBI_Setembro_2022/GUIAS_DE_ITBI_PAGAS_(2020).xlsx",
        "2019": "https://www.prefeitura.sp.gov.br/cidade/secretarias/upload/fazenda/arquivos/itbi/ITBI_Setembro_2022/GUIAS_DE_ITBI_PAGAS_(2019).xlsx",
        "2018": "https://www.prefeitura.sp.gov.br/cidade/secretarias/upload/fazenda/arquivos/itbi/guias_de_itbi_pagas_2018.xlsx",
        "2017": "https://www.prefeitura.sp.gov.br/cidade/secretarias/upload/fazenda/arquivos/itbi/guias_de_itbi_pagas_2017.xlsx",
    }
    download_dir = "./data"
    download_files(links, download_dir)
