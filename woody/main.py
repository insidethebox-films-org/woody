from woody.pywoody import Woody
from woody.cli.cli import CLI

def main():
    app = Woody()
    app.run()
    
    cli = CLI()
    cli.start()

if __name__ == "__main__":
    main()
    