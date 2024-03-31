# REBS: DER Mapping #
A project to geospatially map distributed energy resources (DERs) around the United States. 
  
All data is currently being hosted in the public AWS s3 bucket ```der-data-rebs```. 

You can access data with the AWS URI:

```
http(s)://s3.amazonaws.com/der-data-rebs/path/to/object
```

### s3 Bucket Breakdown
| File Name| Source  |
| -------- | ------- |
| DER_data/battery_storage.csv  | [Microsoft us_der_dataset](https://github.com/microsoft/us_der_dataset)   |
| DER_data/distributed_solar.csv | [Microsoft us_der_dataset](https://github.com/microsoft/us_der_dataset)      |
| DER_data/utility_solar.csv    | [Microsoft us_der_dataset](https://github.com/microsoft/us_der_dataset)     |
| DER_data/wind_turbines.csv   | [USWTDB](https://eerscmap.usgs.gov/uswtdb/)     |
| DER_data/full_coordinates.csv |Compilation|
| transmission_lines.geojson | [EIA - U.S. Energy Atlas](https://atlas.eia.gov/datasets/bd24d1a282c54428b024988d32578e59_0/explore?location=39.011484%2C-107.389808%2C7.33)     |

To run the project: 
1. Clone the repository 
2. Generate needed data files locally. 
```sh
cd REBS_DER_Mapping
cd daily_pricing
python write_prices
```
3. 
```sh
cd REBS_DER_Mapping
panel serve app.py --autoreload --show
```
Loading the interface may take a bit. 

