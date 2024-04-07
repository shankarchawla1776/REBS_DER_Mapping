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
        "daily_pricing/miso_prices.csv",
        "daily_pricing/nyiso_prices.csv",
        "daily_pricing/caiso_prices.csv"
    ]  
    delete_csv_files(csv_files)
