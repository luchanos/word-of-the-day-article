class PingApp:
    """Check that the entire Application is Alive."""

    def __call__(self, *args, **kwargs):
        return {"success": True}
