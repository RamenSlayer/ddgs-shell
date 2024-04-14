#!/usr/bin/python3

from ddg import Duckduckgo
# from argparse import ArgumentParser as argparser
from rich.console import Console
from rich.markup import escape
from os import environ
from shlex import quote


termux = False

if "termux" in environ["PATH"]:
    termux = True
    from os import system as execute

    def to_clipboard(text):
        cmd = "termux-clipboard-set '" + text + "'"
        status = execute(cmd)
        return status
else:
    from pyperclip import copy as to_clipboard

width = 100
console = Console(width=width)
regprint = print
print = console.print

api = Duckduckgo()

shell_message = """
q\t\tquit
v\t\tprint out the results
t TEXT\t\ttext to search for
e TEXT\t\texclude words, no arguments unsets it
el TEXT\t\texclude text from urls, no arguments unsets it
ec\t\tset/unset case sensitivity for word exclusion
p\t\tprint all variables
s\t\texecutes search
m NUM\t\tset max number of search results
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
            link = res["url"].lower()
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
        body = res["description"].lower() if ignore_case else res["description"]
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
    global termux
    if step:
        print("[yellow](q)uit, (c)opy link[/yellow]")
    for res in results:
        print("[b]"+escape(res["title"])+"[/b]")
        print(escape(res["url"]))
        print(escape(res["description"]))
        print("-----------")
        if step:
            tmp = input(" >> ")
            if tmp == 'q':
                break
            elif tmp == 'c':
                if termux:
                    status = to_clipboard(quote(res["url"]))
                    print(f"Copy status: {status}")
                else:
                    to_clipboard(res["url"])
    return 0


def OutputSearch(results):
    out = []
    for res in results:
        out.append("\n".join((res["title"], res["url"], res["description"])))
    return "\n".join(out)


def Shell(*args):
    global console
    print("Welcome to DDGS expanded search")
    print(shell_message)
    text = ""
    ex_words = list()
    results = list()
    debug = False
    ex_links = False
    ex_linkwords = list()
    ignore_case = True
    step = False
    max_res = 0
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
                print(f"[green]Excluding selected words: {ex_words}[/green]")
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
                    max_res = 0
                    print("[green]Results won't be capped[/green]")
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
                results = api.search(text)
                if not results['success']:
                    print("[red]Couldn't get results[/red]")
                    if debug:
                        print("[red]" + escape(str(results)) + "[/red]")
                    results = list()
                    continue
                results = results["data"]
                print("[green]Results acquired[/green]")
            case "v":
                if len(results) == 0:
                    print("[red]No results to display[red]")
                    continue
                tmp_results = results
                if max_res == 0:
                    pass
                else:
                    tmp_results = results[:max_res]
                PrintSearch(Exclude(results=tmp_results,
                                    exwords=ex_words,
                                    fex_links=ex_links,
                                    exlinks=ex_linkwords,
                                    ignore_case=ignore_case),
                            step=step)
                del tmp_results
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
                        print("[red]" + escape(e) + "[/red]")
            case "o":
                if len(results) == 0:
                    print("[red]No results to write[/red]")
                if len(inp) < 2:
                    print("[red]No file specified[/red]")
                    continue
                for dest in inp[1:]:
                    try:
                        with open(dest, 'w') as f:
                            f.write(OutputSearch(Exclude(results=results,
                                                 exwords=ex_words,
                                                 fex_links=ex_links,
                                                 exlinks=ex_linkwords,
                                                 ignore_case=ignore_case)))
                            print(f"[green]Wrote output to: {dest}[/green]")
                    except Exception as e:
                        print(f"[red]Couldn't write to: {dest}[/red]")
                        if debug:
                            print(f"[red]{e}[/red]")
            case _:
                continue
    return 0


def main() -> int:
    Shell()


if __name__ == "__main__":
    main()
