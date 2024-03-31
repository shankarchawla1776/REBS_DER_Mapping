import os

def delete_csv_files(file_paths):
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")
        except OSError as e:
            print(f"Error deleting the file {file_path}: {e}")

if __name__ == "__main__":
    csv_files = [
        "ssp_prices.csv",
        "ercot_prices.csv",
        "isone_prices.csv",
        "miso_prices.csv",
        "pjm_prices.csv",
        "nyiso_prices.csv",
        "caiso_prices.csv"
    ]  
    delete_csv_files(csv_files)
