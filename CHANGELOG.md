# QuickClone Changelog

## Version 0.4.0

1. Add `-L/--last-clone` flag to get the directory of the last clone operation.

## Version 0.3.0

1. Add support for mercurial.
2. Allow overriding the `vcs.remote` configuration option using the
`-S/--system` flag. Currently, this flag accepts `git`, `mercurial` or `hg`.
3. 

## Version 0.2.0

1. Add support for SCP-like locators (e.g. git@github.com:RenoirTan/QuickClone.git)
2. Add unit tests for most of the quickclone library.
3. Add `options.remote.force_scp` option to quickclone.toml.
4. Allow users to use a different config file instead of the one in `~/.config/quickclone.toml`
by using the `--config-file <path>` flag.