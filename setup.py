"""Include the release model when building directly from the public Git tag."""

from __future__ import annotations

import re
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info

ROOT = Path(__file__).parent
MODEL = ROOT / "src" / "sentiment_app" / "modele" / "sentiment.joblib"
MODEL_IN_WHEEL = "sentiment_app/modele/sentiment.joblib"


def ensure_model() -> None:
    if MODEL.is_file():
        return
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'(?m)^version\s*=\s*"([^"]+)"\s*$', pyproject)
    if match is None:
        raise RuntimeError("Impossible de trouver la version du paquet dans pyproject.toml")
    version = match.group(1)
    wheel_url = (
        "https://github.com/bouthaina2004/sentiment-app/releases/download/"
        f"v{version}/sentiment_app-{version}-py3-none-any.whl"
    )
    request = Request(wheel_url, headers={"User-Agent": "sentiment-app-build"})
    try:
        with urlopen(request, timeout=30) as response:
            wheel = response.read()
        with ZipFile(BytesIO(wheel)) as archive:
            model = archive.read(MODEL_IN_WHEEL)
    except Exception as error:
        raise RuntimeError(
            f"Modèle absent et téléchargement impossible depuis {wheel_url}"
        ) from error
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    MODEL.write_bytes(model)


class ModelBuildPy(build_py):
    def run(self) -> None:
        ensure_model()
        super().run()


class ModelEggInfo(egg_info):
    def run(self) -> None:
        ensure_model()
        super().run()


setup(cmdclass={"build_py": ModelBuildPy, "egg_info": ModelEggInfo})
