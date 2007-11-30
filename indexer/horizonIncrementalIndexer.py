#   Copyright 2007 Casey Durfee
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

## the incremental indexer indexes all unprocessed PMS* files in order, deleting them after completing processing.
import glob, os, time
import indexerDriver
from loadPropsFile import *

indexerConfig = loadPropsFile("config/indexer.properties")

HORIZON_BASE_DIR = indexerConfig.get("HORIZON_BASE_DIR")
BETWEEN_RECORD_DELIMITER = indexerConfig.get("HORIZON_BETWEEN_RECORD_DELIMITER")
DO_OPTIMIZE_AFTER_INCREMENTAL_INDEX = indexerConfig.get("DO_OPTIMIZE_AFTER_INCREMENTAL_INDEX")


def processPMSFile( fInName ):
    """takes the name of a PMS file, extracts just the MARC data from it, writes it to a file,
    and returns the name of the file just created and a list of bibs that should be deleted."""
    fOutName = "%s.MARC" % fInName
    fIn = open( fInName )
    marcRecords = []    # this is the best way to avoid a lot of string concatenation.
    deletedBibs = []
    lines = fIn.readlines()    # must do this because jython, not pure python so can't do for line in file:
    fIn.close()
    for lineOn in lines:
        if not lineOn.startswith("B"):
            pass
        # find start of MARC record (after 3rd comma in string )
        else:
            commaAt = 0
            for i in range(3):
                commaAt = lineOn.find(",", commaAt+1)
            assert commaAt != 0, "problem parsing line!!!"
            dataOn = lineOn[ commaAt+1: ].strip()
            # if this is not a delete command, add it to the data
            if dataOn[5] == 'd':    # indicates this is a deleted record
                bib = lineOn.split(",")[0][1:]  # b123345,asdf,... -> 123345
                print "adding delete command for %s" % bib
                deletedBibs.append( bib )
            else:
                marcRecords.append( dataOn )
    if len(marcRecords) >0 :
        data = BETWEEN_RECORD_DELIMITER.join( marcRecords )
        data += BETWEEN_RECORD_DELIMITER    # need this after last one...
        fOut = open( fOutName, "w" )
        fOut.write( data )
        fOut.flush()
        fOut.close()
    else:
        fOutName = None
    return fOutName, deletedBibs

if __name__ == '__main__':
    pmsFiles = glob.glob( "%s/PMS*.DAT" % HORIZON_BASE_DIR )
    for fileOn in pmsFiles:
        print "processing PMS file %s" % fileOn
        processedFilenameOn, deletedBibsOn = processPMSFile(fileOn)
        if processedFilenameOn:
            print "processing MARC file %s" % processedFilenameOn
            indexerDriver.processFile( processedFilenameOn )
            
            # now that we are done processing the file, we delete it.
            print "deleting MARC file %s " % processedFilenameOn
            os.remove( processedFilenameOn )
            print "deleting PMS file %s" % fileOn
            os.remove( fileOn )
            
            if deletedBibsOn:
                print "processing deleted bibs from MARC file %s" % processedFilenameOn
                for bibOn in deletedBibsOn:
                    print "deleting bib %s" % bibOn
                    indexerDriver.deleteRecord( bibOn )
        else:
            print "no records to index"
            os.remove( fileOn )
    # finally, do a commit here.
    print "starting final commit"
    indexerDriver.commit()
    
    # finally, do an optimize here
    if DO_OPTIMIZE_AFTER_INCREMENTAL_INDEX:
        print "starting final optimize"
        indexerDriver.optimize()    # csdebug
        from facetWarmer import *
        warmFacets()
    
