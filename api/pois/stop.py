class Stop:
    def __init__(self, *, name, lat, lon, **kwargs) -> None:
        self.name = name
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f"{self.name}({self.lat}; {self.lon})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Stop):
            return NotImplemented
        return (self.name, self.lat, self.lon) == (
            value.name,
            value.lat,
            value.lon,
        )

    def __hash__(self) -> int:
        return hash((self.name, self.lat, self.lon))

    def __repr__(self):
        return f"Stop(name={self.name}, lat={self.lat}, lon={self.lon})"
