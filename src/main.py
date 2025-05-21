import uvicorn

from src.bootstrap import make_app  # noqa
from src.settings import get_settings


def main() -> None:
    uvicorn.run(
        app='src.bootstrap:make_app',
        # app=make_app,
        workers=6,
        host=get_settings().host,
        port=get_settings().port,
        # reload=get_settings().reload,
        log_level=get_settings().log_level,
        factory=True,
        forwarded_allow_ips='*',
    )


if __name__ == '__main__':
    main()
