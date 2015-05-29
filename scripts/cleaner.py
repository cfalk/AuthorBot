

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
    with open(filename, "r") as f:
      yield f.read()


texts = text_generator("data/raw")

for text in texts:
  print text

