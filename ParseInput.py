#!usr/bin/python2.7
import optparse
import hashlib
import getpass
import random


class ParseInput:
    def __init__(self):
        self.config = {
            "ips": str(),
            "output": "bots.txt",

            "verbose": False,
            "threads": 10,

            "ssh_port": 22,
            "ssh_user": str(),
            "ssh_pass": str()
        }

    def check_input(self):
        parser = optparse.OptionParser("%prog -f <bot_file>")
        parser.add_option("-f", dest="ips", help="plain text ips file")
        parser.add_option("-o", dest="output", help="successful bots output file name")
        parser.add_option("-t", dest="threads", help="threads to run program with")
        parser.add_option("-v", dest="verbose", action="store_true", help="verbose every attempt")
        (options, args) = parser.parse_args()
        self.save_config(parser, options)
        self.ssh_credentials()
        self.print_information()
        return self.config

    def save_config(self, parser, options):
        if not options.ips:
            parser.print_help()
            exit(0)

        self.config["ips"] = self.read_file(options.ips) if self.check_file(options.ips) else None
        self.config["verbose"] = True if options.verbose else False

        if options.output:
            self.config["output"] = self.check_file(options.output)

        if options.threads:
            self.config["threads"] = self.check_range(int(options.threads), 1, 100)

    def check_file(self, filename):
        if filename.endswith(".txt"):
            return filename
        else:
            print("[-] %s using an invalid format. [file_name].txt" % filename)
            exit(0)

    @staticmethod
    def read_file(filename):
        file = open(filename, "r")
        values = file.read().splitlines()
        file.close()
        random.shuffle(values)
        return values

    @staticmethod
    def check_range(num, minr, maxr):
        if minr <= num <= maxr:
            return num
        else:
            print("[-] %d not between range %d and %d." % (num, maxr, minr))
            exit(0)

    def ssh_credentials(self):
        print("\nEnter SSH Credentials:")
        self.config["ssh_user"] = input("Username: ")
        self.config["ssh_pass"] = getpass.getpass("Password: ")
        port = input("Port [22]: ")
        self.config["ssh_port"] = int(port) if port else 22
        print()

    @staticmethod
    def sha2(text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def print_information(self):
        for e in self.config:
            if e == "ssh_pass":
                print("%s:\t%s" % (e, self.sha2(self.config[e])))
            elif e != "ips":
                print("%s:\t%s" % (e, str(self.config[e])))
        print()
