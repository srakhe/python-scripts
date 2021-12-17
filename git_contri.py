import random
import sys
from datetime import datetime, timedelta
import git
from time import altzone
from io import BytesIO
from gitdb import IStream

REPO_PATH = "../history/"


def process_date(dt_str):
    date = datetime.strptime(dt_str, "%d/%m/%Y")
    return date


def generate_history(date):
    repo = git.Repo(REPO_PATH)
    index = repo.index
    message = f"Commit on {date.date()}"
    print(message)
    tree = index.write_tree()
    parents = [repo.head.commit]
    config = repo.config_reader()
    committer = git.Actor.committer(config)
    author = git.Actor.author(config)
    time = int(date.strftime('%s'))
    author_time, author_offset = time, altzone
    committer_time, committer_offset = time, altzone
    conf_encoding = "UTF-8"
    commit = git.Commit
    new_commit = commit(repo, commit.NULL_BIN_SHA, tree,
                        author, author_time, author_offset,
                        committer, committer_time, committer_offset,
                        message, parents, conf_encoding)

    stream = BytesIO()
    new_commit._serialize(stream)
    streamlen = stream.tell()
    stream.seek(0)
    istream = repo.odb.store(IStream(commit.type, streamlen, stream))
    new_commit.binsha = istream.binsha
    repo.head.set_commit(new_commit)


def start(from_dt, to_dt, n_comm):
    from_dt = process_date(from_dt)
    to_dt = process_date(to_dt)
    delta = timedelta(days=1)
    while from_dt <= to_dt:
        from_dt += delta
        num_commit = random.randint(0, int(n_comm))
        print(num_commit)
        for i in range(0, num_commit):
            generate_history(from_dt)


if __name__ == "__main__":
    date_from = sys.argv[1]
    date_to = sys.argv[2]
    max_commits = sys.argv[3]
    start(date_from, date_to, max_commits)
