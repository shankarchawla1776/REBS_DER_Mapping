# REBS: DER Mapping #
A project to geospatially map distributed energy resources (DERs) around the United States. This iteration currently is limited to three types of data: 
- Battery Storage
- Utility Solar
- Distributed Solar
  
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
| transmission_lines.geojson | [EIA - U.S. Energy Atlas](https://atlas.eia.gov/datasets/bd24d1a282c54428b024988d32578e59_0/explore?location=39.011484%2C-107.389808%2C7.33)     |

To view interactive map, clone this repository, install the dependencies listed in ```dependencies.txt```, then open a terminal and run: 
```
panel serve app.py --autoreload --show
```
