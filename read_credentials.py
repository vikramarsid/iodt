from os.path import expanduser


class ReadBlockCredentials(object):

    home = expanduser("~")

    def username(self):
        uname = ""
        with open(self.home + '/.multichain/iodt-node01/multichain.conf') as f:
            for line in f:
                if "rpcuser" in line:
                    user = line.split("=")
                    uname = user[1]
        return uname


    def password(self):
        pword = ""
        with open(self.home + '/.multichain/iodt-node01/multichain.conf') as f:
            for line in f:
                if "rpcpassword" in line:
                    passd = line.split("=")
                    pword = passd[1]
        return pword


# if __name__ == '__main__':
#     print(read_credentials())
