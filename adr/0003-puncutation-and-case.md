|
[next->](0003-decision-3.md)

# 3. Remove most punctuation but keep case

Date: 2025-Mar-10

## Context

When analysing the frequency of words in the body text, puncutation may not be relavtant. But the case the case may be. Essentially when using acronyms such as HTML or PIP. Although the case may changes between uses the meaning of the word is maintained. So they should be considered the same in terms of frequency and. But is all words should be but into the same case pre-processing is less clear.

## Decision

We will maintain the case of the words and display the most commonly used case to the user. All puncutation except for apostrophes will be removed.
