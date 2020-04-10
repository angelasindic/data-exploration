import os
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt


def instantiate_api(user, password):
    return SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')


def find_products(api, path_aoi_geojson, start_date, end_date, processinglevel ='Level-1C', max_cloudpercentage=10):
    geojson_obj = read_geojson(path_aoi_geojson)
    geojson_obj.get('features')[0]['properties']['Name']
    print(f"Searching products for geojson located at: {path_aoi_geojson}")

    footprint = geojson_to_wkt(geojson_obj=geojson_obj)
    products = api.query(footprint,
                         date=(start_date, end_date),
                         platformname='Sentinel-2',
                         processinglevel=processinglevel,
                         cloudcoverpercentage=(0, max_cloudpercentage))

    aoi = geojson_obj.get('features')[0]['properties']['Name']

    print(f"Found {len(products)} products for {aoi}")
    return api.to_geodataframe(products)


def write_product_info(products, target_dir, filename):
    products_gdf = SentinelAPI.to_geodataframe(products)
    data = products_gdf[['uuid', 'identifier', 'filename', 'beginposition', 'endposition', 's2datatakeid']]
    path = os.path.join(target_dir, filename)
    data.to_csv(path, index=False, header=True)

def get_data_path(rel_data_dir='data'):
    abs_dir = os.getcwd()
    return os.path.join(abs_dir, rel_data_dir)

