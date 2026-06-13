import os


def get_root_path():
    """Return the path of the ``btpg`` package directory."""
    return os.path.abspath(
        os.path.join(__file__, "../..")
    )


def get_project_root():
    """Return the repository root directory (the parent of ``btpg``)."""
    return os.path.abspath(
        os.path.join(get_root_path(), "..")
    )


def get_output_path():
    """Return the unified ``output`` directory, creating it if necessary.

    All generated artifacts (e.g. ``*.btml``, ``*.dot``, ``*.png``, ``*.svg``)
    should be written here so that they stay out of the source tree.
    """
    output_path = os.path.join(get_project_root(), "output")
    os.makedirs(output_path, exist_ok=True)
    return output_path
