from typing import List

from data_provider import User, Engine


class UsersStorage:

    def update_black_list(self, data_source: Engine):
        pass

    def add_to_blacklist(self, user: User) -> None:
        pass

    def add_to_whitelist(self, user: User) -> None:
        pass

    def get_blacklist(self) -> List[User]:
        pass

    def get_whitelist(self) -> List[User]:
        pass
