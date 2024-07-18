from src.data_processor import query_by_language, gather_data

ORG_NAME = "codecentric"


def main():
    user_df = gather_data(ORG_NAME)
    matching_devs = query_by_language(user_df, 'scala')

    print(matching_devs)


if __name__ == "__main__":
    main()
