
class Text(object):
  def __init__(self, filename):

    with open(filename, "r") as f:
      self.original = f.read()

    self.filename = filename
    self.cleaned = False

    self.title = ""
    self.author = ""
    self.clean_text = ""

    self._clean()


  def _clean(self):
    import re
    start_tag = re.compile("(\*\*\*)?start of (this |the )?project gutenberg", re.I)
    end_tag = re.compile("(\*\*\*)?end of (this |the )?project gutenberg", re.I)

    # Remove any pre-/post- text from the work.
    lines = self.original.split("\n")
    start, end = 0, len(lines)
    for i, line in enumerate(lines):
      if start_tag.match(line) and i>start: start = i
      elif end_tag.match(line) and i<end: end = i
    lines = lines[start+1:end]

    # Remove any line that has no content and remove any buffering whitespace.
    any_letter = "[a-zA-Z]"
    lines = [line.strip() for line in lines if re.search(any_letter, line)]

    # Removing any illustration demarkations.
    illustration = "\[Illustration"
    lines = [line for line in lines if not re.search(illustration, line, re.I)]

    text = "\n".join(lines)

    # Remove any superfluous spacing.
    text = re.sub(" +", " ", text)


    self.clean_text = text.strip()
    self.cleaned = True

  def get_words(self, original=False):
    if original or not self.clean_text:
      words = self.original.split(" ")

    else:
      words = self.clean_text.split(" ")

    return words


  def read(self):
    return self.clean_text


  def __str__(self):
    if self.cleaned:
      return "Text({}: {} Words)".format(self.title, len(self.get_words()))
    else:
      return "Text({} Words)[Dirty]".format(len(self.get_words(original=True)))


  def __repr__(self):
    return str(self)




def text_generator(path):
  """
  Given a `path` to a directory, iteratively generate the content of
  all *.txt files that reside in that directory.
  """

  from os import listdir
  from os.path import isfile, join

  text_files = [join(path,f) for f in listdir(path)
                  if isfile(join(path,f)) and ".txt" in f]

  for filename in text_files:
    yield Text(filename)



# Debugging Sandbox
texts = text_generator("data/raw")

for text in texts:
  print text
  print text.read()
  raw_input("Continue?")

