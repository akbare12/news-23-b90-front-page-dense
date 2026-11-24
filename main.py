#!/usr/bin/env python3
"""news-23 b90 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    return 1


def validate_png(data):
    """Validate the source PNG header manually (no PIL): signature, IHDR size,
    dimensions, bit depth / colour type, chunk CRCs, IDAT present, IEND last."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return "bad PNG signature"
    if len(data) < 33:
        return "file too short for IHDR"
    (length,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or length != 13:
        return "first chunk must be a 13-byte IHDR"
    width, height, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        return f"expected 1024x1024, got {width}x{height}"
    if depth != 8 or ctype not in (2, 6):
        return f"unexpected bit depth {depth} / colour type {ctype}"
    # Walk chunks: CRC each one, require a non-empty IDAT and a trailing IEND.
    pos, seen_idat, seen_iend = 8, False, False
    while pos + 8 <= len(data):
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype_b = data[pos + 4:pos + 8]
        end = pos + 8 + clen + 4
        if end > len(data):
            return f"truncated chunk {ctype_b!r}"
        crc_stored = struct.unpack(">I", data[end - 4:end])[0]
        crc_calc = binascii.crc32(ctype_b + data[pos + 8:pos + 8 + clen]) & 0xFFFFFFFF
        if crc_stored != crc_calc:
            return f"CRC mismatch in chunk {ctype_b!r}"
        if ctype_b == b"IDAT" and clen > 0:
            seen_idat = True
        if ctype_b == b"IEND":
            if clen != 0:
                return "IEND chunk must be empty"
            if end != len(data):
                return "trailing data after IEND"
            seen_iend = True
            break
        pos = end
    if not seen_idat:
        return "no non-empty IDAT chunk"
    if not seen_iend:
        return "no IEND chunk"
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(HERE)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR exists but is not a directory")
    if not os.path.exists(SRC):
        return fail(f"source entry.png missing: {SRC}")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) < 10000:
        return fail(f"entry.png suspiciously small: {len(data)} bytes")
    if len(data) > 1024 * 1024:
        return fail(f"entry.png over 1 MiB: {len(data)} bytes")
    err = validate_png(data)
    if err:
        return fail(err)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(SRC):
        return fail("output would overwrite the source")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        return fail("output does not match source byte-for-byte")
    print(f"wrote {dst} ({len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
