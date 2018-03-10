#!/usr/bin/env python3
'''
Copyright Daniel Jones 2018

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import os, json;

class Message:
    '''
    messages.append(Message(filepath));
    print(messages[x].filepath);
    '''
    msgcount = 0;
    channels = [];
    def __init__(self, fp, line):
        self.filepath = fp;
        self.line = line;
        Message.msgcount+=1;

    def parsechannel(self):
        # channel name is taken from file path
        self.channel = self.filepath.split("#")[1].split("_")[0];

    def parsedate(self):
        # date taken from file path
        self.date = self.filepath.rsplit("_", 1)[1].rsplit(".", 1)[0];

    def parseline(self):
        try:
            self.user = self.line.split("<", 1)[1].split(">", 1)[0];
        except:
            self.user = "ZNCLOG";
            self.line = "[99:99:99] <ZNCLOG> name change or join/part, disregard.\n";
        self.time = self.line.split(" <", 1)[0].replace("[", "").replace("]", "");
        self.message = self.line.split("> ", 1)[1];
        if self.message.endswith("\n"):
            self.message = self.message[:-1];

    def getstructuredmsg(self):
        self.data = {};
        self.data["date"] = self.date;
        self.data["time"] = self.time;
        self.data["channel"] = self.channel;
        self.data["user"] = self.user;
        self.data["message"] = self.message;
        return self.data;

    def parse(self):
        # get message time
       self.parseline();
       self.parsechannel();
       self.parsedate();

def getlines(logfile):
    with open(logfile, encoding="utf-8") as f:
        for line in f:
            messages.append(Message(logfile, line));

def getlogpaths():
    # loop through each .log file inside indir
    for file in os.listdir(indir):
        if (file.endswith(".log")):
                filepath = os.path.join(indir, file);
                logfiles.append(filepath);
                if (debug):
                    break;

if __name__ == "__main__":
    debug = 1;
    indir = "logs/parse";
    logfiles = [];
    messages = [];
    getlogpaths();
    tmpdata = [];
    # collect all lines
    for file in logfiles:
        getlines(file);
    # parse each line
    for x in range(len(messages)):
        messages[x].parse();
        tmpdata.append(messages[x].getstructuredmsg());
    jsondata = json.dumps(tmpdata);
    print(jsondata);

