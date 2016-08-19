# -*- coding: utf-8 -*-
""" Clearing house for generic text datatypes that are not XML or tabular.
"""

import gzip
import json
import logging
import os
import re
import subprocess
import tempfile

from galaxy.datatypes.data import get_file_peek, Text
from galaxy.datatypes.metadata import MetadataElement
from galaxy.datatypes.metadata import ListParameter
from galaxy.datatypes.metadata import MetadataParameter
from galaxy.util import nice_size, string_as_bool

import logging

log = logging.getLogger(__name__)

class Html( Text ):
    """Class describing an html file"""
    edam_format = "format_2331"
    file_ext = "html"

    def set_peek( self, dataset, is_multi_byte=False ):
        if not dataset.dataset.purged:
            dataset.peek = "HTML file"
            dataset.blurb = nice_size( dataset.get_size() )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def get_mime(self):
        """Returns the mime type of the datatype"""
        return 'text/html'

    def sniff( self, filename ):
        """
        Determines whether the file is in html format
        >>> from galaxy.datatypes.sniff import get_test_fname
        >>> fname = get_test_fname( 'complete.bed' )
        >>> Html().sniff( fname )
        False
        >>> fname = get_test_fname( 'file.html' )
        >>> Html().sniff( fname )
        True
        """
        headers = get_headers( filename, None )
        try:
            for i, hdr in enumerate(headers):
                if hdr and hdr[0].lower().find( '<html>' ) >= 0:
                    return True
            return False
        except:
            return True


class Json( Text ):
    edam_format = "format_3464"
    file_ext = "json"
    blurb = "JavaScript Object Notation (JSON)"

    def set_peek(self, dataset, is_multi_byte=False):
        if not dataset.dataset.purged:
            dataset.peek = get_file_peek(dataset.file_name, is_multi_byte=is_multi_byte)
            dataset.blurb = self.blurb
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disc'

    def sniff(self, filename):
        """
            Try to load the string with the json module. If successful it's a json file.
        """
        log.info("JSON sniffing %s", filename)
        return self._looks_like_json(filename)

    def _looks_like_json(self, filename):
        # Pattern used by SequenceSplitLocations
        if os.path.getsize(filename) < 50000:
            # If the file is small enough - don't guess just check.
            try:
                json.load(open(filename, "r"))
                return True
            except Exception:
                return False
        else:
            with open(filename, "r") as fh:
                ch = self.read(fh)
                return ch == '{' or ch == '['
            #     while True:
            #         line = fh.readline()
            #         line = line.strip()
            #         if line:
            #             # simple types are valid JSON as well - but would such a file
            #             # be interesting as JSON in Galaxy?
            #             return line.startswith("[") or line.startswith("{")
            # return False


    def read(self, f):
        """
        Reads a single character from the file handle skipping over whitespace.

        :param f: an open file handle
        :return: the next non-whitespace character in the file.
        """
        c = f.read(1)
        while c.isspace():
            c = f.read(1)
        # end while
        return c

    # end read
    def display_peek(self, dataset):
        try:
            return dataset.peek
        except:
            return "JSON file (%s)" % ( nice_size(dataset.get_size()) )


class Lapps( Json ):
    """
        Lapps Container.

        A Lapps container is a JSON map with exactly two entries:
        - discriminator
        - payload

        Both the discriminator and payload are string objects, with the value
        of the discriminator being used to determine how the payload should be
        interpreted.

        This means we can identify a LAPPS document by searching for something
        that looks like JSON and starts with a key named "discriminator".
    """
    file_ext = "lapps"
    header = '''{"discriminator":'''
    blurb = "Lapps Data object"

    # MetadataElement(name="annotations", desc="Annotations added during processing", default=[], param=ListParameter, readonly=False, visible=True, no_value=[])
    #
    # def __init__(self, **kwd):
    #     Json.__init__(self, **kwd)
    #
    # def init_meta( self, dataset, copy_from=None ):
    #     Json.init_meta(self, dataset, copy_from=copy_from)


    def sniff(self, filename):
        """
        Reads the start of the file (ignoring whitespace) looking for the
        required LIF header.

        :param filename: The name of the file to be checked.
        :return: True if filename is a LIF file, False otherwise.
        """
        log.info("LAPPS sniffing %s", filename)
        with open(filename, "r") as fh:
            for c in self.header:
                if c != self.read(fh):
                    return False

        log.info("Sniffed a LAPPS file.")
        return True


class Lif( Lapps ):
    """
        The Lapps Interchange Format.

        LIF files are json files conforming to the schema at
        http://vocab.lappsgrid.org/schema/lif.json  If we ignore whitespace
        we know EXACTLY what the opening sequence of characters will be.

    """
    file_ext = "lif"
    header = '''{"discriminator":"http://vocab.lappsgrid.org/ns/media/jsonld"'''
    blurb = "Lapps Interchange Format (LIF)"

    # def __init__(self, **kwd):
    #     Lapps.__init__(self, **kwd)
    #
    # def init_meta( self, dataset, copy_from=None ):
    #     Lapps.init_meta(self, dataset, copy_from=copy_from)

    def sniff(self, filename):
        """
        Reads the start of the file (ignoring whitespace) looking for the
        required LIF header.

        :param filename: The name of the file to be checked.
        :return: True if filename is a LIF file, False otherwise.
        """
        log.info("LIF: Sniffing %s", filename)
        with open(filename, "r") as fh:
            for c in self.header:
                if c != self.read(fh):
                    return False

        log.info("Found a LIF file.")
        return True


class Gate( Lapps ):
    """
        GATE/XML in a JSON wrapper.
        See: http://gate.ac.uk
    """
    file_ext = "gate"
    header = '{"discriminator":"http://vocab.lappsgrid.org/ns/media/xml#gate"'
    blurb = "Gate/XML in a Lapps Container"

    # def __init__(self, **kwd):
    #     Lapps.__init__(self, **kwd)
    #
    # def init_meta( self, dataset, copy_from=None ):
    #     Lapps.init_meta(self, dataset, copy_from=copy_from)

    def sniff(self, filename):
        """
        Reads the start of the file (ignoring whitespace) looking for the
        required GATE header.

        :param filename: The name of the file to be checked.
        :return: True if filename is a GATE file, False otherwise.
        """
        log.info("GATE: Sniffing %s", filename)
        with open(filename, "r") as fh:
            for c in self.header:
                if c != self.read(fh):
                    return False

        log.info("Found a GATE file.")
        return True


class LDC( Lapps ):
    """
        LDC/XML in a JSON wrapper.

    """
    file_ext = "ldc"
    header = '{"discriminator":"http://vocab.lappsgrid.org/ns/media/xml#ldc"'
    blurb = "LDC/XML in a Lapps Container"

    # def __init__(self, **kwd):
    #     Lapps.__init__(self, **kwd)
    #
    # def init_meta( self, dataset, copy_from=None ):
    #     Lapps.init_meta(self, dataset, copy_from=copy_from)

    def sniff(self, filename):
        """
        Reads the start of the file (ignoring whitespace) looking for the
        required GATE header.

        :param filename: The name of the file to be checked.
        :return: True if filename is a GATE file, False otherwise.
        """
        log.info("LDC: Sniffing %s", filename)
        with open(filename, "r") as fh:
            for c in self.header:
                if c != self.read(fh):
                    return False

        log.info("Found a LDC file.")
        return True


class Ipynb(Json):
    file_ext = "ipynb"

    def set_peek(self, dataset, is_multi_byte=False):
        if not dataset.dataset.purged:
            dataset.peek = get_file_peek(dataset.file_name, is_multi_byte=is_multi_byte)
            dataset.blurb = "IPython Notebook"
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disc'

    def sniff(self, filename):
        """
            Try to load the string with the json module. If successful it's a json file.
        """
        if self._looks_like_json(filename):
            try:
                ipynb = json.load(open(filename))
                if ipynb.get('nbformat', False) is not False and ipynb.get('metadata', False):
                    return True
                else:
                    return False
            except:
                return False

    def display_data(self, trans, dataset, preview=False, filename=None, to_ext=None, chunk=None, **kwd):
        config = trans.app.config
        trust = getattr(config, 'trust_ipython_notebook_conversion', False)
        if trust:
            return self._display_data_trusted(trans, dataset, preview=preview, fileame=filename, to_ext=to_ext,
                                              chunk=chunk, **kwd)
        else:
            return super(Ipynb, self).display_data(trans, dataset, preview=preview, fileame=filename, to_ext=to_ext,
                                                   chunk=chunk, **kwd)

    def _display_data_trusted(self, trans, dataset, preview=False, filename=None, to_ext=None, chunk=None, **kwd):
        preview = string_as_bool( preview )
        if chunk:
            return self.get_chunk(trans, dataset, chunk)
        elif to_ext or not preview:
            return self._serve_raw(trans, dataset, to_ext)
        else:
            ofile_handle = tempfile.NamedTemporaryFile(delete=False)
            ofilename = ofile_handle.name
            ofile_handle.close()
            try:
                cmd = 'ipython nbconvert --to html --template full %s --output %s' % (dataset.file_name, ofilename)
                log.info("Calling command %s" % cmd)
                subprocess.call(cmd, shell=True)
                ofilename = '%s.html' % ofilename
            except:
                ofilename = dataset.file_name
                log.exception(
                    'Command "%s" failed. Could not convert the IPython Notebook to HTML, defaulting to plain text.' % cmd)
            return open(ofilename)

    def set_meta(self, dataset, **kwd):
        """
        Set the number of models in dataset.
        """
        pass


class Obo(Text):
    """
        OBO file format description
        http://www.geneontology.org/GO.format.obo-1_2.shtml
    """
    edam_format = "format_2549"
    file_ext = "obo"

    def set_peek(self, dataset, is_multi_byte=False):
        if not dataset.dataset.purged:
            dataset.peek = get_file_peek(dataset.file_name, is_multi_byte=is_multi_byte)
            dataset.blurb = "Open Biomedical Ontology (OBO)"
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disc'

    def sniff(self, filename):
        """
            Try to guess the Obo filetype.
            It usually starts with a "format-version:" string and has several stanzas which starts with "id:".
        """
        stanza = re.compile(r'^\[.*\]$')
        with open(filename) as handle:
            first_line = handle.readline()
            if not first_line.startswith('format-version:'):
                return False

            for line in handle:
                if stanza.match(line.strip()):
                    # a stanza needs to begin with an ID tag
                    if handle.next().startswith('id:'):
                        return True
        return False


class Arff(Text):
    """
        An ARFF (Attribute-Relation File Format) file is an ASCII text file that describes a list of instances sharing a set of attributes.
        http://weka.wikispaces.com/ARFF
    """
    file_ext = "arff"

    """Add metadata elements"""
    MetadataElement(name="comment_lines", default=0, desc="Number of comment lines", readonly=True, optional=True,
                    no_value=0)
    MetadataElement(name="columns", default=0, desc="Number of columns", readonly=True, visible=True, no_value=0)

    def set_peek(self, dataset, is_multi_byte=False):
        if not dataset.dataset.purged:
            dataset.peek = get_file_peek(dataset.file_name, is_multi_byte=is_multi_byte)
            dataset.blurb = "Attribute-Relation File Format (ARFF)"
            dataset.blurb += ", %s comments, %s attributes" % (
                dataset.metadata.comment_lines, dataset.metadata.columns )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disc'

    def sniff(self, filename):
        """
            Try to guess the Arff filetype.
            It usually starts with a "format-version:" string and has several stanzas which starts with "id:".
        """
        with open(filename) as handle:
            relation_found = False
            attribute_found = False
            prefix = ""
            for line_count, line in enumerate(handle):
                if line_count > 1000:
                    # only investigate the first 1000 lines
                    return False
                line = line.strip()
                if not line:
                    continue

                start_string = line[:20].upper()
                if start_string.startswith("@RELATION"):
                    relation_found = True
                elif start_string.startswith("@ATTRIBUTE"):
                    attribute_found = True
                elif start_string.startswith("@DATA"):
                    # @DATA should be the last data block
                    if relation_found and attribute_found:
                        return True
        return False

    def set_meta(self, dataset, **kwd):
        """
            Trying to count the comment lines and the number of columns included.
            A typical ARFF data block looks like this:
            @DATA
            5.1,3.5,1.4,0.2,Iris-setosa
            4.9,3.0,1.4,0.2,Iris-setosa
        """
        if dataset.has_data():
            comment_lines = 0
            first_real_line = False
            data_block = False
            with open(dataset.file_name) as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith('%') and not first_real_line:
                        comment_lines += 1
                    else:
                        first_real_line = True
                    if data_block:
                        if line.startswith('{'):
                            # Sparse representation
                            """
                                @data
                                0, X, 0, Y, "class A", {5}
                            or
                                @data
                                {1 X, 3 Y, 4 "class A"}, {5}
                            """
                            token = line.split('}', 1)
                            first_part = token[0]
                            last_column = first_part.split(',')[-1].strip()
                            numeric_value = last_column.split()[0]
                            column_count = int(numeric_value)
                            if len(token) > 1:
                                # we have an additional weight
                                column_count -= 1
                        else:
                            columns = line.strip().split(',')
                            column_count = len(columns)
                            if columns[-1].strip().startswith('{'):
                                # we have an additional weight at the end
                                column_count -= 1

                        # We have now the column_count and we know the initial comment lines. So we can terminate here.
                        break
                    if line[:5].upper() == "@DATA":
                        data_block = True
        dataset.metadata.comment_lines = comment_lines
        dataset.metadata.columns = column_count


class SnpEffDb(Text):
    """Class describing a SnpEff genome build"""
    file_ext = "snpeffdb"
    MetadataElement(name="genome_version", default=None, desc="Genome Version", readonly=True, visible=True,
                    no_value=None)
    MetadataElement(name="regulation", default=[], desc="Regulation Names", readonly=True, visible=True, no_value=[],
                    optional=True)
    MetadataElement(name="annotation", default=[], desc="Annotation Names", readonly=True, visible=True, no_value=[],
                    optional=True)

    def __init__(self, **kwd):
        Text.__init__(self, **kwd)

    def set_meta(self, dataset, **kwd):
        Text.set_meta(self, dataset, **kwd)
        data_dir = dataset.extra_files_path
        # search data_dir/genome_version for files
        regulation_pattern = 'regulation_(.+).bin'
        #  annotation files that are included in snpEff by a flag
        annotations_dict = {'nextProt.bin' : '-nextprot', 'motif.bin': '-motif'}
        regulations = []
        annotations = []
        if data_dir and os.path.isdir(data_dir):
            for root, dirs, files in os.walk(data_dir):
                for fname in files:
                    if fname.startswith('snpEffectPredictor'):
                        # if snpEffectPredictor.bin download succeeded
                        genome_version = os.path.basename(root)
                        dataset.metadata.genome_version = genome_version
                    else:
                        m = re.match(regulation_pattern, fname)
                        if m:
                            name = m.groups()[0]
                            regulations.append(name)
                        elif fname in annotations_dict:
                            value = annotations_dict[fname]
                            name = value.lstrip('-')
                            annotations.append(name)
            dataset.metadata.regulation = regulations
            dataset.metadata.annotation = annotations
            try:
                fh = file(dataset.file_name, 'w')
                fh.write("%s\n" % genome_version)
                if annotations:
                    fh.write("annotations: %s\n" % ','.join(annotations))
                if regulations:
                    fh.write("regulations: %s\n" % ','.join(regulations))
                fh.close()
            except:
                pass


class SnpSiftDbNSFP(Text):
    """Class describing a dbNSFP database prepared fpr use by SnpSift dbnsfp """
    MetadataElement(name='reference_name', default='dbSNFP', desc='Reference Name', readonly=True, visible=True,
                    set_in_upload=True, no_value='dbSNFP')
    MetadataElement(name="bgzip", default=None, desc="dbNSFP bgzip", readonly=True, visible=True, no_value=None)
    MetadataElement(name="index", default=None, desc="Tabix Index File", readonly=True, visible=True, no_value=None)
    MetadataElement(name="annotation", default=[], desc="Annotation Names", readonly=True, visible=True, no_value=[])
    file_ext = "snpsiftdbnsfp"
    composite_type = 'auto_primary_file'
    allow_datatype_change = False
    """
    ## The dbNSFP file is a tabular file with 1 header line
    ## The first 4 columns are required to be: chrom	pos	ref	alt
    ## These match columns 1,2,4,5 of the VCF file
    ## SnpSift requires the file to be block-gzipped and the indexed with samtools tabix
    ## Example:
    ## Compress using block-gzip algorithm
    bgzip dbNSFP2.3.txt
    ## Create tabix index
    tabix -s 1 -b 2 -e 2 dbNSFP2.3.txt.gz
    """
    def __init__( self, **kwd ):
        Text.__init__( self, **kwd )
        self.add_composite_file( '%s.grp', description='Group File', substitute_name_with_metadata='reference_name', is_binary=False )
        self.add_composite_file( '%s.ti', description='', substitute_name_with_metadata='reference_name', is_binary=False )

    def init_meta( self, dataset, copy_from=None ):
        Text.init_meta( self, dataset, copy_from=copy_from )

    def generate_primary_file( self, dataset=None ):
        """
        This is called only at upload to write the html file
        cannot rename the datasets here - they come with the default unfortunately
        """
        self.regenerate_primary_file( dataset )

    def regenerate_primary_file(self, dataset):
        """
        cannot do this until we are setting metadata
        """
        annotations = "dbNSFP Annotations: %s\n" % ','.join(dataset.metadata.annotation)
        f = open(dataset.file_name, 'a')
        if dataset.metadata.bgzip:
            bn = dataset.metadata.bgzip
            f.write(bn)
            f.write('\n')
        f.write(annotations)
        f.close()

    def set_meta( self, dataset, overwrite=True, **kwd ):
        try:
            efp = dataset.extra_files_path
            if os.path.exists(efp):
                flist = os.listdir(efp)
                for i, fname in enumerate(flist):
                    if fname.endswith('.gz'):
                        dataset.metadata.bgzip = fname
                        try:
                            fh = gzip.open(os.path.join(efp, fname), 'r')
                            buf = fh.read(5000)
                            lines = buf.splitlines()
                            headers = lines[0].split('\t')
                            dataset.metadata.annotation = headers[4:]
                        except Exception as e:
                            log.warn("set_meta fname: %s  %s" % (fname, str(e)))
                        finally:
                            fh.close()
                    if fname.endswith('.tbi'):
                        dataset.metadata.index = fname
            self.regenerate_primary_file(dataset)
        except Exception as e:
            log.warn("set_meta fname: %s  %s" % (dataset.file_name if dataset and dataset.file_name else 'Unkwown', str(e)))
