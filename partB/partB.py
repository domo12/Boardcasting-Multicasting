################################################################
##Read data from csv and store into server
################################################################
import csv
import requests


def clean_database():
    clean_db_url = 'http://localhost:5000/asg/clean-db'
    # Send a POST request to clean the database
    response = requests.post(clean_db_url)
    if response.status_code == 200:
        print('Database cleaned successfully')
    else:
        print('Failed to clean the database:', response.status_code, response.json())


def upload_data(csv_file_path):
    # Read data from CSV file
    data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

    # Upload data to the API
    for fan in data:
        response = requests.post(api_url, json=fan)
        if response.status_code == 201:
            print(f"Uploaded fan with code {fan['code']} successfully")
        else:
            print(f"Failed to upload fan with code {fan['code']}")


################################################################
##Donwload from from web api to csv
################################################################


def download_from_server(api_url, csv_file_path):
    # Make a GET request to the API to retrieve fan data
    response = requests.get(api_url)
    if response.status_code == 200:
        fan_data = response.json()['fans']

        # Save fan data to a CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['id', 'code', 'brand', 'type']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for fan in fan_data:
                writer.writerow(fan)
        print("Fan data downloaded and saved to 'downloaded_fans.csv'")
    else:
        print("Failed to retrieve fan data from the API")


################################################################
##Update fans through web API
################################################################
def update_server_data(api_url, csv_file_path):
    # Read data from CSV file
    csv_data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            row['id'] = row['id'].strip()
            row['code'] = row['code'].strip()
            csv_data.append(row)

    # Read data from server side
    server_data = []
    response = requests.get(api_url)
    if response.status_code == 200:
        server_data = response.json()['fans']

        # Strip leading and trailing spaces in 'code' for each fan in server_data
        for fan in server_data:
            fan['code'] = fan['code'].strip()
    else:
        print("Fail to read fan data from server")

    # Update data according to the CSV file
    for update in csv_data:
        code_to_update = update['code']
        brand_to_update = update['brand']
        fan_id_to_update = update['id']
        fan_type_to_update = update['type']

        for fan in server_data:
            if str(fan['id']) == update['id']:
                fan['code'] = code_to_update
                fan['brand'] = brand_to_update
                fan['type'] = fan_type_to_update
                break

        response = requests.put(f"{api_url}/{fan_id_to_update}",
                                json={'code': code_to_update, 'brand': brand_to_update, 'type': fan_type_to_update})

        if response.status_code == 200:
            print(f"Fan {fan_id_to_update} updated successfully")
        else:
            print(f"Failed to update fan {fan_id_to_update}")


api_url = 'http://localhost:5000/asg/fans'
clean_database()
upload_data('fans.csv')
update_server_data(api_url, "fan_naming_right.csv")
download_from_server(api_url, "downloaded_file.csv")