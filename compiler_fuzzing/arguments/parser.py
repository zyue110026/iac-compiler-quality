import argparse
from compiler_fuzzing.utils import files, strings

def parse():
    """
    parse the command line arguments
    """

    # define arguments and parse
    parser = argparse.ArgumentParser() 

    # create subparser for procedures
    subparser = parser.add_subparsers(
        description='decides on which procedure to run',
        required=True,
        dest='procedure',
    )

    # add subparser for playbook generation
    parser_gen = subparser.add_parser('generate')
    parser_gen.add_argument(
        '-c',
        '--config',
        help='config path',
        type=str,
        default="{{PROJECT_ROOT}}/confs/config.yaml",
    )

    parser_gen.add_argument(
        '--debug',
        help='used for testing the create_ansible function',
        action='store_true',
        default=False,
    )

    args = parser.parse_args()

    # perform substitutions
    args.config = strings.replace_slot(
        args.config, 
        { 'PROJECT_ROOT' : files.get_project_root() }
    )

    return args
