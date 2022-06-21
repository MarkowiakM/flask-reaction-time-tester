from typing import OrderedDict
from flask import g
import sqlite3
import datetime


def connect_db():
    sql = sqlite3.connect('.\data.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def get_user(db, email):
    return db.execute('select id, email, passwd from users where email = ?', [email])


def all_user_results(db, userId):
    return db.execute('select idR, userId, result, resultDate from results where userId = ?', [userId])


def user_test_amount(db, userId):
    return len(all_user_results(db, userId).fetchall())


def all_results(db):
    return db.execute('select idR, result ,userId, resultDate from results')


def all_test_amount(db):
    return len(all_results(db).fetchall())


def select_result(x):
    return float(x['result'])


def user_best_result(db, userId):
    if all_user_results(db, userId).fetchall():
        return min(map(select_result, all_user_results(db, userId).fetchall()))


def best_result(db):
    if all_results(db).fetchall():
        return min(map(select_result, all_results(db).fetchall()))


def user_results_daily(db, userId):
    if all_user_results(db, userId).fetchall():
        user_results = all_user_results(db, userId).fetchall()

        results_by_date = OrderedDict()
        daily_results = []
        days = set()
        for result in user_results:
            if result['resultDate'] in results_by_date:
                results_by_date[result['resultDate']].append(
                    float(result['result']))
            else:
                results_by_date.update(
                    {result['resultDate']: [float(result['result'])]})
        for day, results in results_by_date.items():
            days.add(day)
            daily_results.append(sum(results) / len(results))
        return (list(days), daily_results)
