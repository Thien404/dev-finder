from utils.data_processor import query_by_language, gather_data

ORG_NAME = "codecentric"


def main():
    data = gather_data(ORG_NAME)
    matching_devs = query_by_language(data, 'java')

    print(matching_devs)


if __name__ == "__main__":
    main()
