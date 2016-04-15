import urllib, os

def download(urlbase, filename):
    if not os.path.isfile(filename):
        url = urlbase + filename
        try:
            urllib.urlretrieve(url, filename=filename)
        except IOError as e:
            raise IOError('No Internet connection')
        # Check if downloaded file is an HTML file, which
        # is what github.com returns if the URL is not existing
        f = open(filename, 'r')
        if 'DOCTYPE html' in f.readline():
            raise IOError('URL %s does not exist' % url)

def read_genetic_code_v1(filename):
    infile = open(filename, 'r')
    genetic_code = {}
    for line in infile:
        columns = line.split()
        genetic_code[columns[0]] = columns[1]
    return genetic_code

urlbase = 'http://hplgit.github.com/bioinf-py/data/'
genetic_code_file = 'genetic_code.tsv'
download(urlbase, genetic_code_file)
code = read_genetic_code_v1(genetic_code_file)

def read_genetic_code_v2(filename):
    return dict([line.split()[0:2]
                 for line in open(filename, 'r')])

code2 = read_genetic_code_v2('genetic_code.tsv')
assert code == code2

def read_genetic_code_v3(filename):
    genetic_code = {}
    for line in open(filename, 'r'):
        columns = line.split()
        genetic_code[columns[0]] = {}
        genetic_code[columns[0]]['1-letter']   = columns[1]
        genetic_code[columns[0]]['3-letter']   = columns[2]
        genetic_code[columns[0]]['amino acid'] = columns[3]
    return genetic_code

def read_genetic_code_v4(filename):
    genetic_code = {}
    for line in open(filename, 'r'):
        c = line.split()
        genetic_code[c[0]] = {
        '1-letter': c[1], '3-letter': c[2], 'amino acid': c[3]}
    return genetic_code

code = read_genetic_code_v3('genetic_code.tsv')
print code['UUC']
print code['UUG']

code2 = read_genetic_code_v4('genetic_code.tsv')
assert code == code2

name = 'UUC'
print '%s translates into the amino acid "%s" with "%s" '\
      'as 3-letter code.' % \
      (name, code[name]['amino acid'], code[name]['3-letter'])

def read_dnafile_v1(filename):
    lines = open(filename, 'r').readlines()
    # Remove newlines in each line and join
    dna = ''.join([line.strip() for line in lines])
    return dna

lactase_gene_file = 'lactase_gene.txt'
download(urlbase, lactase_gene_file)
lactase_gene = read_dnafile_v1(lactase_gene_file)
print '10 first bases of the lactase gene: ', lactase_gene[:10]

lactase_exon_file = 'lactase_exon.tsv'
download(urlbase, lactase_exon_file)

def read_exon_regions_v1(filename):
    positions = []
    infile = open(filename, 'r')
    for line in infile:
        start, end = line.split()
        start, end = int(start), int(end)
        positions.append((start, end))
    infile.close()
    return positions

def read_exon_regions_v2(filename):
    return [tuple(int(x) for x in line.split())
            for line in open(filename, 'r')]

lactase_exon_regions = read_exon_regions_v2(lactase_exon_file)
print 'Start and end position of the second exon '\
      'of the lactase gene: ', lactase_exon_regions[1]

lactase_exon_regions1 = read_exon_regions_v1(lactase_exon_file)
assert lactase_exon_regions == lactase_exon_regions1

# For simplicity's sake, we will consider mRNA as the concatenation of exons,
# although in reality, additional base pairs are added to each end.

def create_mRNA(gene, exon_regions):
    mrna = ''
    for start, end in exon_regions:
        mrna += gene[start:end].replace('T','U')
    return mrna

mrna = create_mRNA(lactase_gene, lactase_exon_regions)
print '10 last bases of the (coding sequence of the) mRNA '\
      'for the lactase gene: ', mrna[-10:]

# Try a version of create_mRNA where gene is a numpy array
# and where numpy functionality is used (much faster for
# long strings, but create_mRNA is perhaps fast enough)
import numpy as np

def create_mRNA_v2(gene, exon_regions):
    if isinstance(gene, str):
        gene = np.array(gene, dtype='c')
    mrna = np.concatenate(
        [gene[start:end] for start, end in exon_regions])
    mrna[mrna == 'T'] = 'U'
    return mrna

g = 'A'*50000000
exon_regions = [(i, i+1000) for i in range(1, 490000, 10000)]
import time
t0 = time.clock()
create_mRNA(g, exon_regions)
t1 = time.clock()
create_mRNA_v2(g, exon_regions)
t2 = time.clock()
print 'vectorized mRNA:', t2-t1, t1-t0, (t1-t0)/(t2-t1)


def tofile_with_line_sep_v1(text, filename, chars_per_line=70):
    outfile = open(filename, 'w')
    for i in xrange(0, len(text), chars_per_line):
        start = i
        end = start + chars_per_line
        outfile.write(text[start:end] + '\n')
    outfile.close()

def tofile_with_line_sep_v2(text, foldername, filename,
                            chars_per_line=70):
    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    filename = os.path.join(foldername, filename)
    outfile = open(filename, 'w')

    if chars_per_line == 'inf':
        outfile.write(text)
    else:
        for i in xrange(0, len(text), chars_per_line):
            start = i
            end = start + chars_per_line
            outfile.write(text[start:end] + '\n')
    outfile.close()

tofile_with_line_sep_v2(mrna, 'output', 'lactase_mrna.txt')

def create_protein(mrna, genetic_code):
    protein = ''
    for i in xrange(len(mrna)/3):
        start = i * 3
        end = start + 3
        protein += genetic_code[mrna[start:end]]
    return protein

genetic_code = read_genetic_code_v1('genetic_code.tsv')
protein = create_protein(mrna, genetic_code)
tofile_with_line_sep_v2(protein, 'output',
                        'lactase_protein.txt', 70)

def create_protein_fixed(mrna, genetic_code):
    protein_fixed = ''
    trans_start_pos = mrna.find('AUG')
    for i in range(len(mrna[trans_start_pos:])/3):
        start = trans_start_pos + i*3
        end = start + 3
        amino = genetic_code[mrna[start:end]]
        if amino == 'X':
            break
        protein_fixed += amino
    return protein_fixed

protein = create_protein_fixed(mrna, genetic_code)
tofile_with_line_sep_v2(protein, 'output',
                        'lactase_protein_fixed.txt', 70)

print '10 last amino acids of the correct lactase protein: ', \
      protein[-10:]
print 'Lenght of the correct protein: ', len(protein)


def congential_lactase_deficiency(
    lactase_gene,
    genetic_code,
    lactase_exon_regions,
    output_folder=os.curdir,
    mrna_file=None,
    protein_file=None):

    pos = 30049
    mutated_gene = lactase_gene[:pos] + 'A' + lactase_gene[pos+1:]
    mutated_mrna = create_mRNA(mutated_gene, lactase_exon_regions)

    if mrna_file is not None:
        tofile_with_line_sep_v2(
            mutated_mrna, output_folder, mrna_file)

    mutated_protein = create_protein_fixed(
        mutated_mrna, genetic_code)

    if protein_file:
        tofile_with_line_sep_v2(
            mutated_protein, output_folder, protein_file)
    return mutated_protein

mutated_protein = congential_lactase_deficiency(
    lactase_gene, genetic_code, lactase_exon_regions,
    output_folder='output',
    mrna_file='mutated_lactase_mrna.txt',
    protein_file='mutated_lactase_protein.txt')

print '10 last amino acids of the mutated lactase protein:', \
      mutated_protein[-10:]
print 'Lenght of the mutated lactase protein:', \
      len(mutated_protein)
