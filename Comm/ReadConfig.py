import configparser
from ApiTest.Comm.Filepath import Configlpath


class ReadConfig:

    def read_config(self, section):

        cf = configparser.ConfigParser()
        cf.read(Configlpath(), encoding='utf-8')

        value = cf.items(section)

        return value

    def get_key(self, section, option):
        cf = configparser.ConfigParser()
        cf.read(Configlpath(), encoding='utf-8')
        value = cf.get(section, option)
        return value

#
# if __name__ == '__main__':
#     res = ReadConfig().read_config('SENDER1')
#     print(dict(res))
#     se = ReadConfig().get_key('ADDRESSEE', 'add1')
#     print(se)
