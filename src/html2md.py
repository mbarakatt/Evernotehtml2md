import sys
import bs4
from bs4 import BeautifulSoup

markdown = ['']

# input_text = sys.stdin.read()
input_text = open('../data/2017/2017.html', 'r').read()
# input_text = open('easy.html', 'r').read()


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
                markdown.append('\n')
    elif type(bs_tag) == bs4.element.NavigableString:
        print("STRING", len(str(bs_tag.string)), bs_tag.parent.name, ":", bs_tag)
        # if  and bs_tag.parent.tag
        # if str(bs_tag.string) != '\n' or (str(bs_tag.string) == '\n' and markdown[-1] != '\n'):

        # To force new line add two spaces at the end of a line
        if bs_tag.parent.name in ['div', 'ul'] and  str(bs_tag.string) == '\n' and bs_tag.previous_sibling is not None:
            if markdown[find_last_non_empty_line()] != '\n':
                if markdown[find_last_non_empty_line()][-2:] != "  ":
                    markdown[find_last_non_empty_line()] += "  "
                else:
                    markdown.append(bs_tag.string)

        elif bs_tag.parent.name == "li":
            markdown.append("* " + bs_tag.string)
        else:
            markdown.append(bs_tag.string)
        return

    for item in bs_tag.contents:
        recursive_print(item, level)


output_text = BeautifulSoup(input_text, 'html.parser')

recursive_print(output_text.body, 0)

fout = open('out.md', 'w')
for l in markdown:
    fout.write(l + '\n')

fout.close()
# sys.stdout.write(input_text)
sys.stdout.write(BeautifulSoup(input_text, 'html.parser').prettify())

# maybe the way to handle this is via a recursive function?
