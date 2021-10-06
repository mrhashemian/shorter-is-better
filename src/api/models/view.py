class View:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get("id")
        self.link_id: int = kwargs.get("link_id")
        self.browser: str = kwargs.get("browser")
        self.platform: str = kwargs.get("platform")
        self.device: str = kwargs.get("device")
        self.system: str = kwargs.get("system")
        self.ip: str = kwargs.get("ip")
        self.created_at: str = kwargs.get("created_at")
