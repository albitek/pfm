from os import path
from os import remove

from fm import store_access_token


def _delete_file_if_exists(file_name: str) -> None:
    if path.exists(file_name):
        remove(file_name)


def test_store_access_token():
    # arrange
    fake_item_id_1 = 'kPqEoxGnZXTe8NwyRQRkiejjnW7zLeSWVq6AB'
    fake_access_token_1 = 'fake-token-428cd300-1227-4524-977e-3e1f36cb1b66'
    fake_item_id_2 = 'kPqEoxGnZXTe8NwyRQRkiejjnW7zLeSWVqxxx'
    fake_access_token_2 = 'fake-token-428cd300-1227-4524-977e-3e1f36cb1bxx'
    fake_file_name = '/tmp/example_target_file.csv'
    _delete_file_if_exists(fake_file_name)

    # act
    store_access_token(item_id=fake_item_id_1, access_token=fake_access_token_1, file_name=fake_file_name)
    store_access_token(item_id=fake_item_id_2, access_token=fake_access_token_2, file_name=fake_file_name)

    # assert
    with open(fake_file_name, 'r') as file:
        lines = file.readlines()

        # make sure the number of lines is correct
        assert len(lines) == 3  # two from the first function execution and one from the second

        # make sure the first line is the header
        header = lines[0]
        assert 'item_id' in header
        assert 'access_token' in header
        assert fake_item_id_1 in lines[1]
        assert fake_access_token_1 in lines[1]
        assert fake_item_id_2 in lines[2]
        assert fake_access_token_2 in lines[2]
