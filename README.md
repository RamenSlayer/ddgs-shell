# ddgs-shell
DDGS (duck duck go search) shell in python with extended functionality
## About
So you know how you can't exclude words from a search in duckduckgo? That's annoying, right? No longer shall we suffer from this oppression! So anyway that was the point of the entire project.

There are now 2! files. Oh sh!t that's what branches are for. Ah well. One is the original/full/normal/main version and the other is universal/backup/mobile version. The problem was that the original was using some lib that's just not present on android and idk how to fix that if possible. So I changed python libs (this is the third library I've tried and it actually works). Theoretically it should give less results due to the way duckduckgo works. [Unless that's a lie...](https://stackoverflow.com/questions/37012469/duckduckgo-api-getting-search-results) Well it is what it is. Now we have 2 functional versions. Cool.
## Tutorial
`!e` applies retroactively! It doesn't need to be set before searching! You can also reset it to get the original results.
## Installation
For normal version:

`pip install -r requirements.txt`, or check if your package manager provides "rich" because... it probably does.

For mobile version:

`pip install -r requirements-m.txt`
## TODO
1. Write examples because rn I don't think the usage is obvious

2. Merge files maybe? But honestly I don't want to because what's the point?

That's it.
