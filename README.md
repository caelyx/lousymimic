**lousymimic -- World's lamest mimicry machine**

Create a databse:
`lousymimic --ingest -d database.db -s textfile.db [--sentences || --lines]`

Use a database to generate content:
`lousymimic [-d lousymimic.db] [-n sentences/lines] [-w words]`


Sample textfiles are in `text/`:

*  `text/2born2.txt` == Hamlet's soliloquy, from [Wikipedia](http://en.wikipedia.org/wiki/To_be,_or_not_to_be)

*  `text/hamlet.txt` == Full-text of Hamlet, with some edits for purpose, from [MIT](http://shakespeare.mit.edu/hamlet/full.html)
