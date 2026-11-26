"""
The module for the management of data across the process.
It translates SQL lines into python objects.
It translates python objects into json and json into python objects.
"""

import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .errors import SASError

_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "protocol.json"
_SCHEMA = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
_REGISTRY = Registry().with_resources([(_SCHEMA["$id"], Resource.from_contents(_SCHEMA))])

PROTOCOL_VERSION: int = _SCHEMA["$defs"]["hello"]["properties"]["protocol"]["const"]

def validator_for(name: str) -> Draft202012Validator:
    """
    returns a json validator for one of the definitions inside the schema ("$defs" fields)
    """
    return Draft202012Validator({"$ref": f"{_SCHEMA['$id']}#/$defs/{name}"}, registry=_REGISTRY)

_SERVER_MESSAGES = {
    "hello":   validator_for("hello"),
    "samples": validator_for("samples"),
    "error":   validator_for("error"),
}


class ProtocolError(SASError):
    """
    A client sent something that just don't work.
    Never fatal, just a reply saying it was wrong.
    Code 76 represents EX_PROTOCOL in sysexits.h
    """
    # In truth, the error will likely never reach main
    # becaue it will probably be handled by the thread
    exit_code = 76

@dataclass(frozen=True, slots=True)
class Data:
    """
    A single point in time's worth of data.
    """
    n: int
    t_ms: int
    stage: str | None
    values: dict[str, float | bool | str] | None

@dataclass(frozen=True, slots=True)
class Get:
    """
    A client request for data in the interval [from_n, to_n[
    """
    from_n: int
    to_n: int

@dataclass(frozen=True, slots=True)
class Hello:
    """
    Dataclass for hellos
    """
    protocol: int
    session: str
    fields: dict[str, str | None]

@dataclass(frozen=True, slots=True)
class Error:
    """
    dataclass for errors
    """
    code: str
    detail: str

def decode(line: bytes) -> Hello | list[Data] | Error:
    """
    One line from the server, checked against the schema. Raises ProtocolError if invalid.
    """
    try:
        message = json.loads(line)
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ProtocolError(f"not valid JSON: {e}") from e

    validator = _SERVER_MESSAGES.get(message.get("type")) if isinstance(message, dict) else None
    if validator is None:
        raise ProtocolError("Invalid message field")

    errors = [e.message for e in validator.iter_errors(message)]
    if errors:
        raise ProtocolError("; ".join(errors))

    match message["type"]:
        case "hello":
            return Hello(message["protocol"], message["session"], message["fields"])
        case "samples":
            return [Data(**entry) for entry in message["data"]]
        case "error":
            return Error(message["code"], message["detail"])
        case _: raise ProtocolError(f"unhandled type {message['type']}")


def _encode(message:dict) -> bytes:
    """
    Encodes python objects into valid json.
    """
    return json.dumps(message, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"

def encode_samples(entries: Sequence[Data]) -> bytes:
    """
    Encodes samples into bytes.
    """
    return _encode({"type": "samples", "data": [asdict(d) for d in entries]})

def encode_hello(session: str, fields: dict[str, str | None]):
    """
    Encodes the hello message sent to all clients on first connection.

    Session is a single timestamp that covers all restarts the server may have had.
    It differentiates sessions so that a single launch is not spread across multiple sessions.

    Fields are key-value entries that match the telemetry sent by 'samples'.
    Where 'key' is the name, 'value' is the unit.

    For example, a field named 'altitude' would have the 'm' unit, for meters.
    The list of fields should be generated at boot using the schema for the session's SQL DB.
    """
    return _encode({"type": "hello", "protocol": PROTOCOL_VERSION, "session": session, "fields": fields})

def encode_error(code: str, detail: str) -> bytes:
    """An 'error' message, sent to the one client that caused it."""
    return _encode({"type": "error", "code": code, "detail": detail})
