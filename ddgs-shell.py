#!/usr/bin/python3

from duckduckgo_search import DDGS
# from argparse import ArgumentParser as argparser
from rich.console import Console
from rich.markup import escape
from pyperclip import copy as to_clipboard


width = None
console = Console(width=width)
regprint = print
print = console.print

shell_message = """
q\t\tquit
v\t\tprint out the results
t TEXT\t\ttext to search for
e TEXT\t\texclude words, no arguments unsets it
el TEXT\t\texclude text from urls, no arguments unsets it
ec\t\tset/unset case sensitivity for word exclusion
m [NUM]\t\tset max number of results
p\t\tprint all variables
s\t\texecutes search
d\t\tset/unset debugging info, off by default
vs\t\tset/unset stepping for printing results, off by default
o [FILES]\toutputs results to file(s)
w WIDTH\t\tto set console to certain width
h\t\tprint this message
"""


def SepStr(string: str):
    q_index = []
    out = []
    for i, char in enumerate(string):
        if char == '"':
            q_index.append(i)
    if len(q_index) < 2:
        return string.split()
    q_index = q_index[:len(q_index)//2*2]
    for word in string[:q_index[0]].split():
        word = word.strip()
        if len(word) != 0:
            out.append(word)
    for i in range(0, len(q_index), 2):
        out.append(string[q_index[i]+1:q_index[i+1]])
        if i < len(q_index)-2:
            for word in string[q_index[i+1]+1:q_index[i+2]].split():
                word = word.strip()
                if len(word) != 0:
                    out.append(word)
        else:
            for word in string[q_index[i+1]+1:].split():
                word = word.strip()
                if len(word) != 0:
                    out.append(word)
    return out


def Exclude(results: list,
            exwords: list,
            fex_links: bool = False,
            exlinks: list = list(),
            ignore_case: bool = True
            ) -> list:
    if len(exwords) + len(exlinks) == 0:
        return results
    out = []
    for res in results:
        include = True
        # just check the link first amiright
        if fex_links or len(exlinks) > 0:
            link = res["href"].lower()
            if fex_links and len(exlinks) == 0:
                exlinks = exwords
            for exlink in exlinks:
                if exlink.lower() in link:
                    include = False
                    break
        if not include:
            continue
        if len(exwords) == 0:
            if include:
                out.append(res)
            continue
        # and if needed check the body
        title = res["title"].lower() if ignore_case else res["title"]
        body = res["body"].lower() if ignore_case else res["body"]
        for word in exwords:
            if ignore_case:
                word = word.lower()
            if word in title or word in body:
                include = False
                break
        if include:
            out.append(res)
    return out


def PrintSearch(results: list, step: bool = False):
    if step:
        print("[yellow](q)uit, (c)opy to clipboard[/yellow]")
    for res in results:
        print("[b]"+escape(res["title"])+"[/b]")
        print(escape(res["href"]))
        print(escape(res["body"]))
        print("-----------")
        if step:
            tmp = input(" >> ")
            if tmp in ["!q", 'q']:
                break
            elif tmp in ['!c', 'c']:
                to_clipboard(res["href"])
    return 0


def OutputSearch(results):
    out = []
    for res in results:
        out.append("\n".join((res["title"], res["href"], res["body"])))
    return "\n".join(out)


def Shell(*args):
    global console
    print("Welcome to DDGS expanded search")
    print(shell_message)
    text = ""
    max_res = 100
    ex_words = list()
    results = list()
    debug = False
    ex_links = False
    ex_linkwords = list()
    ignore_case = True
    step = False
    backend = "lite"
    while True:
        inp = input(" > ")
        if inp == 'q':
            print("Exiting")
            break
        else:
            inp = inp.split()
        if len(inp) == 0:
            continue
        match inp[0]:
            case "t":
                text = " ".join(inp[1:])
                print(f"[green]Search text: {text}[green]")
            case "e":
                if len(inp) == 1:
                    ex_words = list()
                    print("[green]Not excluding any words[/green]")
                    continue
                ex_words = SepStr(" ".join(inp[1:]))
                print(f"[green]Excluding from search: {ex_words}[/green]")
            case "el":
                if len(inp) == 1:
                    ex_linkwords = list()
                    print("[green]Not excluding any words[/green]")
                    continue
                ex_linkwords = SepStr(" ".join(inp[1:]))
                print(f"[green]Excluding from links: {ex_linkwords}[/green]")
            case "ec":
                ignore_case = not ignore_case
                print(f"[green]Ignoring exclusion case: {ignore_case}[/green]")
            case "m":
                if len(inp) > 2:
                    print("[red]max requires 1 or 0 arguments[/red]")
                    continue
                if len(inp) == 1:
                    max_res = 100
                    print("[green]max set to 100[/green]")
                    continue
                try:
                    max_res = int(inp[1])
                    print(f"[green]Max results set to {max_res}[/green]")
                except Exception as e:
                    print(f"[red]Couldn't set max results to {' '.join(inp[1:])} [red]")
                    if debug:
                        regprint(e)
                    continue
            case "p":
                print(f"Search text: {text}",
                      f"Max results: {max_res}",
                      f"Excluded words: {ex_words}",
                      f"Stepping: {step}",
                      f"Debugging: {debug}",
                      f"Excluding links: {ex_links}",
                      f"Ignoring case: {ignore_case}",
                      f"Width: {console.width}",
                      f"Number of results: {len(results)}",
                      sep="\n")
            case "s":
                if text == "":
                    print("[red]No search text![/red]")
                    continue
                try:
                    results = DDGS().text(keywords=text,
                                          max_results=max_res,
                                          safesearch="Off",
                                          backend=backend)
                    print("[green]Results acquired[/green]")
                except Exception as e:
                    if "ratelimit" in str(e).lower():
                        print("[red]It appears we've been ratelimited[/red]")
                    else:
                        print("[red]Something went wrong[/red]")
                    print("Try using \"> backend\"")
                    if debug:
                        regprint(e)
            case "v":
                if len(results) == 0:
                    print("[red]No results to display[red]")
                    continue
                PrintSearch(Exclude(results=results,
                                    exwords=ex_words,
                                    fex_links=ex_links,
                                    exlinks=ex_linkwords,
                                    ignore_case=ignore_case),
                            step=step)
                continue
            case "vs":
                step = not step
                print(f"[green]Stepping set to: {step}[/green]")
            case "d":
                debug = not debug
                print(f"[green]Debugging set to: {debug}[/green]")
            case "h":
                print(shell_message)
            case "w":
                if len(inp) > 2:
                    print("[red]w takes 0 or 1 arguments[/red]")
                    continue
                elif len(inp) == 1:
                    console.width = None
                    print("[green]Width set to None[/green]")
                    continue
                try:
                    console.width = int(inp[1])
                    print(f"[green]Width set to {console.width}[/green]")
                except Exception as e:
                    print(f"[red]Couldn't set width to {inp[1]}[/red]")
                    if debug:
                        regprint(e)
            case "o":
                if len(results) == 0:
                    print("[red]No results to write[/red]")
                if len(inp) < 2:
                    print("[red]No file specified[/red]")
                    continue
                for dest in inp[1:]:
                    try:
                        with open(dest, 'w') as f:
                            f.write(OutputSearch(Exclude(results,
                                                         ex_words,
                                                         ex_links,
                                                         ignore_case)))
                            print(f"[green]Wrote output to: {dest}[/green]")
                            continue
                    except Exception as e:
                        print(f"[red]Couldn't write to: {dest}[/red]")
                        if debug:
                            regprint(e)
            case "backend":
                if len(inp) != 2:
                    print("[red]Takes exactly one argument: html/api/lite")
                    continue
                if inp[1] in ["lite", "html", "api"]:
                    backend = inp[1]
                    print(f"[green]Set backend to {inp[1]}[/green]")
                else:
                    print("[red]Must be one of html/api/lite[/red]")
            case _:
                continue
    return 0


def main() -> int:
    Shell()


if __name__ == "__main__":
    main()
