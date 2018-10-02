import logging
import time
from django.conf import settings
from git import Repo


class GitClient(object):
    """docstring for GitClient"""
    repo = Repo(settings.BASE_DIR)
    git = repo.git

    def __init__(self):
        super(GitClient, self).__init__()
        self.init_timestamp = int(time.time())

    def handle_first_branch(self):
        logging.warning(f"Switching to {self.first_branch_name}")
        self.git.checkout("HEAD", b=self.first_branch_name)
        self.git.add(".")
        self.git.commit("-m", f"Branch Generated from Scaffolder at {self.init_timestamp}")
        self.ending_timestamp = int(time.time())
        logging.warning(f"Switching to {self.second_branch_name}")
        self.git.checkout("HEAD", b=self.second_branch_name)

    def handle_second_branch(self):
        self.git.add(".")
        self.git.commit("-m", f"Branch Generated from Scaffolder at {self.ending_timestamp}")
        self.git.checkout(f"{self.first_branch_name}")
        logging.warning(f"Merging {self.second_branch_name} into {self.first_branch_name}")
        self.git.merge(f"{self.second_branch_name}", "-X", "ours")
        logging.warning(f"Current working branch is {self.first_branch_name}")

    @property
    def first_branch_name(self):
        return f"scaffolder_{self.init_timestamp}_1"

    @property
    def second_branch_name(self):
        return f"scaffolder_{self.ending_timestamp}_2"
