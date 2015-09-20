from flask.ext import uploads
allowed = uploads.IMAGES
_config = uploads.UploadConfiguration('./Application/static/uploads/',
                                 base_url='/static/uploads/',
                                 allow=allowed,
                                 deny=())
images = uploads.UploadSet('images', allowed)
images._config = _config