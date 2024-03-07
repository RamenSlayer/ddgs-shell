#!/usr/bin/python3

from duckduckgo_search import DDGS
# from argparse import ArgumentParser as argparser
from rich import print

shell_message = """
!q\t\tquit
!v\t\tprint out the results
!t TEXT\t\ttext to search for
!e TEXT\t\texclude words, no text unsets it
!el\t\tset/unset excluding words from links, off by default
!ec\t\tset/unset case sensitivity for word exclusion
!m NUM\t\tset max number of results
!p\t\tprint all variables
!s\t\texecutes search
!d\t\tset/unset debugging info, off by default
!vs\t\tset/unset stepping for printing results, off by default
!o [FILES]\t\toutputs results to file(s)
!h\t\tprint this message
"""


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
        body = results[i]["body"]
        link = results[i]["href"]
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
        print("[yellow]!q to stop scrolling if needed[/yellow]")
    for res in results:
        print("[b]"+res["title"]+"[/b]")
        print(res["href"])
        print(res["body"])
        print("-----------")
        if step:
            tmp = input("Next")
            if tmp in ["!q", 'q']:
                break
    return 0


def Output_Search(results):
    out = []
    for res in results:
        out.append("\n".join((res["title"], res["href"], res["body"])))
    return "\n".join(out)


def Shell(*args):
    print("Welcome to DDGS expanded search")
    print(shell_message)
    text = ""
    max_res = 100
    ex_words = None
    results = None
    debug = False
    ex_links = False
    ignore_case = True
    step = False
    while True:
        inp = input(" > ")
        if inp == '!q':
            print("Exiting")
            break
        else:
            inp = inp.split()
        match inp[0]:
            case "!t":
                text = " ".join(inp[1:])
                print(f"[green]Search text: {text}[green]")
            case "!e":
                if len(inp) == 1:
                    ex_words = None
                    print("[green]Not excluding any words[/green]")
                    continue
                ex_words = inp[1:]
                print(f"[green]Excluding selected words: {ex_words}[/green]")
            case "!el":
                ex_links = not ex_links
                print(f"[green]Exluding text in links: {ex_links}[/green]")
            case "!ec":
                ignore_case = not ignore_case
                print(f"[green]Ignoring exclusion case: {ignore_case}[/green]")
            case "!m":
                if len(inp) != 2:
                    print("[red]max requires exactly one argument[/red]")
                    continue
                try:
                    max_res = int(inp[1])
                    print(f"[green]Max results set to {max_res}[/green]")
                except Exception as e:
                    print(f"[red]Couldn't set max results to {inp[1]}[red]")
                    if debug:
                        print(f"[red]{e}[/red]")
                    continue
            case "!p":
                print(f"Search text: {text}",
                      f"Max results: {max_res}",
                      f"Excluded words: {ex_words}",
                      f"Stepping: {step}",
                      f"Debugging: {debug}",
                      f"Excluding links: {ex_links}",
                      f"Ignoring case: {ignore_case}",
                      sep="\n")
            case "!s":
                if text == "":
                    print("[red]No search text![/red]")
                    continue
                results = DDGS().text(keywords=text,
                                      max_results=max_res,
                                      safesearch="Off")
                print("[green]Results acquired[/green]")
            case "!v":
                if results is None:
                    print("[red]No results yet![red]")
                    continue
                if ex_words is not None:
                    Print_Search(Exclude(results,
                                         ex_words,
                                         ex_links,
                                         ignore_case),
                                 step=step)
                    continue
                Print_Search(results, step=step)
                continue
            case "!vs":
                step = not step
                print(f"[green]Stepping set to: {step}[/green]")
            case "!d":
                debug = not debug
                print(f"[green]Debugging set to: {debug}[/green]")
            case "!h":
                print(shell_message)
            case "!o":
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
    return 0


def main() -> int:
    Shell()


if __name__ == "__main__":
    main()
