# ddgs-shell
DDGS (duck duck go search) shell in python with extended functionality
## About
So you know how you can't exclude words from a search in duckduckgo? That's annoying, right? No longer shall we suffer from this oppression! So anyway that was the point of the entire project.

There are now 2! files. Oh sh!t that's what branches are for. Ah well. One is the original/full/normal/main version and the other is universal/backup/mobile version. The problem was that the original was using some lib that's just not present on android and idk how to fix that if possible. So I changed python libs (this is the third library I've tried and it actually works). The results are limited to ?30? Well it is what it is. Now we have 2 functional versions. Cool.

## Installation
For normal version:

```
pip install -r requirements.txt
``` 
or check your package manager (you should do this on arch)

For mobile version:

```
pip install -r requirements-m.txt
```

For termux additionally run in termux:

```
pkg install termux-api
```

Install Termux:API from fdroid/Google/wherever else kids get apps nowadays

## Tutorial

```
q		quit
t TEXT		text to search for
s		executes search
v		print out the results
vs		print the results one at a time
e TEXT		exclude words, no arguments unsets it
el TEXT		exclude text from urls, no arguments unsets it
ec		set/unset case sensitivity for word exclusion
p		print all variables
m NUM		set max number of search results
d		set/unset debugging info, off by default
o [FILES]	outputs results to file(s)
w WIDTH		to set console to certain width
h		print this message
```

So how do I use this thing? Good question

### q stands for quit

Ok I'm bored let's quit

```
 > q
Exiting
```

### t stands for text

First thing you need is the text to search for. Set it using `t`

```
 > t cats and dogs
Search text: cats and dogs
```

### s stands for search

To execute the search use `s`

```
 > s
Results acquired
 ```

This will pass 'cats and dogs' to DuckDuckGo (equivalent to 'duckduckgo.com/?q=cats+and+dogs') and get results.

### v stand for view

We can view the results using `v`

```
 > v
Cats & Dogs - Wikipedia
https://en.wikipedia.org/wiki/Cats_&_Dogs
blah blah blah long description
-----------
Cats & Dogs (2001) - IMDb
https://www.imdb.com/title/tt0239395/
yet another wall of text
-----------
Urgent Need for Pet Adoption - Find Dogs & Cats & More | Petfinder
https://www.petfinder.com/
qwertyuiop placeholder poiuytrewq
...
```

(body and the rest of results are cut for easier demonstration)

### vs stands for view (stepping)

Wow that sure is a lot of results to view at once. Use `vs` to view results one at a time.

```
 > vs
(q)uit, (c)opy to clipboard
Cats & Dogs - Wikipedia
https://en.wikipedia.org/wiki/Cats_&_Dogs
Sure is a lot of text, too bad I'm not reading it.
-----------
 >> 

```

Wow, only one result! What can we do now?

Well, view the next result. Just press `Enter`.

```
...
-----------
 >> 
Cats & Dogs (2001) - IMDb
https://www.imdb.com/title/tt0239395/
Dooooooon't care
-----------
 >> 
```

We can stop viewing the results using q

```
...
-----------
 >> q
 >
```

We can copy the url of the latest result using c (though it will automatically scroll to the next result. Should fix it)

```
...
Cats & Dogs - Wikipedia
https://en.wikipedia.org/wiki/Cats_&_Dogs
Sure is a lot of text, too bad I'm not reading it.
 >> c
Cats & Dogs (2001) - IMDb
https://www.imdb.com/title/tt0239395/
qwertyuiopasdfghjklzxcvbnm
-----------
 >>
```

Our clipboard will be set to "https://en.wikipedia.org/wiki/Cats_&_Dogs". Unfortunately doesn't work in tty mode. Needs konsole or wtv. Idk about windows.

### e stands for exclude

Ok, fun part. Use `e` to filter out results with the text you don't want to see. (warning: this is only cosmetic and happens only when displaying the results). I don't want to see anything related to the movie.

```
 > e film movie trailer
Excluding from search: ['film', 'movie', 'trailer']
```

Let's see if it works (idk, I made it so maybe it doesn't)

```
 > v
Urgent Need for Pet Adoption - Find Dogs & Cats & More | Petfinder
https://www.petfinder.com/
Petfinder helps you find your new ...
-----------
Pet Adoption | Animal Shelter | Worcester Animal Rescue League
https://worcesterarl.org/
Founded initially by a group of ...
-----------
Watch Cats & Dogs | Prime Video - amazon.com
https://www.amazon.com/Cats-Dogs-Jeff-Goldblum/dp/B000GOV7G6
All my homies hate corporations
...
```

As we can see no mention of the words "movie" and the rest. But we still see the mention of THE movie. Let's filter out the results of "Cats & Dogs" specifically by embedding it in quotes. (For now `e` sets the result each time, not appends it. Might be changed later)

```
 > e "Cats & Dogs"
Excluding from search: ['Cats & Dogs']
```

Btw don't look at the function I use to separate the quotes. That's my Magnus Carlsen or smth. Don't even try to include a double quote inside another double quote. I'll find you.

Let's see if it worked

```
 > v
...
...
-----------
10 Best Dog Breeds That Get Along With Cats - The Spruce Pets
https://www.thesprucepets.com/dog-breeds-that-get-along-with-cats-4688282
Learn which dog breeds are typically friendly and sociable with cats, and why...
```

As we can see, no mentions of "Dogs & Cats".

To reset exclusion just use `e` by itself

```
 > e
Not excluding any words
```

### el stands for exclude links

Excludes text found in links. (Basically the usage is to exclude domains or extensions I guess)

Let's say we don't want to see .com websites

```
 > el .com
Excluding from links: ['.com']
```

Let's see if it works

```
 > v
Cats & Dogs - Wikipedia
https://en.wikipedia.org/wiki/Cats_&_Dogs
Smth smth
-----------
Cats & Dogs (film series) - Wikipedia
https://en.wikipedia.org/wiki/Cats_&_Dogs_(film_series)
That's enough *skull emoji*
-----------
Pet Adoption | Animal Shelter | Worcester Animal Rescue League
https://worcesterarl.org/
Don't buy pets. Adopt them, don't be an asshole
...
```

(before anyone sues me, all of the text in the body has been edited)

No .com websites here. As with e, use `el` by itself to reset it.

```
 > el
Not excluding any words
```

### ec stands for exclude (case)

So as you could've noticed I did not care about case all this time. That's because ec was on. We were ignoring case. If you want your exclusion to be case-ful, use ec

```
Ignoring exclusion case: False
```

If we want to turn it back on:

```
Ignoring exclusion case: True
```

Believe me that it works.

### m stands for max (results)

Works differently for mobile and full versions. 

For the full version determines the maximum amount of results to receive. 

Can't do the same for the mobile version, so it just changes the amount of results that are displayed. It's cosmetic so it can be changed without using `s` again.

The usage is simple `m NUM` where num is the number of results you want to see.

```
 > t foss
Search text: foss
 > m 1
Max results set to 1
 > s
Results acquired
 > v
Free Open Source Software
https://www.freeopensourcesoftware.org/index.php/Main_Page
This follows the same natural way that science has developed over time." - Taoism of Open Source; Chen Nan Yang; September 29, 2007. Free Open Source Software (FOSS), sometimes also called just Open Source or Free Software, is software that is licensed to be free to use, modify, and distribute. Most FOSS licenses also include a kind of legal ...
-----------
 > 
```

As we can see there was only 1 result, as was set.

### d stands for debug

`d` allows us to view error messages when they are handled by try-except. 

Let's see what it would look like without debug:

```
 > m clearlynotanumber
Couldn't set max results to clearlynotanumber
 >
```

Huh, I sure wonder why. Let's see.

```
 > d
Debugging set to: True
 > m clearlynotanumber
Couldn't set max results to clearlynotanumber 
invalid literal for int() with base 10: 'clearlynotanumber'
 > 
```

Ooooh, who could've guessed.

### o stands for output

You ever want to output a result into a file? Say no more.

`o` works like v but with the output to a file.

```
 > t foss
Search text: foss
 > el .com .net
Excluding from links: ['.com', '.net']
 > s
Results acquired
 > o tmp1 tmp2
Wrote output to: tmp1
Wrote output to: tmp2
 > 
```

As we can see it can write to more than one file at a time. Need to add append instead of write.

### w stands for (terminal) width

I guess we need cosmetics or something.

Oh nooooo the text is taking up all of my screen, I need to have it only on the left side of my screen for some reason, however will I do that? No worries, use `w NUM`, where NUM is the number of symbols you want in a line.

```
 > regular output:
 > vs
(q)uit, (c)opy to clipboard
Free Open Source Software
https://www.freeopensourcesoftware.org/index.php/Main_Page
This follows the same natural way that science has developed over time." - Taoism of Open Source; Chen Nan Yang; September 29, 2007. Free Open Source Software (FOSS), sometimes also called just Open Source or Free Software, is software that is licensed to be free to use, modify, and distribute. Most FOSS licenses also include a kind of legal ...
-----------
 >> q
 > w 30
Width set to 30
 > changed output:
 > vs
(q)uit, (c)opy to clipboard
Free Open Source Software
https://www.freeopensourcesoft
ware.org/index.php/Main_Page
This follows the same natural 
way that science has developed
over time." - Taoism of Open 
Source; Chen Nan Yang; 
September 29, 2007. Free Open 
Source Software (FOSS), 
sometimes also called just 
Open Source or Free Software, 
is software that is licensed 
to be free to use, modify, and
distribute. Most FOSS licenses
also include a kind of legal 
...
-----------
 >> q
 >
```

### p stands for print (variables)

So let's see all the variables that we care about.

```
 > p
Search text: abc
Max results: 100
Excluded words: ['tv']
Excluded from links: ['.com', '.net']
Debugging: True
Ignoring case: True
Width: 178
Number of results: 100
```

### h stands for HEEEEELPPPP!!!!

Print the help message that you saw at the start.

## TODO
1. Maybe forced inclusion, though you can use double quotes in the search so why?
2. Merge files (will start today finally)
3. Make everything a function
4. Add append instead of write for output to file
5. Open link in x

That's it.
