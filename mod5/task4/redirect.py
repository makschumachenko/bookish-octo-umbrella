import sys
from contextlib import contextmanager

@contextmanager
def Redirect(*args, **kwargs):
    original_streams = {}
    for stream_name in kwargs:
        original_streams[stream_name] = getattr(sys, stream_name)
        setattr(sys, stream_name, kwargs[stream_name])

    try:
        yield
    finally:
        for stream_name, original_stream in original_streams.items():
            setattr(sys, stream_name, original_stream)
