import sqlite3

class DB:

    cursor = None
    def __init__(self):
        self.__conn = sqlite3.connect('../maps.db')
        self.__conn.row_factory = sqlite3.Row
        DB.cursor = self.__conn.cursor()

    def __del__(self):
        self.__conn.close()


class Scores:

    @staticmethod
    def get_scores():
        DB.cursor.execute("SELECT * FROM scores")
        return DB.cursor.fetchall()

    @staticmethod
    def get_score_from_chart(score, chart):
        score_par = (score, chart)
        DB.cursor.execute("SELECT * FROM scores WHERE score == (?) AND chart_hash == (?)", score_par)
        return DB.cursor.fetchone()

    @staticmethod
    def get_clear_scores():
        DB.cursor.execute("SELECT * FROM scores WHERE gauge >= 0.7 AND gameflags == 0")
        return DB.cursor.fetchall()

    @staticmethod
    def get_excessive_clear_scores():
        DB.cursor.execute("SELECT * FROM scores WHERE gauge > 0 AND gameflags == 1")
        return DB.cursor.fetchall()

    @staticmethod
    def get_puc_scores():
        DB.cursor.execute("SELECT * FROM scores WHERE miss == 0 AND score == 10000000")
        return DB.cursor.fetchall()

    @staticmethod
    def get_uc_scores():
        DB.cursor.execute("SELECT * FROM scores WHERE miss == 0 AND score < 10000000")
        return DB.cursor.fetchall()

    @staticmethod
    def get_failed_scores():
        DB.cursor.execute("SELECT * FROM scores WHERE gauge == 0 AND gameflags == 1 OR gauge < 0.7 AND gameflags == 0")
        return DB.cursor.fetchall()

    @staticmethod
    def get_top_score_of_chart_by_level(level):
        # get top clear score of each chart (both clear and exc clear) by level
        DB.cursor.execute("SELECT artist, title, level, MAX(score) as score, gauge, gameflags, miss FROM charts LEFT JOIN scores ON hash == chart_hash AND (gauge >= 0.7 AND gameflags == 0 OR gauge > 0 AND gameflags == 1) WHERE level == (?) AND path LIKE '%SDVX%' GROUP BY hash ORDER BY folderid", (level,))
        return DB.cursor.fetchall()


class Charts:

    @staticmethod
    def get_charts():
        DB.cursor.execute("SELECT * FROM charts")
        return DB.cursor.fetchall()

    @staticmethod
    def get_chart_by_hash(hash):
        saved_hash = (hash,)
        DB.cursor.execute("SELECT * FROM charts WHERE hash == (?)", saved_hash)
        return DB.cursor.fetchone()

    @staticmethod
    def get_charts_by_short_diff(difficulty):
        saved_difficulty = (difficulty,)
        DB.cursor.execute("SELECT * FROM charts WHERE diff_shortname == (?)", saved_difficulty)
        return DB.cursor.fetchall()

    @staticmethod
    def get_charts_by_level(level):
        level = (level,)
        DB.cursor.execute("SELECT * FROM charts WHERE level == (?)", level)
        return DB.cursor.fetchall()

    @staticmethod
    def get_charts_by_artist(artist):
        DB.cursor.execute("SELECT * FROM charts WHERE artist LIKE (?)", ('%' + artist + '%',))
        return DB.cursor.fetchall()
