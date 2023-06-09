from html import escape
from datetime import datetime

# To manually change
RECOMMENDED_BLOG_POST_URL = ""

# All our blog posts end like this. The date is the building date
def the_hackerbirds_love_you():
    return "<p><i>the hackerbirds love you - . . - "+datetime.today().strftime('%Y-%m-%d')+"</i></p>"

# We still keep header.html in another file so that our IDE can prettify it
footer_html = """<br><br></main>
<footer>
    """+the_hackerbirds_love_you()+"""
    <a href="#">scroll up</a> &emsp; <a href="../">homepage</a> &emsp; <a href="""+RECOMMENDED_BLOG_POST_URL+""">check out our previous blog post</a>
</footer>
</body>
</html>"""

def write_index_html(post):
    # Erases contents of index.html
    open("index.html", "w").close()
    with open("index.html", "a") as index_html:
        # Write header.html to index.html
        with open("header.html", "r") as header_html:
            index_html.write(header_html.read())

        # Write post contents
        index_html.write(post)

        # Write footer
        index_html.write(footer_html)   

# Parses each line into html.
def parse(line):
    html = ""
    escaped_line = escape(line)
    if escaped_line == "\n":
        return "<br>"
    else:
        # This is for inline code blocks
        if '`' in escaped_line:
            split_code_line = escaped_line.split("`")
            if len(split_code_line) % 2 == 0:
                # Means there's an odd amount of '`` which shouldn't happen
                raise Exception("Code tag weirdly formatted at line \""+line+"\". Are you sure there is the right amount of '`' in your line?")

            open_tag = True
            # For loop for all the `
            for thing in split_code_line:
                # Actually the loop goes one extra round so
                # we need this if condition for when there are no more `
                if '`' not in escaped_line:
                    break
                code_tick_index = escaped_line.index('`')
                if open_tag is True:
                    escaped_line = escaped_line[:code_tick_index] + "<code>" + escaped_line[code_tick_index+1:]
                    open_tag = False
                else: 
                    escaped_line = escaped_line[:code_tick_index] + "</code>" + escaped_line[code_tick_index+1:]
                    open_tag = True

        # Inline italic text
        if '__' in escaped_line:
            split_code_line = escaped_line.split("__")
            if len(split_code_line) % 2 == 0:
                raise Exception("Italics formatted at line \""+line+"\". Are you sure there is the right amount of '__' in your line?")

            open_tag = True
            # For loop for all the `
            for thing in split_code_line:
                # Actually the loop goes one extra round so
                # we need this if condition for when there are no more `
                if '__' not in escaped_line:
                    break
                code_tick_index = escaped_line.index('__')
                if open_tag is True:
                    escaped_line = escaped_line[:code_tick_index] + "<i>" + escaped_line[code_tick_index+2:]
                    open_tag = False
                else: 
                    escaped_line = escaped_line[:code_tick_index] + "</i>" + escaped_line[code_tick_index+2:]
                    open_tag = True
        # Inline bold text
        if ('*' in escaped_line and escaped_line[0] != '*'):
            split_code_line = escaped_line.split("*")
            if len(split_code_line) % 2 == 0:
                raise Exception("Bold formatted at line \""+line+"\". Are you sure there is the right amount of '*' in your line?")

            open_tag = True
            # For loop for all the `
            for thing in split_code_line:
                # Actually the loop goes one extra round so
                # we need this if condition for when there are no more `
                if '*' not in escaped_line:
                    break
                code_tick_index = escaped_line.index('*')
                if open_tag is True:
                    escaped_line = escaped_line[:code_tick_index] + "<b>" + escaped_line[code_tick_index+1:]
                    open_tag = False
                else: 
                    escaped_line = escaped_line[:code_tick_index] + "</b>" + escaped_line[code_tick_index+1:]
                    open_tag = True
                    
        # Headers: id is used to scroll
        if escaped_line.startswith("# "):
            text = escaped_line.rstrip()[2:]
            html = "<h1 id=\""+text.replace(" ", "-")+"\">"+text+"</h1>"
        elif escaped_line.startswith("## "):
            text = escaped_line.rstrip()[3:]
            html = "<h2 id=\""+text.replace(" ", "-")+"\">"+text+"</h2>"
        elif escaped_line.startswith("### "):
            text = escaped_line.rstrip()[4:]
            html = "<h3 id=\""+text.replace(" ", "-")+"\">"+text+"</h3>"
        elif escaped_line.startswith("% "):
            text = escaped_line.rstrip()[2:]
            html = "<div class=\"fronter\">"+text+"</div>"
        # Link/URL (" => ")
        elif escaped_line.startswith("=&gt; "):
            split_line = escaped_line.rstrip().split(" ")
            url = split_line[1]
            text = url
            if len(split_line) > 2: # There is text after the URL
                text = ' '.join(split_line[2:])

            html = "<a href=\""+url+"\">"+text+"</a>"
        # List element
        elif escaped_line.startswith("* "):
            html = "<li>"+parse(line.rstrip()[2:])+"</li>"
        # Blockquote (" > ")
        elif escaped_line.startswith("&gt; ") and not escaped_line.startswith("=&gt; "):
            html = "<blockquote><p>"+escaped_line.rstrip()[4:]+"</p></blockquote>"
        # Bar line
        elif escaped_line == "---\n":
            html = "<hr>"
        else:
            html = "<p>"+escaped_line.rstrip()+"</p>"
    return html

with open("post.txt", "r") as f:
    html = ""
    is_in_code_block = False
    is_in_list = False
    for line in f:
        # Beginning OR end of a code block
        if line.startswith("```"):
            if is_in_code_block is True:
                is_in_code_block = False
                # Close code bock
                html += "</pre>"
            else:
                is_in_code_block = True
                # Open code block
                html += "<pre aria-label=\"\">"
        # List element
        elif line.startswith("* "):
            # If not in a list already, put us in list mode
            if is_in_list is False:
                html += "<ul>"
                is_in_list = True
            html += parse(line)
        else:
            # Line isn't ``` (code block) or starts with "*" (list)
            if is_in_code_block is True:
                html += escape(line)
            elif is_in_list is True:
                html += "</ul>"
                html += parse(line)
                # We exit list mode
                is_in_list = False
            else:
                html += parse(line)

    write_index_html(html)
