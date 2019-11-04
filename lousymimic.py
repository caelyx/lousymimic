#!/usr/bin/env python

import random
import anydbm
import argparse
import cPickle


## Support functions ##

def dict_add(d, index, item):
  """ Cheater function which simplifies adding new content to the hash."""
  if d.has_key(index):
    dlist = cPickle.loads(d[index])
    dlist.append(item)
    d[index] = cPickle.dumps(dlist)
  else:
    d[index] = cPickle.dumps([item])



## Data connections ##

def connectToWrite(fn='lousymimic.db', delimiter="\n"):
  d = anydbm.open(fn, 'c')
  if d.has_key('DELIMITER'):
    delimiter = d['DELIMITER']
  else:
    d['DELIMITER'] = delimiter
  return(d, delimiter)


def connectToRead(fn='lousymimic.db'):
  d = anydbm.open(fn, 'r')
  delimiter = d['DELIMITER']
  return(d, delimiter)



## Main logic ##

def ingest(fp_in, dict_out, delimiter="\n"):
  """Updates a db with new content."""
  content = fp_in.read()
  blocks = content.split(delimiter)
  
  # Dictionary structure is:
  # dict_out = {'word': ['next word', 'next word', ...]}
  # Special condition: delimiter is treated as a word

  for b in blocks:
    ws = b.split()
    if (len(ws) > 1):
      dict_add(dict_out, delimiter, ws[0])
      
      ws.append(delimiter)
      for wi in range(len(ws) - 1):
	dict_add(dict_out, ws[wi], ws[wi + 1])


def express(d, count=5, delimiter="\n"):
  """Generates text from an existing db."""
  for _ in range(count):
    word = random.choice(cPickle.loads(d[delimiter]))
    while (word != delimiter):
      print(word)
      word = random.choice(cPickle.loads(d[word]))
    print(delimiter)



## Main line ##

def main():

  parser = argparse.ArgumentParser(description="World's lamest mimicry machine.")
  parser.add_argument('-i', '--ingest', action='store_true', help='Update an existing db.')
  parser.add_argument('-e', '--express', action='store_true', help='Express some nonsense from the db.')
  parser.add_argument('-d', '--database', action='store', nargs=1, help='Database to use.')
  parser.add_argument('-s', '--source', action='store', nargs=1, help='Source text file to update with.')
  parser.add_argument('-n', '--number', action='store', nargs=1, help='Number of sentences/lines to express.')
  parser.add_argument('--sentences', action='store_true', help='Break content into sentences.')
  parser.add_argument('--lines', action='store_true', help='Break content into lines (default).')
  args = parser.parse_args()

  # Are we updating or creating?

  if (args.ingest):
    delimiter = '\n'
    if (args.sentences):
      delimiter = '.'
    if (args.database):
      (d, delimiter) = connectToWrite(args.database[0], delimiter)
    else:
      (d, delimiter) = connectToWrite('lousymimic.db', delimiter)
    fp = open(args.source[0])
    ingest(fp, d, delimiter)

  elif (args.express):
    if (args.database):
      (d, delimiter) = connectToRead(args.database[0])
    else:
      (d, delimiter) = connectToRead('lousymimic.db')
    n = 5
    if (args.number): n = int(args.number[0])
    express(d, n, delimiter)
  else:
    print("No action requested.")


if __name__ == "__main__":
  main()
