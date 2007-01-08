# Copyright (c) 2006,2007 Mitch Garnaat http://garnaat.org/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from boto.s3.user import User
import StringIO

CannedACLStrings = ['private', 'public-read',
                    'public-read-write', 'authenticated-read']

class Policy:

    def __init__(self, parent=None):
        self.parent = parent
        self.acl = None

    def startElement(self, name, attrs, connection):
        if name == 'Owner':
            self.owner = User(self)
            return self.owner
        elif name == 'AccessControlList':
            self.acl = ACL(self)
            return self.acl
        else:
            return None

    def endElement(self, name, value, connection):
        if name == 'Owner':
            pass
        elif name == 'AccessControlList':
            pass
        else:
            setattr(self, name, value)

    def to_xml(self):
        s = '<AccessControlPolicy>'
        s += self.owner.to_xml()
        s += self.acl.to_xml()
        s += '</AccessControlPolicy>'
        return s

class ACL:

    def __init__(self, policy=None):
        self.policy = policy
        self.grants = []

    def add_grant(self, grant):
        self.grants.append(grant)

    def startElement(self, name, attrs, connection):
        if name == 'Grant':
            self.grants.append(Grant(self))
            return self.grants[-1]
        else:
            return None

    def endElement(self, name, value, connection):
        if name == 'Grant':
            pass
        else:
            setattr(self, name, value)

    def to_xml(self):
        s = '<AccessControlList>'
        for grant in self.grants:
            s += grant.to_xml()
        s += '</AccessControlList>'
        return s
        
class Grant:

    def __init__(self, acl=None, grantee=None):
        self.acl = acl
        self.grantee = grantee

    def startElement(self, name, attrs, connection):
        if name == 'Grantee':
            self.grantee = User(self)
            if attrs.has_key('xsi:type'):
                self.grantee.type = attrs['xsi:type']
            else:
                self.grantee.type = None
            return self.grantee
        else:
            return None

    def endElement(self, name, value, connection):
        if name == 'Grantee':
            pass
        elif name == 'Permission':
            self.permission = value
        else:
            setattr(self, name, value)

    def to_xml(self):
        s = '<Grant>'
        s += self.grantee.to_xml('Grantee')
        s += '<Permission>%s</Permission>' % self.permission
        s += '</Grant>'
        return s
        
            