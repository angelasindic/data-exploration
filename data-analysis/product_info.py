def instantiate_api(user, password):
    from sentinelsat import SentinelAPI
    return SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')


def find_products(api, path_aoi_geojson, start_date, end_date,
                  level='Level-1C', min_cloudpercentage=0, max_cloudpercentage=10):
    from sentinelsat import read_geojson, geojson_to_wkt
    geojson_obj = read_geojson(path_aoi_geojson)
    geojson_obj.get('features')[0]['properties']['Name']
    print(f"Searching products for geojson located at: {path_aoi_geojson}")

    footprint = geojson_to_wkt(geojson_obj=geojson_obj)
    products = api.query(footprint,
                         date=(start_date, end_date),
                         platformname='Sentinel-2',
                         processinglevel=level,
                         cloudcoverpercentage=(min_cloudpercentage, max_cloudpercentage))

    aoi = geojson_obj.get('features')[0]['properties']['Name']

    print(f"Found {len(products)} products for {aoi}")
    return products


def write_product_info(products, target_dir, filename):
    import os.path
    from sentinelsat import SentinelAPI

    products_gdf = SentinelAPI.to_geodataframe(products)
    data = products_gdf[['uuid', 'identifier', 'filename', 'tileid', 'endposition', 'cloudcoverpercentage', 'geometry']]
    path = os.path.join(target_dir, filename)
    data.to_csv(path, index=False, header=True)
    return products_gdf


def load_product_info(prod_path, aoi_path=None, user=None, password=None):
    import os.path
    import pandas as pd

    gdf = None
    if os.path.isfile(prod_path):
        print(f"Reading product meta data from file: {prod_path}")
        gdf = pd.read_csv(prod_path)
        gdf['endposition'] = pd.to_datetime(gdf['endposition'])
    elif user is None or password is None:
        print("To retrieve product info, user and password should be provided")
    elif aoi_path is None:
        print("To retrieve product info, path to aoi should be specified")
    else:
        print(f"Retrieve product info and write it to: {prod_path}")
        api = instantiate_api(user, password)
        products = find_products(api=api, path_aoi_geojson=aoi_path, start_date='20000101', end_date='20200415', max_cloudpercentage=70)
        gdf = write_product_info(products, get_data_path('data'),  prod_path)
    return gdf


def get_timestamps(prod_path, tileid='17PKK'):
    df = load_product_info(prod_path)
    print(df.info())

    ### FILTER the tile
    data = df[df['tileid'] == tileid]
    data = data[['filename', 'endposition']]
    print(f"NaN's found: {data[data.isna().any(axis=1)].count()}")
    data.dropna(inplace=True)
    data['date'] = data['endposition'].apply(lambda ts: ts.strftime('%Y-%m-%d'))

    return data.set_index('date')['endposition'].to_dict()


def get_data_path(rel_data_dir='data'):
    import os
    abs_dir = os.getcwd()
    return os.path.join(abs_dir, rel_data_dir)


dict = get_timestamps('data/golfo_dulce_prods.csv')
print(dict)


# def get_product_path(title, timestamp, root='/eodata/Sentinel-2/MSI/L1C'):
#     path = root + '/' + timestamp.strftime('%Y/%m/%d') + '/' + title + '.SAFE'
#     return path
#
# def get_result_path(timestamp, root='/dev/shm/results/batch_run'):
#     return root + '/' + timestamp.strftime('%Y-%m-%d')
