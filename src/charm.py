#!/usr/bin/env python3

import logging
from pathlib import Path

import ops

logger = logging.getLogger(__name__)


class ReproCharm(ops.CharmBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Uncomment this to do the reboot on install.
#        self.framework.observe(self.on.install, self._on_install)

        # secret-changed more directly shows the behaviour, because it's
        # not the event you'd expect to get first after the reboot
        self.framework.observe(self.on.secret_changed, self._on_install)
        # Need to trigger listening.
        try:
            # Obviously the secret ID will be different for everyone. I was too
            # lazy to put it in config or have the charm create it.
            self.model.get_secret(id="secret:cv72svptvhl396divtn0").get_content()
        except Exception:
            pass

    def _on_install(self, event: ops.InstallEvent) -> None:
        flag = Path("/home/ubuntu/reboot-required")
        if flag.exists():
            raise Exception("ran installation twice!")
        logger.info("rebooting unit %s", self.unit.name)
        flag.touch()
        self.unit.reboot(True)


if __name__ == "__main__":  # pragma: nocover
    ops.main(ReproCharm)
