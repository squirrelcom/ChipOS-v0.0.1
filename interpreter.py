from colorama import init
from basictoken import BASICToken as Token
from lexer import Lexer
from program import Program
from sys import stderr


def main():

    banner = (
        """
         ███████   ███      ███            ███████    ███████  
        ████  ████ ███      ███          ████   ████ ████  ████
        ███    ███ ███                   ███     ███ ████      
        ███        ██████   ███ ██████   ███     ███  ███████   
        ███        ███  ███ ███ ███  ███ ███     ███     █████ 
        ███    ███ ███  ███ ███ ███  ███ ███     ███        ███
        ████  ████ ███  ███ ███ ███ ████ ████   ████ ████  ████ 
          ██████   ███  ███ ███ ██████     ███████     ██████
                                ███                             
                                ███                             
                                ███                             
        """)

    from colorama import Fore, Back, Style
    print(Back.BLUE)
    print(Fore.MAGENTA + (banner))
    print(Fore.BLACK)

    lexer = Lexer()
    program = Program()

    # Continuously accept user input and act on it until
    # the user enters 'EXIT'
    while True:

        stmt = input('> ')

        try:
            tokenlist = lexer.tokenize(stmt)

            # Execute commands directly, otherwise
            # add program statements to the stored
            # BASIC program

            if len(tokenlist) > 0:

                # Exit the interpreter
                if tokenlist[0].category == Token.EXIT:
                    break

                # Add a new program statement, beginning
                # a line number
                elif tokenlist[0].category == Token.UNSIGNEDINT\
                     and len(tokenlist) > 1:
                    program.add_stmt(tokenlist)

                # Delete a statement from the program
                elif tokenlist[0].category == Token.UNSIGNEDINT \
                        and len(tokenlist) == 1:
                    program.delete_statement(int(tokenlist[0].lexeme))

                # Execute the program
                elif tokenlist[0].category == Token.RUN:
                    try:
                        program.execute()

                    except KeyboardInterrupt:
                        print("Program terminated")

                # List the program
                elif tokenlist[0].category == Token.LIST:
                    program.list()

                # Save the program to disk
                elif tokenlist[0].category == Token.SAVE:
                    program.save(tokenlist[1].lexeme)
                    print("Program written to file")

                # Load the program from disk
                elif tokenlist[0].category == Token.LOAD:
                    program.load(tokenlist[1].lexeme)
                    print("Program read from file")

                # Delete the program from memory
                elif tokenlist[0].category == Token.NEW:
                    program.delete()

                # Unrecognised input
                else:
                    print("Unrecognised input", file=stderr)
                    for token in tokenlist:
                        token.print_lexeme()
                    print(flush=True)

        # Trap all exceptions so that interpreter
        # keeps running
        except Exception as e:
            print(e, file=stderr, flush=True)


if __name__ == "__main__":
    main()
