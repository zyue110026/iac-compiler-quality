from compiler_fuzzing import (
    arguments,
    utils,
    cfg_reader,
    unit_testing,
)

from compiler_fuzzing.ansible_tools import (
    build_module_list,
    generate_ansible_for_modules
)

from compiler_fuzzing.chat_gpt import (
    create_ansible,
    validate_ansible,
    run_ansible,
    generate_statistics,
)
def main():
    args = arguments.parse()
    cfg = cfg_reader.primary.load(args.config)

    if args.procedure == 'generate':
        # run the generator
        create_ansible(args, cfg)

    elif args.procedure == 'validate':
        # run validator
        validate_ansible(args, cfg)
        
    elif args.procedure == 'run':
        # execute playbooks
        run_ansible(args, cfg)    

    elif args.procedure == 'stat':
        # run the generator
        generate_statistics(args, cfg)

    elif args.procedure == 'gen_module_list':
        # generate module list
        build_module_list(args, cfg)
        
        
    elif args.procedure == 'gen_module_ansible':
        # generate module list
        generate_ansible_for_modules(args, cfg)

    elif args.procedure == 'unit_test':
        # run through unit tests
        unit_testing.unit_test(cfg)
        
    else:
        raise NotImplementedError(utils.strings.clean_multiline(
            """
            Procedure added to args but case not added to main function in <project root>/lm_toolkit/__init__.py.
            """
        ))
            
