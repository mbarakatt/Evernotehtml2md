import sys
import bs4
from bs4 import BeautifulSoup

markdown = ['\n']

# input_text = sys.stdin.read()
input_text = open('2017/2017.html', 'r').read()
# input_text = open('easy.html', 'r').read()


def recursive_print(bs_tag, level):
    # print(level)
    level += 1
    if type(bs_tag) == bs4.element.ProcessingInstruction:
        print("PROCIN", bs_tag)
        return
    if type(bs_tag) == bs4.element.Doctype:
        print("DOCTYP", bs_tag)
        return
    if type(bs_tag) == bs4.element.NavigableString:
        print("STRING", bs_tag)
        if str(bs_tag.string) != '\n' or (str(bs_tag.string) == '\n' and
                markdown[-1] != '\n'):  # has to be one for some reason
            print(len(str(bs_tag.string)))
            # print('TT', str(bs_tag.string)[0], 'TT')
            markdown.append(bs_tag)
        return

    if bs_tag.name == 'hr':
        markdown[-1] = "# " + markdown[-1]
    # if bs_tag.name == 'div':  # if the div only contains a cr
    #     if bs_tag.div.s
    print("TAGTAG", bs_tag.name)

    for item in bs_tag.contents:
        recursive_print(item, level)


output_text = BeautifulSoup(input_text, 'html.parser')

recursive_print(output_text.body, 0)

fout = open('out.md', 'w')
for l in markdown:
    fout.write(l + '\n')

fout.close()
# sys.stdout.write(BeautifulSoup(input_text, 'html.parser').prettify())

# maybe the way to handle this is via a recursive function?
