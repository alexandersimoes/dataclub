# Helper for tracking actions, attribute views and page views
from dataviva import db
from dataviva.account.models import Action, PageView, AttrView
from dataviva.utils import make_query

def add_action(uid, key, value=None):
    action = Action(user_id=uid, key=key, value=value)
    db.session.add(action)
    db.session.commit()

def add_attrview(uid, attr, value):
    res = db.session.query(AttrView).filter(AttrView.user_id == uid, AttrView.attr==attr, AttrView.value==value).first()
    if not res:
        attrview = AttrView(user_id=uid, attr=attr, value=value, count=1)
        db.session.add(attrview)
    else:
        res.count += 1
        db.session.add(res)
    db.session.commit()

def add_pageview(uid, page):
    res = db.session.query(PageView).filter(PageView.user_id == uid, PageView.page==page).first()
    if not res:
        pageview = PageView(user_id=uid, page=page, count=1)
        db.session.add(pageview)
    else:
        res.count += 1
        db.session.add(res)
    db.session.commit()

def get_recent(uid, limit=20, offset=None):
    attr_data = make_query.query_table(AttrView, columns=[AttrView.attr, AttrView.value, AttrView.count, AttrView.timestamp], limit=limit, order=AttrView.timestamp, offset=offset)
    page_data = make_query.query_table(PageView, columns=[PageView.page, PageView.count, AttrView.timestamp], limit=limit, order=AttrView.timestamp, offset=offset)

    return {"attrs": attr_data, "pages" : page_data}