# REBS: DER Mapping in the CAISO #
A project meant to geospatially map distributed energy resources (DERs) around the United States. This iteration is currently limited to the California Independent System Operator (CAISO). 
Corrdinate data is currently stored in an AWS S3 bucket, but will be tranisitioned to a PostGIS database. 

Data Sources: 
- Wind Turbines - USTWDB: https://eerscmap.usgs.gov/uswtdb/
- Utility & distributed solar - Microsoft us_der_dataset: https://github.com/microsoft/us_der_dataset
- Energy Transmission lines - EIA U.S. Energy Atlas: https://atlas.eia.gov/datasets/bd24d1a282c54428b024988d32578e59_0/explore?location=39.011484%2C-107.389808%2C7.33
- Pricing - EIA pricing API: https://www.eia.gov/developer/#:~:text=The%20EIA%20API%20is%20offered,Registration%20is%20required.


To view interactive map, clone this repository then open a terminal and run: 

```
panel serve ds.py --autoreload --show
```