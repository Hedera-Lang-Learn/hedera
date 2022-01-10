from webpack_loader.loader import WebpackLoader

from .settings import *  # noqa: F401, F403


# do not use workers or cache for RQ
RQ_ASYNC = False


# We need to fake webpack's stats file so that django-webpack-loader has what it needs
# to render templates. See https://github.com/django-webpack/django-webpack-loader#usage-in-tests.
class TestingWebpackLoader(WebpackLoader):
    """See https://github.com/django-webpack/django-webpack-loader/issues/187#issuecomment-901449290"""

    def get_bundle(self, bundle_name):
        """
        Effectively mocks out `render_bundle` template tag.

        Return a non-existent JS bundle for each one requested.

        Django webpack loader expects a bundle to exist for each one
        that is requested via the 'render_bundle' template tag. Since we
        don't want to store generated bundles in our repo, we need to
        override this so that the template tags will still resolve to
        something when we're running tests.

        The name and URL here don't matter, this file doesn't need to exist.
        """
        return [
            {
                "name": f"test.{bundle_name}.bundle.js",
                "url": "http://localhost:8000/static/bundles/test.bundle.js",
            }
        ]

    def get_assets(self):
        """
        Effectively mocks out `webpack_static` template tag.

        Return an empty asset stats object so that webpack_loader.utils.get_static()
        does not raise an error.
        """
        return {}


# Use a mock webpack loader class which does not actually look up webpack-stats.json,
# as it will not be present during unit tests
WEBPACK_LOADER = {
    "DEFAULT": {
        "LOADER_CLASS": "hedera.test_settings.TestingWebpackLoader",
    }
}
