import os.path
import shutil
from pathlib import Path

from git import Repo, GitCommandError
import argh
from argh import arg

from cat import Cat


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
    _commit_changes(f'Gittycat: Adopted new Cat "{cat.name}"')

    cat = Cat.load(name)
    assert cat.food == 100.0
    cat.hunger(10.0)
    cat.save()


def status(**kwargs):
    """
    Gives back the current state of your cat.
    Is also used to process any new changed to the repository that were made since the last use of Gittycat
    """
    raise NotImplementedError


def pet(**kwargs):
    """
    Pets the cat. Very important.
    """
    raise NotImplementedError


def release(**kwargs):
    """
    Releases your cat into the wilds of the cloud. Use this command to remove Gittycat from your repository again.
    """
    print('Releasing all Cats into the cloud!')
    shutil.rmtree('.gittycat', ignore_errors=True)
    _commit_changes('Gittycat: Released all Cats and removed Gittycat from Repo')


if __name__ == '__main__':
    argh.dispatch_commands([adopt, status, pet, release])
