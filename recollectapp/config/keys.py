

class Keys:
    """
    Centralize Redis keys used throughout app.
    """

    def __init__(self, prefix: str):
        # Prefix for all redis keys in app.
        self.prefix = prefix

    def pre(self, s: str) -> str:
        return f"{self.prefix}:{s}"

    def github_repo(self, owner: str, repo_name: str) -> str:
        return f"{self.prefix}:resource:github:{owner}:{repo_name}"

    def github_repo_lists(self, owner: str, repo_name: str) -> str:
        return f"{self.prefix}:resource:github:{owner}:{repo_name}:lists"

    def language_list(self) -> str:
        return f"{self.prefix}:resource:data:languages"

    def awesome_list_list(self) -> str:
        return f"{self.prefix}:resource:data:awesome_lists"
