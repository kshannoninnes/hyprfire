class PacketRangeExportError(ValueError):
    """Exception raised for issues when trying to export a range of packets to a file"""


class JSONError(ValueError):
    """Exception raised when there's an error with JSON encoding/decoding"""
