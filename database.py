from typing import OrderedDict
from flask import g
import sqlite3

DB_FILEPATH = '.\data.db'


def connect_db():
    """connect_db - connects to a database and returns it """
    sql = sqlite3.connect(DB_FILEPATH)
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    """get_db - returns a database """
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def get_user(db, email):
    """get_user - returns a user with a given email"""
    return db.execute('select id, email, passwd from users where email = ?', [email])


def all_user_results(db, userId):
    """all_user_results - returns all results of a user
    with a given id from a database"""
    return db.execute('select idR, userId, result, resultDate from results where userId = ?', [userId])


def user_test_amount(db, userId):
    """user_test_amount - returns a number of taken tests
    by a user with a given id"""
    return len(all_user_results(db, userId).fetchall())


def all_results(db):
    """all_results- returns all results from a database"""
    return db.execute('select idR, result ,userId, resultDate from results')


def all_test_amount(db):
    """all_test_amount - returns a number of all taken tests"""
    return len(all_results(db).fetchall())


def select_result(x):
    """select_result - retrieves and returns result from a given row of a database"""
    return float(x['result'])


def user_best_result(db, userId):
    """user_best_result - returns the best result of a user with a given id"""
    if all_user_results(db, userId).fetchall():
        return min(map(select_result, all_user_results(db, userId).fetchall()))


def best_result(db):
    """best_result - returns the best result of all users"""
    if all_results(db).fetchall():
        return min(map(select_result, all_results(db).fetchall()))


def user_results_daily(db, userId):
    """user_results_daily - returns a tuple of a list of days
    and a list of average results"""
    if all_user_results(db, userId).fetchall():
        user_results = all_user_results(db, userId).fetchall()
        results_by_date = OrderedDict()
        daily_results = []
        days = []
        for result in user_results:
            if result['resultDate'] in results_by_date:
                results_by_date[result['resultDate']].append(
                    float(result['result']))
            else:
                results_by_date.update(
                    {result['resultDate']: [float(result['result'])]})
        for day, results in results_by_date.items():
            days.append(day)
            daily_results.append(sum(results) / len(results))
        return (days, daily_results)
