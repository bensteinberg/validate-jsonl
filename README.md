validate-jsonl
=================

This tool is intended to be used in a GitHub Action for validating
JSONL files provided in a pull request. Install and run like this:

```
on: pull_request
jobs:
  validate-jsonl:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout the PR
        uses: actions/checkout@v3
        with:
          fetch-depth: 2
      - name: Install the validator
        run: |
          pip install git+https://github.com/bensteinberg/validate-jsonl.git
      - name: Validate files changed in the current PR
        run: |
          changedFiles=$(git diff --name-only HEAD^1 HEAD | grep '\.jsonl$')
          for file in $changedFiles; do
            echo "Processing file: $file"
            validate --schema schema.json --jsonl $file
          done
```

At the moment, you will need to include the schema in your repo; the
[example here](citations.json) is not part of the package. Note that
since the action above looks for files ending in `.json` as well as
`.jsonl`, you should add the schema to the repo before setting up the
action, or add it via push rather than pull request.
