#!/usr/bin/python3

# jt  change to  keeping connections within functions not attempting to share
# 2021/01/27 jont@ninelocks.com
# based on druhams code but with some hacky bits done to it.
# I open t/close the db in each call as I was having odd problems of missing results
# exclusively use ip number as that worked out on a local network with local names
# without doing that I eneded up with clients banning an ip twice. once when they banned it themeslevs and again
# when pulled back from db as hostname /ip didnt resolve so the qery dmeant client didnt exclude itself.
# added a few lines that can be uncommented when debugging things


import socket
import datetime
from flask import Flask
from flask import jsonify
from flask import request
from flask import escape
from flask_caching import Cache
import mysql.connector


# pip install dnspython
import dns.resolver
import dns.reversename
import dns.exception


import api_cfg as cfg

app = Flask(__name__)
app.url_map.strict_slashes = False
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


#db = mysql.connector.connect(host=cfg.mysql["host"], user=cfg.mysql["user"], passwd=cfg.mysql["passwd"], db=cfg.mysql["db"])


#cur = db.cursor(dictionary=True)

#jts dns lookup alternative, admittedly odd return values but this is more for debuggin things
def lookup(ip):
    try:
        rev_name = dns.reversename.from_address(ip)

        n = str(dns.resolver.query(rev_name, "PTR")[0])
        return n
        # result = self.query(rev_name,"PTR").__iter__().next().to_text()[:-1]

    except dns.resolver.NXDOMAIN:
        return ip  # happy to just have ip
    except dns.exception.Timeout:
        return "%s: jTIMEOUT\n" % (ip)
    except dns.resolver.YXDOMAIN:
        return "%s: YXDOMAIN\n" % (ip)
    except dns.resolver.NoNameservers:
        # return "%s: NoNameservers\n" % (ip)
        return ip  # or maybe we should say nothing or had an error
    except:
        return "%s: UNSPECIFIED ERROR\n" % (ip)


@app.route('/', methods=['GET'])
@app.route('/api', methods=['GET'])
@app.route('/api/', methods=['GET'])
@cache.cached(timeout=3600)
def about():
    return '<h3>Shared Fail2Ban API</h3><br/><strong>Paul Clark, Adam Boutcher</strong><br/>(<em>UKI-SCOTGRID-DURHAM</em>) IPPP, Durham University.<br/><br/><a href="https://github.com/bulgemonkey/Shared-Fail2Ban">https://github.com/bulgemonkey/Shared-Fail2Ban</a>'


@app.route('/api/v1', methods=['GET'])
@app.route('/api/v1/', methods=['GET'])
@cache.cached(timeout=3600)
def help():
    return '/api - About<br/>/api/v1 - Help<br/>/api/v1/time/[str:jailname]/[int:hour]/[all] - Banned IPs by time (last n hours)<br/>/api/v1/count/[str:jailname]/[int:count]/[all] - Banned IPs by count (n bans)<br/>args: domain=domain_filter, time=time_filter_in_hours'


# These are IPs that have been bad for a short ban
@app.route('/api/v1/time', methods=['GET'])
@app.route('/api/v1/time/', methods=['GET'])
@app.route('/api/v1/time/<string:jail>', methods=['GET'])
@app.route('/api/v1/time/<string:jail>/', methods=['GET'])
@app.route('/api/v1/time/<string:jail>/<int:time>', methods=['GET'])
@app.route('/api/v1/time/<string:jail>/<int:time>/', methods=['GET'])
@app.route('/api/v1/time/<string:jail>/<int:time>/<string:host>', methods=['GET'])
@app.route('/api/v1/time/<string:jail>/<int:time>/<string:host>/', methods=['GET'])
@cache.cached(timeout=5)
def gettime(jail="ssh", time=1, host="remote"):

    #cur = mysql.connection.cursor(dictionary=True)
    db = mysql.connector.connect(
        host=cfg.mysql["host"], user=cfg.mysql["user"], passwd=cfg.mysql["passwd"], db=cfg.mysql["db"])
    cur = db.cursor(dictionary=True)

    if host == "remote":
        #try:
        #host = socket.gethostbyaddr(request.remote_addr)[0]
        host = lookup(request.remote_addr)
       # except socket.herror:
        #    host = "unknown.host"
    else:
        host = "*"

    host = request.remote_addr  # jon hack as I only cae about ip numbers

    filter = ""
    if 'domain' in request.args:
        filter = filter+" AND hostname like '%%%s'" % (
            escape(request.args.get('domain', default=None, type=str)))

    jail = jail.lower()

    #may need to see how this works in live network with proper names
    if filter:
        sql = "SELECT UNIX_TIMESTAMP(created) as created, ip, port, protocol FROM f2b WHERE created>=DATE_ADD(NOW(), INTERVAL -%s HOUR) AND jail = '%s' AND hostname != '%s' %s" % (
            int(time), escape(jail), escape(host), filter)
    else:
        sql = "SELECT UNIX_TIMESTAMP(created) as created, ip, port, protocol FROM f2b WHERE created>=DATE_ADD(NOW(), INTERVAL -%s HOUR) AND jail = '%s' AND hostname != '%s'" % (
            int(time), escape(jail), escape(host))
    cur.execute(sql)
    row = cur.fetchall()
    # was bug here where it was cur referenced not cur 2
    print(" ", cur.rowcount, " records read")
    print("sql was ", sql)
    cur.close()
    db.close()
    return jsonify(row)

# These are IPs that are repeatedly bad
@app.route('/api/v1/count', methods=['GET'])
@app.route('/api/v1/count/', methods=['GET'])
@app.route('/api/v1/count/<string:jail>', methods=['GET'])
@app.route('/api/v1/count/<string:jail>/', methods=['GET'])
@app.route('/api/v1/count/<string:jail>/<int:count>', methods=['GET'])
@app.route('/api/v1/count/<string:jail>/<int:count>/', methods=['GET'])
@app.route('/api/v1/count/<string:jail>/<int:count>/<string:host>', methods=['GET'])
@app.route('/api/v1/count/<string:jail>/<int:count>/<string:host>/', methods=['GET'])
@cache.cached(timeout=5)
def getcount(jail="all", count=1000, host="remote"):
    #cur = mysql.connection.cursor(dictionary=True)
    db = mysql.connector.connect(
        host=cfg.mysql["host"], user=cfg.mysql["user"], passwd=cfg.mysql["passwd"], db=cfg.mysql["db"])
    cur = db.cursor(dictionary=True)

    #if host == "remote":
        #try:
        #host = socket.gethostbyaddr(request.remote_addr)[0]
        #host = lookup(request.remote_addr) #jons altrernat lookup
        #except socket.herror:
        #    host = "unknown.host"
    #else:
    #    host = "*"

    host = request.remote_addr  # jon hack as I only cae about ip numbers

    filter = ""
    if 'domain' in request.args:
        filter = filter+" AND hostname like '%%%s'" % (
            escape(request.args.get('domain', default=None, type=str)))
    if 'time' in request.args:
        filter = filter+" AND created>=DATE_ADD(NOW(), INTERVAL -%d HOUR)" % (
            request.args.get('time', default=None, type=int))

    jail = jail.lower()
    if jail == "all":
        jailsql = ""
    else:
        jailsql = "jail = '%s' AND" % (escape(jail))

    if filter:
        sql = "SELECT COUNT(*) as count, ip, port, protocol FROM f2b WHERE %s hostname != '%s' %s GROUP BY ip HAVING count >= %d ORDER BY count DESC" % (
            jailsql, escape(host), filter, int(count))
    else:
        sql = "SELECT COUNT(*) as count, ip, port, protocol FROM f2b WHERE %s hostname != '%s' GROUP BY ip HAVING count >= %d ORDER BY count DESC" % (
            jailsql, escape(host), int(count))
    cur.execute(sql)
    row = cur.fetchall()
    # was bug here where it was cur referenced not cur 2
    print("JT ", cur.rowcount, " records read")
    cur.close()
    db.close()
    return jsonify(row)

# A method to write back into the database
@app.route('/api/v1/put', methods=['PUT'])
def put():
    rowcount = 0  # jt added to simplify close later
    db = mysql.connector.connect(
        host=cfg.mysql["host"], user=cfg.mysql["user"], passwd=cfg.mysql["passwd"], db=cfg.mysql["db"])
    cur2 = db.cursor(dictionary=True)
    #cur2 = mysql.connection.cursor(cursorclass=DictCursor)
    if 'X-TOKEN' in request.headers:
        tokensql = "SELECT COUNT(*) as count FROM f2b_api WHERE `key` = '%s'" % (
            request.headers.get('X-TOKEN', default=None, type=str))
        cur2.execute(tokensql)
        row = cur2.fetchall()
        if int(row[0]['count']) >= 1:

            if 'date' not in request.json:
                return "Incomplete request - date"
            else:
                pdate = request.json['date']
            if 'jail' not in request.json:
                return "Incomplete request - jail"
            else:
                pjail = request.json['jail']
                pjail = pjail.lower()
            if 'proto' not in request.json:
                return "Incomplete request - proto"
            else:
                pproto = request.json['proto']
            if 'port' not in request.json:
                return "Incomplete request - port"
            else:
                pport = request.json['port']
            if 'ip' not in request.json:
                return "Incomplete request - ip"
            else:
                pip = request.json['ip']
            # Optional

            """if 'hostname' not in request.json:
                #try:
                    #phost = socket.gethostbyaddr(request.remote_addr)[0]
                print("hostname not in request")    
                phost = lookup(request.remote_addr)
                #except socket.herror:
                #    return "Unable to determine your hostname, please include it in the request"
            else:
                phost = request.json['hostname']

            """
            phost = lookup(
                request.remote_addr)  # or I may just use ip and forget hostnames altogether
            if 'bantime' not in request.json:
                pbantime = "900"
            else:
                pbantime = request.json['bantime']

            sql = "INSERT INTO f2b SET hostname = '%s', created = '%s', jail = '%s', protocol = '%s', port = '%s', ip = '%s', bantime = '%d'" % (
                escape(phost), escape(pdate), escape(pjail), escape(pproto), escape(pport), escape(pip), int(pbantime))
            cur2.execute(sql)
            db.commit()
       	    # print("PUT - SQL: ", sql, " from ", request.remote_addr)
            # was bug here where it was cur referenced not cur 2
            print("PUT - ", cur2.rowcount, " records inserted.")
            rowcount = cur2.rowcount
            cur2.close()
            db.close()
       	    if rowcount > 0:
                return "OK"
       	    else:
                return "FAILED"
        else:
            return "Please PUT request with your TOKEN."
    else:
        return "Please PUT request with your TOKEN."


if __name__ == "__main__":
    app.run()
    #from waitress import serve
    #app.run(host='0.0.0.0', port=3744,debug=True);
    #serve(app, host='0.0.0.0', port=80)
