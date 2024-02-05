#!/usr/bin/env python3

import os.path
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from git import Repo, GitCommandError
import argh
from argh import arg
from tqdm import tqdm

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


def _has_changes_since(repo: Repo, timestamp: datetime) -> bool:
    for commit in repo.iter_commits('HEAD'):
        if commit.committed_datetime > timestamp:
            return True
    return False


@arg('name', type=str, help='Name of your new cat')
@arg('--personality', type=str, help='Personality of the cat to adopt')
def adopt(name: str, personality: str = 'default', **kwargs) -> None:
    """Adopts a cat into the Git Repository associated with the current working directory"""
    try:
        Path(os.path.join('.gittycat', 'cats')).mkdir(parents=True)
    except FileExistsError:
        raise FileExistsError(
            ".gittycat folder already exists for this repository! Delete the folder or use " +
            "'gittycat release' to get rid of any remaining cats.")

    cat = Cat.create_with_personality(name, personality)
    cat.save()
    print(f'Successfully adopted {cat.name}, your new best friend!')
    cat.ascii_plot("adoption")
    _commit_changes(f'Gittycat | Adopted new Cat "{cat.name}"')


@arg('name', type=str, help='Name of new cat')
def status(name: str) -> None:
    """
    Gives back an overview of the current needs of your cat.
    """
    cat = Cat.load(name)
    repo = Repo('.')

    print('==========')
    print('Cat needs:')
    print('==========')
    meter_format = '{desc} |{bar}| ({n:06.2f}/{total:06.2f})'
    with tqdm(total=cat.max_food, desc='Food      ', file=sys.stdout, ncols=100, bar_format=meter_format) as bar:
        bar.update(cat.food)
    with tqdm(total=cat.max_food, desc='Energy    ', file=sys.stdout, ncols=100, bar_format=meter_format) as bar:
        bar.update(cat.energy)
    with tqdm(total=cat.max_food, desc='Excitement', file=sys.stdout, ncols=100, bar_format=meter_format) as bar:
        bar.update(cat.excitement)
    print(f'Current evolution stage: {cat.get_evolution_stage()}')
    print(f'Evolution: {cat.evolution:.2f} (Stage Thresholds: {cat.evolution_thresholds})')

    if cat.excitement > 66 and cat.energy > 66:
        cat.ascii_plot("excited")
    elif cat.excitement < 33 or cat.energy < 33:
        cat.ascii_plot("bored")
    else:
        cat.ascii_plot("normal")

    if _has_changes_since(repo, cat.last_update):
        print('\nYou have unprocessed commits since the last time you used Gittycat!'
              ' Use "gittycat update" to process them.')


@arg('name', type=str, help='Name of new cat')
def update(name: str) -> None:
    """Processes any commits made since this command was last used and updates the cat's needs accordingly."""
    cat = Cat.load(name)
    repo = Repo('.')

    # Get days since last update, including partial days
    days_since_last_update = (datetime.now(timezone.utc) - cat.last_update).total_seconds() / 86400.0
    # Update cat state based on time passed
    new_evolution_reached: bool = cat.update_by_time_passed(days_since_last_update)
    # Iterate through all commits since last update
    print('Processing commits since last update...')
    for commit in repo.iter_commits('HEAD'):
        # Terminate once we reach a commit older than the last update
        if commit.committed_datetime < cat.last_update:
            break
        # Exclude commits made by Gittycat itself
        if 'Gittycat' in commit.author.name:
            continue
        # Process commit
        print(f'  Processing commit {commit.hexsha} by {commit.author.name} ({commit.message.strip()})')
        # Every commit feeds the cat
        cat.feed(1)
        # Every file touched makes the cat more tired
        cat.exhaust(len(commit.stats.files.keys()))
        # Every line added to the repository make the cat more excited
        cat.excite(commit.stats.total['insertions'])
    print('Done!\n')

    cat.last_update = datetime.now(timezone.utc)
    cat.save()
    _commit_changes(f'Gittycat | Updated my needs', f'{cat.name} (via Gittycat) <gittycat@example.com>')

    if new_evolution_reached:
        print(f'What?')
        print(f'{cat.name} is evolving! They have now reached evolution stage {cat.get_evolution_stage()}!')

    status(name)


@arg('name', type=str, help='Name of your new cat')
def pet(name: str) -> None:
    """
    Pets your cat. Very important.
    """
    cat = Cat.load(name)
    cat.pet()
    _commit_changes(f'Gittycat | I got some pets. Happy times!', f'{cat.name} (via Gittycat)')
    print(f'You pet your cat {name}. It purrs happily.')


@arg('name', type=str, help='Name of your cat')
def nap(name: str) -> None:
    """
    Lets your cat take a quick nap as a manual way to recover energy for those busy coding days
    """
    cat = Cat.load(name)
    cat.nap()
    _commit_changes(f'Gittycat | I took a nap and recovered some energy', f'{cat.name} (via Gittycat)')
    print(f'Time for {name} to take a nap and recover some energy! Zzzz...')


@arg('name', type=str, help='Name of your cat')
def release(**kwargs) -> None:
    """
    Releases your cat into the wilds of the cloud. Use this command to remove Gittycat from your repository again.
    """
    print('Releasing your cat into the wild!')

    # plot the ascii
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ascii", "cat1", "0", "release.txt")
    with open(path, 'r') as file:
        content = file.read()
        print(content)
    
    shutil.rmtree('.gittycat', ignore_errors=True)
    _commit_changes('Gittycat | Released all Cats and removed Gittycat from Repo')


if __name__ == '__main__':
    argh.dispatch_commands([adopt, status, update, pet, nap, release])
