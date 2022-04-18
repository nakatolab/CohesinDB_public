import urllib
with urllib.request.urlopen('http://togows.org/api/ucsc/hg38/chr1:12345-12500.fasta') as response:
   html = response.read()
html
" ".join(html.decode("utf-8").split("\n")[1:-1])


with urllib.request.urlopen('http://genome.ucsc.edu/cgi-bin/das/hg19/dna?segment=chr1:12345,12500') as response:
   html = response.read()
html.decode("utf-8").split("\n")
