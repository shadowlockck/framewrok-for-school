# Install PyMySQL as MySQLdb if mysqlclient is not available
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
