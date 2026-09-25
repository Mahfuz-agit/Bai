# Book Knowledge Engine

PDF filenames are irrelevant to identity. A SHA-256 based content ID is used.

Outputs per book:
- `source.json`
- `knowledge.json`

Library-level output:
- `library_index.json`

The intended long-term flow is:

`raw text → atomic claims → concepts → causal/semantic relations → contradiction checks → synthesis → recall practice`
