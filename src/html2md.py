#!/usr/bin/env python3
import sys
import os
import bs4
from bs4 import BeautifulSoup
from distutils.dir_util import copy_tree
import subprocess


def find_last_non_empty_line():
    for i, l in list(enumerate(markdown))[::-1]:
        if l != '\n':
            return i
    return 0


def recursive_print(bs_tag, level):
    # print(level)
    level += 1
    print("LEVEL", level)
    if type(bs_tag) == bs4.element.ProcessingInstruction:
        print("PROCIN", bs_tag)
        return
    elif type(bs_tag) == bs4.element.Doctype:
        print("DOCTYP", bs_tag)
        return
    elif type(bs_tag) == bs4.element.Tag:
        print("TAGTAG", bs_tag.name)
        if bs_tag.name == 'hr':
            markdown[find_last_non_empty_line()] = "## " + markdown[find_last_non_empty_line()]
        elif bs_tag.name == 'br':
            if len(markdown) < 2 or (markdown[-1] != '\n' and markdown[-2] != '\n'):
                print("NEWLINE_A")
                markdown.append('\n')
        elif bs_tag.name == "img":
            markdown.append("![ " + "] (" + os.path.join('r', bs_tag["src"].split('/')[-1]) + ")" + ")")
    elif type(bs_tag) == bs4.element.NavigableString:
        print("STRING", len(str(bs_tag.string)), bs_tag.parent.name, ":", bs_tag)
        # if  and bs_tag.parent.tag
        # if str(bs_tag.string) != '\n' or (str(bs_tag.string) == '\n' and markdown[-1] != '\n'):

        # To force new line add two spaces at the end of a line
        if bs_tag.parent.name in ['div', 'ul'] and str(bs_tag.string) == '\n' and bs_tag.previous_sibling is not None:
            if markdown[find_last_non_empty_line()][-2:] != "  ":
                markdown[find_last_non_empty_line()] += "  "
            else:
                if len(markdown) < 2 or (markdown[-1] != '\n' and markdown[-2] != '\n'):
                    markdown.append(bs_tag.string)

        elif bs_tag.parent.name == "li":  # enumration
            markdown.append("* " + bs_tag.string)
        elif bs_tag.parent.name == "a":  # link, local or on the web
            if "href" in bs_tag.parent.attrs.keys():
                if "http" == bs_tag.string[0:4] or "www" == bs_tag.string[0:3]:
                    markdown.append("[" + bs_tag.string + "] (" + bs_tag.parent["href"] + ")")
                else:
                    markdown.append("[" + bs_tag.string.split('/')[-1] + "] (" + os.path.join('r', bs_tag.parent["href"].split('/')[-1]) + ")")
            else:
                markdown.append('WTF')
        else:
            if bs_tag.string == "\n":
                if len(markdown) < 2 or (markdown[-1] != '\n' and markdown[-2] != '\n'):
                    print("NEWLINE_B")
                    markdown.append('\n')
            else:
                markdown.append(bs_tag.string)
        return

    for item in bs_tag.contents:
        recursive_print(item, level)


def write_markdown(markdown, path):
    fout = open(path, 'w')
    for l in markdown:
        fout.write(l + '\n')
    fout.close()


if __name__ == "__main__":
    markdown = ['']
    file_path = '/Users/mbarakatt/Documents/2016/2016.html'
    file_name = file_path.split('/')[-1][:-len(".html")]
    output_folder = file_name
    containing_folder = file_path[:-len(file_path.split('/')[-1])]
    path = os.path.join(output_folder, file_name + ".md")
    if os.path.isdir(os.path.join(containing_folder, file_name + '.resources')):
        if not os.path.isdir(path[:-len(path.split('/')[-1])]):
            os.makedirs(path[:-len(path.split('/')[-1])])
        bash_command = "cp -r " + os.path.join(containing_folder, file_name + '.resources') + " " + os.path.join(output_folder, "r")
        subprocess.Popen(bash_command.split()).communicate()  # this way preserves accents in file name
    input_text = open(file_path, 'r').read()
    output_text = BeautifulSoup(input_text, 'html.parser')
    recursive_print(output_text.body, 0)
    write_markdown(markdown, path)
