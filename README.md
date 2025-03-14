# QuickClone
Command line utility for quickly cloning remote SCM repositories as succintly as possible.

This project is a prime example of spending 24 hours to save 2 seconds.

## Notes

Currently, only git is supported. I might add mercurial and then subversion
later.

## Installation

From source:

```shell
git clone https://github.com/RenoirTan/QuickClone.git
cd QuickClone
pip install .
```

From [PYPI](https://pypi.org):

```shell
pip install quickclone
```

Both ways should install `qkln` and `quickclone` to PATH, meaning you don't have
to call quickclone using `python -m quickclone`. `qkln` and `quickclone` are
both entry points to the same *main* function, so you can call either command.

## Configuration

You can configure QuickClone by editing `~/.config/quickclone.toml`.


## Examples

```shell
qkln RenoirTan/QuickClone
```

If `options.local.remotes_dir` is defined, QuickClone will clone the repo into
a folder in that directory. For example, if `options.local.remotes_dir` is
defined as `~/Code/remote`, the repo will be cloned to
`~/Code/remote/github.com/RenoirTan/QuickClone`.

You can also override `options.local.remotes_dir` by specifying the destination
path or adding the `-Id` flag to the command.

```shell
qkln RenoirTan/QuickClone ~/Desktop/destination
```

```shell
qkln RenoirTan/QuickClone -Id
```

In the latter example, QuickClone will ignore `options.local.remotes_dir` and
clone to `./QuickClone`.

After cloning the remote repository, QuickClone will save where the repository
was cloned to locally in a cache file. You can then use this command to see
where the last repository was cloned to:

```shell
qkln -L
```

and then cd into that directory:

```shell
cd $(qkln -L)
```

As of version 0.6, QuickClone stores a history of previously cloned repositories
instead of just one. You can specify which repository's path to print by
specifying its index in QuickClone's history:

```shell
cd $(qkln -LZ 1) # to clone the second item
```

If the `--last-clones-index/-Z` flag is set to `-1`, then the list of previously
stored repositories is printed.

```shell
qkln -LZ -1
```