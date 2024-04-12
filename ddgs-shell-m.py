#!/usr/bin/python3

from ddg import Duckduckgo
# from argparse import ArgumentParser as argparser
from rich.console import Console
from rich.markup import escape
from os import environ


termux = False

if "termux" in environ["PATH"]:
    termux = True
    from os import system as execute

    def to_clipboard(text):
        cmd = "termux-clipboard-set \"" + text.raw() + "\""
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
e TEXT\t\texclude words, no text unsets it
el\t\tset/unset excluding words from links, off by default
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


def CleanStupidUrls(url: str):
    """A stupid url is one that uses double quotes."""
    url = url.replace('"', '\\"')
    return url


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
            words: list,
            ex_links: bool = False,
            ignore_case: bool = True,
            preserve_initial: bool = True):
    if preserve_initial:
        results = results.copy()
    end = len(results)
    i = 0
    while i < end:
        title = results[i]["title"]
        body = results[i]["description"]
        link = results[i]["url"]
        if ignore_case:
            body = body.lower()
            title = title.lower()
            link = link.lower()
        for word in words:
            if ignore_case:
                word = word.lower()
            if word in title:
                results.__delitem__(i)
                end -= 1
                i -= 1
                break
            elif word in body:
                results.__delitem__(i)
                end -= 1
                i -= 1
                break
            elif ex_links and word in link:
                results.__delitem__(i)
                end -= 1
                i -= 1
                break
        i += 1
    return results


def Print_Search(results: list, step: bool = False):
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
                    status = to_clipboard(CleanStupidUrls(["url"]))
                    print(f"Copy status: {status}")
                to_clipboard(res["url"])
    return 0


def Output_Search(results):
    out = []
    for res in results:
        out.append("\n".join((res["title"], res["url"], res["description"])))
    return "\n".join(out)


def Shell(*args):
    global console
    print("Welcome to DDGS expanded search")
    print(shell_message)
    text = ""
    ex_words = None
    results = None
    debug = False
    ex_links = False
    ignore_case = True
    step = False
    max_res = None
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
                    ex_words = None
                    print("[green]Not excluding any words[/green]")
                    continue
                ex_words = SepStr(" ".join(inp[1:]))
                print(f"[green]Excluding selected words: {ex_words}[/green]")
            case "el":
                ex_links = not ex_links
                print(f"[green]Exluding text in links: {ex_links}[/green]")
            case "ec":
                ignore_case = not ignore_case
                print(f"[green]Ignoring exclusion case: {ignore_case}[/green]")
            case "m":
                if len(inp) > 2:
                    print("[red]max requires 1 or 0 arguments[/red]")
                    continue
                if len(inp) == 1:
                    max_res = None
                    print("[green]max set to None[/green]")
                    continue
                try:
                    max_res = int(inp[1])
                    print(f"[green]Max results set to {max_res}[/green]")
                except Exception as e:
                    print(f"[red]Couldn't set max results to {' '.join(inp[1:])} [red]")
                    if debug:
                        print(f"[red]{e}[/red]")
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
                      sep="\n")
                if results is None:
                    print(f"Number of results: {results}")
                else:
                    print(f"Number of results: {len(results)}")
            case "s":
                if text == "":
                    print("[red]No search text![/red]")
                    continue
                results = api.search(text)
                if not results['success']:
                    print("[red]Couldn't get results[/red]")
                    if debug:
                        print("[red]" + escape(str(results)) + "[/red]")
                    results = None
                    continue
                results = results["data"]
                print("[green]Results acquired[/green]")
            case "v":
                if results is None:
                    print("[red]No results![red]")
                    continue
                tmp_results = results
                if max_res is None:
                    pass
                else:
                    tmp_results = results[:max_res]
                if ex_words is not None:
                    Print_Search(Exclude(tmp_results,
                                         ex_words,
                                         ex_links,
                                         ignore_case),
                                 step=step)
                    del tmp_results
                    continue
                Print_Search(tmp_results, step=step)
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
                if results is None:
                    print("[red]No results to write[/red]")
                if len(inp) < 2:
                    print("[red]No file specified[/red]")
                    continue
                for dest in inp[1:]:
                    try:
                        with open(dest, 'w') as f:
                            if ex_words is not None:
                                f.write(Output_Search(Exclude(results,
                                                              ex_words,
                                                              ex_links,
                                                              ignore_case)))
                                print(f"[green]Wrote output to: {dest}[/green]")
                                continue
                            f.write(Output_Search(results))
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
