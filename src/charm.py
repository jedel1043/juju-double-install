#!/usr/bin/env python3

import logging
from pathlib import Path

import ops

logger = logging.getLogger(__name__)


class ReproCharm(ops.CharmBase):
    _stored = ops.StoredState()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stored.set_default(installs=0)

        self.framework.observe(self.on.install, self._on_install)

    def _on_install(self, event: ops.InstallEvent) -> None:
        if Path("/var/run/reboot-required").exists():
            logger.info("rebooting unit %s", self.unit.name)
            self.unit.reboot(True)

        self._stored.installs += 1
        if self._stored.installs > 1:
            raise Exception("ran installation twice!")

        self.unit.status = ops.ActiveStatus()


if __name__ == "__main__":  # pragma: nocover
    ops.main(ReproCharm)
