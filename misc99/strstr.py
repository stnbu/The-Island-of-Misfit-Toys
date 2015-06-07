


class BuildInfo(str):

    def __new__(cls, version, build_num=None, path=None):
        obj = super(BuildInfo, cls).__new__(cls, version)
        obj.build_num = build_num
        obj.path = path
        return obj


x = BuildInfo('xxx')

x.build_num = 'abcfesafdsa,'
print x.build_num
