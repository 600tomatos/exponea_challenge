from flask_restplus import Resource as OriginalResource


class ResourceItf(OriginalResource):
    """Base api resource interface  to create API controllers"""
    service = None

    def __getattr__(self, item):
        """get any attribute from service"""

        if not self.service:
            raise ValueError('No underlying service defined for this resource')
        return getattr(self.service, item)
