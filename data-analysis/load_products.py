import argparse
from product_info import load_product_info


def main(product_path, aoi_path, username=None, password=None):
    print("Running product info with:")
    print(f"aoi path : {aoi_path}, product path: {product_path}")
    print(f"username: {username}, password: {password}")

    if (username is not None and password is None) or (username is None and password is not None):
        print("provide both username and password or none of them")
    else:
        load_product_info(product_path, aoi_path, username, password)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    Loads product info from the given path if existing, otherwise performs api call to retrieve info.
    Loads info and stores it to given product path.
    """)
    parser.add_argument("product_path", help="location of product info to read or write")

    parser.add_argument("--aoi_path", help="location of the aoi json file")
    parser.add_argument("--username", help="username for science hub")
    parser.add_argument("--password", help="password for science hub")

    #parser.add_argument("--location", help="Location where the files are created")
    args = parser.parse_args()
    print(args)
    main(args.product_path, args.aoi_path, args.username, args.password)