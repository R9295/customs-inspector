from cleo.commands.command import Command
from poetry.installation.executor import Executor
from poetry.installation.operations import Install, Update
from poetry.plugins.application_plugin import ApplicationPlugin
import os
from customs_inspector.audit import audit


# override Executor._install
def overriden_install_func(self, operation: Update | Install):
    package = operation.package
    if package.source_type == "directory" and not self._use_modern_installation:
        return self._install_directory_without_wheel_installer(operation)

    cleanup_archive: bool = False
    if package.source_type == "git":
        archive = self._prepare_git_archive(operation)
        cleanup_archive = True
    elif package.source_type == "file":
        archive = self._prepare_archive(operation)
    elif package.source_type == "directory":
        archive = self._prepare_archive(operation)
        cleanup_archive = True
    elif package.source_type == "url":
        assert package.source_url is not None
        archive = self._download_link(operation, Link(package.source_url))
    else:
        archive = self._download(operation)

    operation_message = self.get_operation_message(operation)
    message = (
        f"  <fg=blue;options=bold>•</> {operation_message}:"
        " <info>Installing...</info>"
    )
    self._write(operation, message)

    if not self._use_modern_installation:
        return self.pip_install(archive, upgrade=operation.job_type == "update")

    try:
        if operation.job_type == "update":
            # Uninstall first
            # TODO: Make an uninstaller and find a way to rollback in case
            # the new package can't be installed
            assert isinstance(operation, Update)
            audit(
                operation.initial_package, archive, operation.package.version, self._env
            )
            self._remove(operation.initial_package)

        self._wheel_installer.install(archive)
    finally:
        if cleanup_archive:
            archive.unlink()

class CustomsInspectorPlugin(ApplicationPlugin):
    def activate(self, application):
        Executor._install = overriden_install_func
