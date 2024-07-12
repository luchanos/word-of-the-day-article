class PingApp:
    """Check that en entire Application is Alive."""

    def __call__(self, *args, **kwargs):
        return {"success": True}
