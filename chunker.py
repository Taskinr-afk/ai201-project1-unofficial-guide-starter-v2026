"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below now splits on paragraph breaks and copies each
document's title line onto every chunk it produces. `fallback_split` is kept
underneath it — that's the starter's original fixed-window chunker, and the
thing to compare against in unit 2. Call it with explicit numbers
(`fallback_split(docs, 800, 120)`) to reproduce the original baseline, since
CHUNK_SIZE in config.py is no longer 800.

The baseline it produced, for the record:

    88 chunks, 317 characters on average (shortest 178, longest 549),
    produced by chunker.py::fallback_split

That is 88 documents coming out as 88 chunks, because almost nothing in
`campus_life` reaches 800 characters and so nothing was ever cut.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _split_title_and_body(text: str) -> tuple[str, list[str]]:
    """
    Separate a document's title line from its body paragraphs.

    Every document in `campus_life` opens with a short title line that is the
    only place the subject is named — "Laundry in Old Brewhouse", "Workload
    for CS 210 Data Structures" — and then switches to bare pronouns ("the
    machines are old"). That line is what `split_documents` copies onto every
    chunk, so it gets pulled out on its own here.
    """
    lines = text.strip().split("\n")
    title = lines[0].strip()
    rest = "\n".join(lines[1:]).strip()
    body = [p.strip() for p in re.split(r"\n\s*\n", rest) if p.strip()]
    return title, body


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split on paragraph breaks, and copy the title line onto every chunk.

    Why this, and not fixed-size windows:

    These documents are short — 317 characters on average, 549 at the longest
    — so the starter's 800-character window never cut anything, and 88
    documents came out as 88 chunks. That is the wrong default for the ones
    holding two unrelated thoughts. `dining_kestrel_commons.txt` is wait
    times in one paragraph and opening hours in the next; glued together,
    that chunk answers "when does it close?" only loosely, because half of it
    is about salad bars.

    Splitting them apart sharpens the match but risks something worse: the
    dining hall's name lives only in the title line, and this corpus has
    eight near-identical dining halls and eight housing buildings. A chunk
    reading "Hours are 7am to 9pm" with no name attached isn't vague, it's
    ambiguous between eight buildings. So every chunk carries the title line
    on its front. That is this chunker's actual idea, and it's what criterion
    4 in criteria.md checks.

    The rules, in order:
      - cut only at blank lines, never mid-sentence;
      - start a new chunk once the current one would pass CHUNK_SIZE;
      - merge anything under MIN_CHUNK_SIZE back into its neighbour, so the
        pipeline can't emit a stray fragment;
      - prefix every chunk with its document's title line.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        title, body = _split_title_and_body(doc.text)

        if not body:
            # A one-line document: the title line is all there is, so it
            # becomes the chunk rather than being prefixed to one.
            pieces = [title] if title else []
            title = ""
        else:
            pieces = []
            current = ""
            for para in body:
                candidate = f"{current}\n\n{para}" if current else para
                if (
                    current
                    and len(candidate) > config.CHUNK_SIZE
                    and len(current) >= config.MIN_CHUNK_SIZE
                ):
                    pieces.append(current)
                    current = para
                else:
                    current = candidate

            if current:
                if pieces and len(current) < config.MIN_CHUNK_SIZE:
                    pieces[-1] = f"{pieces[-1]}\n\n{current}"
                else:
                    pieces.append(current)

        for index, piece in enumerate(pieces):
            chunks.append(
                Chunk(
                    text=f"{title}\n\n{piece}" if title else piece,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
