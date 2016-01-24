#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import json
import jieba
import cn_report
import cn

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, model):
        self.model = model

    def get(self):
        word = self.get_argument("word", default=u'税收')
        n = self.get_argument("n", default=u'50')
        words = [w for w in jieba.cut(word.strip())]
        try:
            n = int(n)
        except ValueError, e:
            n = 50
        ret = self.model.most_similar(positive=words, topn=n)
        self.write(json.dumps(ret, ensure_ascii=False))
        self.set_header("Content-Type", "application/json; charset=utf-8")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler, dict(model=cn_report.build_model())),
        (r"/cn", MainHandler, dict(model=cn.build_model())),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(9888)
    tornado.ioloop.IOLoop.current().start()
