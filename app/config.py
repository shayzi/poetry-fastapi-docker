from pathlib import Path

from dynaconf import Dynaconf


def _get_settings_files() -> list[str]:
    app_root_dir = Path(__file__).parent.parent
    return [str(app_root_dir / "settings.toml")]


settings = Dynaconf(
    settings_files=_get_settings_files(),
    env_switcher="HOME_ASSIGNMENT_ENV",
    envvar_prefix="HOME_ASSIGNMENT",
    environments=True,
    load_dotenv=True,
)
