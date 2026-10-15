# Install PyMySQL as MySQLdb if mysqlclient is not available
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Python 3.14+ compatibility patch for Django BaseContext.__copy__
try:
    import sys
    if sys.version_info >= (3, 14):
        import django.template.context as _ctx
        def _safe_basecontext_copy(self):
            obj = self.__class__.__new__(self.__class__)
            obj.__dict__.update(self.__dict__)
            obj.dicts = self.dicts[:]
            return obj
        _ctx.BaseContext.__copy__ = _safe_basecontext_copy
except Exception:
    pass

