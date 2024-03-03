# REBS: DER Mapping #
A project to geospatially map distributed energy resources (DERs) around the United States. This iteration currently is limited to three types of data: 
- Battery Storage
- Utility Solar
- Distributed Solar
All data is currently being hosted in the public AWS s3 bucket ```der-data-rebs```. 

### s3 Bucket Breakdown
| File Name| Source  |
| -------- | ------- |
| January  | $250    |
| February | $80     |
| March    | $420    |


Data Sources: 
- Wind Turbines - USTWDB: https://eerscmap.usgs.gov/uswtdb/
- Utility & distributed solar - Microsoft us_der_dataset: https://github.com/microsoft/us_der_dataset
- Energy Transmission lines - EIA U.S. Energy Atlas: https://atlas.eia.gov/datasets/bd24d1a282c54428b024988d32578e59_0/explore?location=39.011484%2C-107.389808%2C7.33
- Pricing - EIA pricing API: https://www.eia.gov/developer/#:~:text=The%20EIA%20API%20is%20offered,Registration%20is%20required.


To view interactive map, clone this repository then open a terminal and run: 
```
panel serve app.py --autoreload --show
```
