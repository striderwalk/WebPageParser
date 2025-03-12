|
[next->](0003-puncutation-and-case.md)

# 2. Keep new line characters while parsing

Date: 2025-Mar-10

## Context

When parsing the HTML, the files will contain whitespace and/or newlines. This information is likely not relavtant to the data analysis of the text. But it may be usfully in future to maintain the structure. As users may want to read the whole text and the formatting both makes it easier and might be important in terms the meaning of the text.

## Decision

We will retrain the new line characters in when processing the text. This is incase the users want to be able read the whole text in future.
