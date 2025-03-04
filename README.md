Small repro to show how `ops` version `2.18.0` runs the installation hook twice.

### To run

```shell
charmcraft pack && juju add-model repro && juju deploy ./repro_amd64.charm
```

Then, the `repro` application should block on `Exception: ran installation twice!`

Bumping the version of `ops` on the [`requirements.txt`](./requirements.txt) file to `2.18.1` fixes the issue.
