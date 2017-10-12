import os.path
import sys
import urllib.request
import pandas as pd


def read_taxid_list(filename, dict=None):
    """ Read a taxID list file.

    A taxID list file consists of three tab separated columns: 1. ID type,
    2. ID of sequence, 3. NCBI taxonomy ID for the sequence. It is headed by
    one line starting with the '#' char.

    Parameters
    ----------
    filename : str
        Path to the file containing the taxID list.
    dict : dict
        Optional. Provide an existing dictionary into which parsed results
        should be added. Useful if the taxID list consists of several files.

    Returns
    -------
    A dict of dict. First dict's keys are the sequence types, e.g. "gi",
    "GeneID", "NC". Second level keys are the sequence IDs and their values are
    the according NCBI taxonomy IDs, or taxIDs for short.

    Raises
    ------
    IOError
        If the file cannot be read.
    ValueError
        If a line does not contain of exactly three tab delimited fields.
    """
    if dict is None:
        dict = {}
    try:
        f = open(filename, 'r')
        f.readline()  # header
        for line in f:
            try:
                type, accession, taxid = line.rstrip().split("\t")
                if type not in dict:
                    dict[type] = {}
                dict[type][accession] = int(taxid)
            except ValueError:
                f.close()
                raise ValueError("Error parsing line '%s' of file '%s'" %
                                 (line, filename))

        f.close()
        return dict
    except IOError:
        raise IOError('Cannot read file "%s"' % filename)


def read_metaphlan_markers_info(filename):
    """ Reads the MetaPhlAn markers_info.txt file.

    MetaPhlAn's OTU analogous are 'clades'. Currently, they have around 8900.
    A 'clade' is composed of one or many (sub)sequences of specific marker
    genes. Those marker genes come from three sources: 1) genbank: "^gi|",
    2) gene: "^GeneID:", and 3) NCBI nr: "^NC_".

    Parameters
    ----------
    filename : str
        Path to the filename 'markers_info' of MetaPhlAn.

    Returns
    -------
    A dict with an entry for each 'clade'. Their values are dicts themselves,
    with keys that refer to one of the three sequence sources. And their values
    are sets of marker gene IDs. For example:
    's__Escherichia_phage_vB_EcoP_G7C': {'GeneID': {'11117645', '11117646'}}

    Raises
    ------
    IOError
        If the file cannot be read.
    """
    clades = {}
    try:
        file = open(filename, 'r')
        for line in file:
            if line.startswith('gi|'):
                type_ids = 'gi'
                accession = (line.split('\t')[0]).split('|')[1]
            elif line.startswith('GeneID:'):
                type_ids = 'GeneID'
                accession = (line.split('\t')[0]).split(':')[1]
            elif line.startswith('NC_'):
                type_ids = 'NC'
                accession = line.split('\t')[0]
            else:
                type_ids = None
                accession = None

            if (type_ids is not None) and (accession is not None):
                clade = line.split("clade': '")[1].split("'")[0]
                if clade not in clades:
                    clades[clade] = {}
                if type_ids not in clades[clade]:
                    clades[clade][type_ids] = {}
                clades[clade][type_ids][accession] = True

        for clade in clades:
            for type_id in clades[clade]:
                clades[clade][type_id] = set(clades[clade][type_id].keys())

        file.close()
        return clades

    except IOError:
        raise IOError('Cannot read file "%s"' % filename)


def _read_ncbitaxonomy_file(filename):
    """ A generic function to read an NCBI taxonomy file, which is delimited
    by '\t|\t?'.

    Parameters
    ----------
    filename : str
        Path to a file from an NCBI taxonomy dump.

    Returns
    -------
    A dict. Key = first field of file, Value = second field of file.

    Raises
    ------
    IOError
        If the file cannot be read.
    ValueError
        If IDs of entries cannot be converted into int.
    """
    entries = {}
    try:
        file = open(filename, 'r')
        for line in file:
            fields = list(map(str.strip, line.split('|')))
            try:
                entries[int(fields[0])] = int(fields[1])
            except ValueError:
                file.close()
                raise ValueError("cannot convert entry IDs (%s, %s) to int."
                                 % (fields[0], fields[1]))

        file.close()
        return entries

    except IOError:
        raise IOError('Cannot read file "%s"' % filename)


def read_ncbi_merged(filename):
    """ Reads NCBI's merged.dmp file and returns a dict of old and merged IDs.

    Parameters
    ----------
    filename : str
        Path to the filename 'merged.dmp' of NCBI's taxonomy.

    Returns
    -------
    A dict, where keys are old IDs and their values are the new merged IDs.

    Raises
    ------
    IOError
        If the file cannot be read.
    ValueError
        If IDs of old or merged nodes cannot be converted into int.
    """
    return _read_ncbitaxonomy_file(filename)


def update_taxids(input, updatedTaxids):
    """ Updates a map of sequenceIDs to taxIDs with information from merged.dmp

    Some of NCBI's taxonomy IDs might get merged into others. Older sequences
    can still point to the old taxID. The new taxID must be looked up in the
    merged.dmp file in order to be able to find the right node in the taxonomy
    tree.

    Parameters
    ----------
    input : dict of dicts of sets
        The keys of the outer dicts are the sequence types, e.g. NC, GeneID or
        gi. Keys of the inner dict are OTUs or clades. Values of the inner
        dict are sets of taxIDs.
    updatedTaxids : dict
        Content of merged.dmp in form of a dict where key is current taxID and
        value the new taxID

    Returns
    -------
    The original map, but some taxIDs might have been updated.
    """
    for seqType in input:
        for seqID in input[seqType]:
            cur_taxid = input[seqType][seqID]
            if cur_taxid in updatedTaxids:
                input[seqType][seqID] = updatedTaxids[cur_taxid]
    return input


def generate_map_metaphlan2_ncbitaxids(filename_map, latest_mergeddump=None):
    """Creates an ID map from metaphlan2 to NCBI taxonomy IDs.

    For every metaphlan2 database, we once need to create a map from their
    clade names to NCBI taxonomy IDs. Since a clade is a set of several
    sequences which can stem from different organisms, one clade can point to
    multiple NCBI taxonomy IDs.
    The resulting format is one clade per row, tab separated, first column is
    clade name, second column holds a comma separated list of NCBI taxonomy
    IDs.

    The file 'Metaphlan/markers_info.txt' is part of metaphlans repository:
        https://bitbucket.org/biobakery/metaphlan2/src/f19f7cfdc990aa9f2d983
        7a89bcc5188912c8a82/utils/markers_info.txt.bz2?at=default&fileviewer
        =file-view-default
    The file 'metaphlan2_taxids.txt' is the result of a lengthy query against
    NCBI and can be found here:
        https://github.com/sjanssen2/ggmap/blob/master/Cache/
        taxids_metaphlan.txt

    Parameters
    ----------
    filename_map : str
        The filepath for the resulting map from metaphlan2 clades to NCBI
        taxonomy IDs.
    latest_mergeddump : str
        Filepath to "merged.dmp" file of a NCBI taxonomy dump. TaxIDs might
        have changed between this dump and the generation of the file
        "metaphlan2_taxids.txt", thus these IDs need to be updated.
    """

    filename_metaphlan2_marker = "markers_info.txt"
    if not os.path.exists(filename_metaphlan2_marker):
        sys.stderr.write(
            ('The "markers_info.txt" file from metaphlan2 is missing. Please '
             'browse to https://bitbucket.org/biobakery/metaphlan2/raw/f19f7c'
             'fdc990aa9f2d9837a89bcc5188912c8a82/utils/markers_info.txt.bz2 d'
             'ownload and extract the file and try again.'))

    filename_taxids = 'metaphlan2_taxids.txt'
    if not os.path.exists(filename_taxids):
        urllib.request.urlretrieve(
            ("https://raw.githubusercontent.com/sjanssen2/ggmap/master/"
             "Cache/taxids_metaphlan.txt"),
            filename_taxids)

    # reads a precompiled map of taxIDs for every sequence used in creating
    # metaphlans database
    taxids_metaphlan = read_taxid_list(filename_taxids)

    # reads the markers_info.txt file shipped with metaphlan which defines of
    # which sequences a metahplan clade is composed
    clades_metaphlan = read_metaphlan_markers_info(filename_metaphlan2_marker)

    if latest_mergeddump is not None:
        merged = read_ncbi_merged(latest_mergeddump)
        # update taxonomy IDs for metaphlan sequences
        taxids_metaphlan = update_taxids(taxids_metaphlan, merged)

    # iterates over all metaphlan clades and translates the sequence IDs of the
    # clade into NCBI taxonomy IDs
    _map = []
    for clade in clades_metaphlan.keys():
        taxids = set()
        for _type in clades_metaphlan[clade].keys():
            for _id in clades_metaphlan[clade][_type]:
                taxids |= set([taxids_metaphlan[_type][_id]])
        _map.append({'metaphlan2_clade': clade,
                     'NCBI_taxids': ",".join(map(str, taxids))})
    _map = pd.DataFrame(_map)[['metaphlan2_clade', 'NCBI_taxids']]

    # write the resulting map into a tab separated file
    _map.to_csv(filename_map, sep="\t", index=False)


if __name__ == '__main__':
    generate_map_metaphlan2_ncbitaxids(
        'map_metaphlanclade_ncbitaxids.tsv',
        '/home/qiz173/Databases/stdb/20170803/raw/taxdump/merged.dmp')
