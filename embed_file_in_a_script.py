#!/usr/bin/env python3

"""
Script:	embed_file_in_a_script.py
Date:	2019-04-10

Platform: MacOS

Description:
Creates a script that will unpack a file embedded into it
You can ad on to the script to perform different operations
"""
__author__ = 'thedzy'
__copyright__ = 'Copyright 2018, thedzy'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'thedzy'
__email__ = 'thedzy@hotmail.com'
__status__ = 'Developer'

import optparse
import os
import uu


def main(script, infile, outfile):
    """
    Write a script and embed the infile.  On run of the script it will create the outfile
    :param script: (String) Path to script to be created
    :param infile: (String) Path to infile to be embedded
    :param outfile: (String) Path to outfile that will be created
    :return:
        2: Problem validating path/files
    """

    # If no script is specified. use the name of the infile as a template
    if script is None:
        infile_path = os.path.dirname(infile)
        if os.path.isdir(infile_path):
            script = '{0}/{1}_expand.py'.format(infile_path, os.path.basename(infile).replace('.', '_'))
        else:
            print('Path to infile is invalid, check destination and try again')
            exit(2)

    # If no outfile, assume the outfile will be the same file
    if outfile is None:
        outfile = infile

    # Cannot proceed without a file to embed
    if not os.path.isfile(infile):
        print('File to embed cannot be found, check destination and try again')
        exit(2)

    # Temporary file to contain the uuencode data
    tmp_path = '/tmp/' + os.path.splitext(os.path.basename(infile))[0] + '.tmp'

    # print summary
    print('{0:10s} : {1}'.format('infile', infile))
    print('{0:10s} : {1}'.format('outfile', outfile))
    print('{0:10s} : {1}'.format('script', script))

    # Header of the script
    header = '\n'.join([
        '#!/usr/bin/env python3\n',
        'import uu\n',
        'data = """',
    ])

    # Footer of the script
    footer = '\n'.join([
        '"""\n',
        'with open("{0}", "w") as tmp_file:'.format(tmp_path),
        '   tmp_file.write(data)',
        '   tmp_file.close()',
        'uu.decode("{0}")'.format(tmp_path),
        '',
        '## TODO: Insert code to work with file unpacked',
        '',
        'exit()\n',
    ])

    # Write the script
    try:
        uu.encode(infile, tmp_path, outfile)
        tmp_file = open(tmp_path)
        with open(script, 'w') as script_file:
            script_file.write(header)
            script_file.write(tmp_file.read())
            script_file.write(footer)
            script_file.close()
    except uu.Error as err:
        print(err)
        exit(3)

    # Make the script executable
    os.chmod(script, 0o755)

    return 0


if __name__ == '__main__':
    # Create the parser and give it the program version #
    parser = optparse.OptionParser('%prog [options]\nCreate a script that will embed a file.  '
                                   'The script can be added on to to handle the file.  '
                                   'Example: A image can be embedded and then we set as the wallpaper', version='%prog 1.0', )


    # Store an option
    parser.add_option('-o', '--outfile',
                      action='store', dest='outfile', default=None,
                      help='OutFile: The file that will be created, when the new script is run')
    # Store infile
    parser.add_option('-i', '--infile',
                      action='store', dest='infile', default=None,
                      help='InFile: The file that will read the create the script')

    # Store script
    parser.add_option('-s', '--script',
                      action='store', dest='script', default=None,
                      help='IScript: The script that will host the InFile')

    options, args = parser.parse_args()

    if options.infile is None:
        print('You require an input file')
        exit(1)

    success = main(options.script, options.infile, options.outfile)
    exit(success)
