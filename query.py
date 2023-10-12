import requests
from urllib.parse import urlencode
import json

# Define the base URL and parameters
base_url = "http://wfs.geosampa.prefeitura.sp.gov.br/geoserver/geoportal/ows" #Especificar servicio
params_template = {
    "service": "WFS",
    "version": "1.0.0",
    "request": "GetFeature",
    "typeName": "geoportal:lote_cidadao",
    "srsName": "EPSG:31983",
    "outputFormat": "application/json"
}

extent = (313389.6701789342332631, 7343742.8202777458354831, 360618.1969658101443201, 7416156.3540473589673638)

interval = 5000

max_features_per_request = 2000

left, bottom, right, top = extent

request_count = 0

while left < right and bottom < top:
    bbox = f"{left},{bottom},{left + interval},{bottom + interval}"
    params = params_template.copy()
    params["bbox"] = bbox

    params["startIndex"] = 0

    while True:
        params["maxFeatures"] = max_features_per_request

        full_url = f"{base_url}?{urlencode(params)}"

        response = requests.get(full_url)
        response.raise_for_status()

        data = response.json()

        filename = f"bbox_{left}_{bottom}_page_{params['startIndex']}.geojson"

        with open(filename, "w") as file:
            json.dump(data, file)

        if len(data["features"]) < max_features_per_request:
            break
        params["startIndex"] += max_features_per_request

    left += interval
    if left >= right:
        left = extent[0]
        bottom += interval

    request_count += 1

# Print the total number of requests made
print(f"Total requests made: {request_count}")
