import os.path
import shutil
from datetime import datetime, timezone
from pathlib import Path

from git import Repo, GitCommandError
import argh
from argh import arg

from cat import Cat

FOOD_PER_COMMIT = 10.0
EXCITEMENT_PER_LINE = 0.5

HUNGER_PER_DAY = 100.0
ENERGY_PER_DAY = 100.0
BOREDOM_PER_DAY = 100.0


def _commit_changes(message: str, author='Gittycat <gittycat@example.com>'):
    repo = Repo('.')
    git = repo.git
    try:
        git.add('.gittycat/*')
    except GitCommandError:
        # Did not match any files
        return
    git.commit(message=message, author=author)
    assert not repo.bare


@arg('name', type=str, help='Name of your new cat')
@arg('--personality', type=str, help='Personality of the cat to adopt')
def adopt(name: str, **kwargs):
    """Adopts a cat into the Git Repository associated with the current working directory"""
    try:
        Path(os.path.join('.gittycat', 'cats')).mkdir(parents=True)
    except FileExistsError:
        raise FileExistsError(
            ".gittycat folder already exists for this repository! Delete the folder or use " +
            "'gittycat release' to get rid of any remaining cats.")

    cat = Cat(name)
    cat.save()
    print(f'GotSuccessfully adopted {cat.name}, your new best friend!')
    _commit_changes(f'Gittycat | Adopted new Cat "{cat.name}"')


@arg('name', type=str, help='Name of your new cat')
def status(name: str):
    """
    Gives back the current state of your cat.
    Is also used to process any new changed to the repository that were made since the last use of Gittycat
    """
    cat = Cat.load(name)
    repo = Repo('.')

    # Get days since last update, including partial days
    days_since_last_update = (datetime.now(timezone.utc) - cat.last_update).total_seconds() / 86400.0
    # Adjust cat needs based on time passed
    cat.hunger(days_since_last_update * HUNGER_PER_DAY)
    cat.bore(days_since_last_update * BOREDOM_PER_DAY)
    cat.recharge(days_since_last_update * ENERGY_PER_DAY)

    # Iterate through all commits since last update
    for commit in repo.iter_commits('HEAD'):
        # Terminate once we reach a commit older than the last update
        if commit.committed_datetime < cat.last_update:
            break
        # Exclude commits made by Gittycat itself
        if 'Gittycat' in commit.author.name:
            continue
        # Process commit
        print(f'Processing commit {commit.hexsha} by {commit.author.name} ({commit.message.strip()})')
        # Every commit feeds the cat
        cat.feed(FOOD_PER_COMMIT)
        # Every line of code makes the cat more tired
        line_changes = commit.stats.total['lines']
        cat.excite(line_changes * EXCITEMENT_PER_LINE)
        # TODO exhaustion, based on what metric?

    cat.last_update = datetime.now(timezone.utc)
    cat.save()
    _commit_changes(f'Gittycat | Updated my needs', f'{cat.name} (via Gittycat) <gittycat@example.com>')


@arg('name', type=str, help='Name of your new cat')
def pet(name: str):
    """
    Pets the cat. Very important.
    """
    cat = Cat.load(name)
    cat.pet()
    print(f'You pet your cat {name}. It purrs happily.')


def release(**kwargs):
    """
    Releases your cat into the wilds of the cloud. Use this command to remove Gittycat from your repository again.
    """
    print('Releasing all Cats into the cloud!')
    shutil.rmtree('.gittycat', ignore_errors=True)
    _commit_changes('Gittycat | Released all Cats and removed Gittycat from Repo')


if __name__ == '__main__':
    argh.dispatch_commands([adopt, status, pet, release])
