# (C) 2013, Stephan Buys, <stephan.buys@gmail.com>
#
# This file is based on noop.py which is a part of Ansible, and is
# a derivative work as per the GPL. All original conditions apply.
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import datetime
import time
import yaml
import glob

class CallbackModule(object):

    tmpfolder = "./tmp_xunit_out/"
    filename = "xunit.xml"
    current={}
    results={}
    init = False
    start = None

    fmt = '%Y-%m-%d %H:%M:%S'

    def delta(self,str):
        return 0
        (dt,fractions) = str.split('.')
        x = time.strptime(dt,'%H:%M:%S')
        since_last = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec)
        since_last_in_seconds = since_last.days * 24 * 60 * 60 + since_last.seconds
        return since_last_in_seconds

    def writeline(self,key,value):

        if type(value) == int:
            if value == 0.0:
                value = "0"
            else:
                value = str(value)

        value = value.strip('\n')
        value = value.strip('\r')

        file = self.current['file']
        file = open(file, 'ab+')

        file.write(key + ": ")
        if value.find(':')!=-1:
        #    file.write('"' + value + '"')
            pass
        else:
            file.write(value)
        file.write('\n')
        file.close()


    def __init__(self):
        pass

    def on_any(self, *args, **kwargs):

        if len(args) == 0:
            return

        if type(args[0]) != str:
            return
        
        if len(args) == 1:
            return


        if 'name' in self.current:


            self.current['host'] = args[0]

            details = args[1]

            if details:

                if 'invocation' in details:
                    module = details['invocation']

                    self.writeline('module_name',module['module_name'])
                    self.writeline('module_args', module['module_args'])
                    self.current['details'] = details



        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.writeline('host',host)
        if 'delta' in res:
	         self.writeline('run_time',self.delta(res['delta']))

        self.writeline('result','failed')
        if 'stdout' in res:
            self.writeline('stdout','"' + res['stdout'] + '"')

        if 'stderr' in res and res['stderr'] != "":
            self.writeline('stderr','"'+ res['stderr'] + '"')

        if 'failcount' in self.results:
            self.results['failcount'] = self.result['failcount'] + 1
        else:
            self.results['failcount'] = 1



    def runner_on_changed(self, host, res):
        self.writeline('host',host)
        self.writeline('run_time',self.delta(res['delta']))
        self.writeline('result','changed')


    def runner_on_ok(self, host, res):

        if 'delta' in res:
            self.writeline('run_time',self.delta(res['delta']))

        if 'invocation' in res:
            if res['invocation']['module_name'] == 'setup':
                return

        self.writeline('host',host)
        self.writeline("result","ok")
        pass

    def runner_on_error(self, host, msg):

        self.writeline('error_host',host)
        self.writeline('error_host',msg)
        pass

    def runner_on_skipped(self, host, item=None):
        pass

    def runner_on_unreachable(self, host, res):
        pass

    def runner_on_no_hosts(self):
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        pass

    def runner_on_async_ok(self, host, res, jid):
        pass

    def runner_on_async_failed(self, host, res, jid):
        pass

    def playbook_on_start(self):
        pass

    def playbook_on_notify(self, host, handler):
        pass

    def playbook_on_no_hosts_matched(self):
        pass

    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):

        if 'count' in self.results:
            self.results['count'] = self.results['count'] + 1
        else:
             self.results['count'] = 1

        file = os.path.join(self.tmpfolder,str(self.results['count']) + ".out")

        self.current = {}
        self.current['name'] = name
        self.current['file'] = file

        self.writeline('name',name)
        self.writeline('run_count',str(self.results['count']))


        pass

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
        pass

    def playbook_on_setup(self):
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        pass

    def playbook_on_not_import_for_host(self, host, missing_file):
        pass

    def playbook_on_play_start(self, pattern):
        if self.init == False:
            self.init_xunit()
            self.init = True


    def init_xunit(self):
        if not os.path.exists(self.tmpfolder):
            os.makedirs(self.tmpfolder)
        else:
            shutil.rmtree(self.tmpfolder)
            os.makedirs(self.tmpfolder)

        filename = "xunit_out.xml"
        output = open(filename, 'w')
        output.write('<?xml version="1.0"?>\n')
        output.write('<testsuites xmlns="http://check.sourceforge.net/ns">\n')
        d = datetime.datetime.now()
        datetimestring = d.strftime(self.fmt)
        output.write('<datetime>' + datetimestring +'</datetime>\n')
        self.start = d



    def playbook_on_stats(self, stats):

        filename = "xunit_out.xml"
        output = open(filename, 'ab+')

        indent = ""

        files = glob.glob(os.path.join(self.tmpfolder,'*.out'))

        failcount = 0
        testcount = 0
        testname = "ansible_testrunner"
        id = "1"
        results = []

        output.write('  <suite>\n')
        output.write('  <title>' + testname + '</title>\n')

        for filename in files:

            testcount = testcount + 1

            stream = file(filename, 'r')
            obj = yaml.load(stream)

            if 'run_time' in obj:
                runtime = obj['run_time']
            else:
                runtime = 0

            if runtime == 0:
                timestr = "0"
            else:
                timestr = str(runtime)

            errormessage=""
            message = "Not Available"

            if 'stderr' in obj:
                errormessage = obj['stderr']
            elif 'stdout' in obj:
                errormessage = obj['stdout']
            else:
                if 'module_args' in obj:
                    if obj['module_args'] == None:
                        errormessage = "Failed command but no arguments could be found"
                    else:
                        errormessage = "Failed on "  + obj['module_args']
                else:
                    errormessage = "no module args, fatal error must have occurred, check ansible syntax"



            if 'result' in obj:
                if obj['result'] == "failed":
                    result = "failure"
                    message = errormessage
                else:
                    result = "success"
                    message = "Passed"
            else:
                result = "failure"
                message = errormessage

            if message == None:
                message = "Not Available"

            results.append('    <test result="' + result + '">\n')
            results.append('      <path>.</path>\n')
            results.append('      <fn>unknown</fn>\n')
            results.append('      <id>' + obj['name'] +'</id>\n')
            results.append('      <iteration>0</iteration>\n')
            results.append('      <description>NULL</description>\n')
            results.append('      <message>'+message+'</message>\n')
            results.append('    </test>\n')

            stream.close()



        for line in results:
            output.write(line)

        output.write('  </suite>\n')
        d = datetime.datetime.now()

        since_last = self.start - d

        since_last_in_seconds = since_last.days * 24 * 60 * 60 + since_last.seconds
        if since_last_in_seconds == 0:
            durationstring = "0.0"
        else:
            durationstring = str(since_last_in_seconds)
            durationstring = durationstring + ".0"

        output.write('  <duration>'+durationstring + '</duration>\n')
        output.write('</testsuites>\n')
        output.close()


