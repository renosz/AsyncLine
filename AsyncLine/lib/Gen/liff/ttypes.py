#
# Autogenerated by Frugal Compiler (3.4.3)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from frugal.util import make_hashable
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol


class LiffErrorCode(int):
    INVALID_REQUEST = 1
    UNAUTHORIZED = 2
    CONSENT_REQUIRED = 3
    VERSION_UPDATE_REQUIRED = 4
    SERVER_ERROR = 100

    _VALUES_TO_NAMES = {
        1: "INVALID_REQUEST",
        2: "UNAUTHORIZED",
        3: "CONSENT_REQUIRED",
        4: "VERSION_UPDATE_REQUIRED",
        100: "SERVER_ERROR",
    }

    _NAMES_TO_VALUES = {
        "INVALID_REQUEST": 1,
        "UNAUTHORIZED": 2,
        "CONSENT_REQUIRED": 3,
        "VERSION_UPDATE_REQUIRED": 4,
        "SERVER_ERROR": 100,
    }

class LiffFeatureType(int):
    GEOLOCATION = 1
    ADVERTISING_ID = 2
    BLUETOOTH_LE = 3

    _VALUES_TO_NAMES = {
        1: "GEOLOCATION",
        2: "ADVERTISING_ID",
        3: "BLUETOOTH_LE",
    }

    _NAMES_TO_VALUES = {
        "GEOLOCATION": 1,
        "ADVERTISING_ID": 2,
        "BLUETOOTH_LE": 3,
    }

class LiffChatContext(object):
    """
    Attributes:
     - chatMid
    """
    def __init__(self, chatMid=None):
        self.chatMid = chatMid

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.chatMid = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('LiffChatContext')
        if self.chatMid is not None:
            oprot.writeFieldBegin('chatMid', TType.STRING, 1)
            oprot.writeString(self.chatMid)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.chatMid))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class LiffContext(object):
    """
    Attributes:
     - none
     - chat
     - squareChat
    """
    def __init__(self, none=None, chat=None, squareChat=None):
        self.none = none
        self.chat = chat
        self.squareChat = squareChat

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.none = LiffNoneContext()
                    self.none.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.chat = LiffChatContext()
                    self.chat.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRUCT:
                    self.squareChat = LiffSquareChatContext()
                    self.squareChat.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('LiffContext')
        if self.none is not None:
            oprot.writeFieldBegin('none', TType.STRUCT, 1)
            self.none.write(oprot)
            oprot.writeFieldEnd()
        if self.chat is not None:
            oprot.writeFieldBegin('chat', TType.STRUCT, 2)
            self.chat.write(oprot)
            oprot.writeFieldEnd()
        if self.squareChat is not None:
            oprot.writeFieldBegin('squareChat', TType.STRUCT, 3)
            self.squareChat.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.none))
        value = (value * 31) ^ hash(make_hashable(self.chat))
        value = (value * 31) ^ hash(make_hashable(self.squareChat))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class LiffErrorConsentRequired(object):
    """
    Attributes:
     - channelId
     - consentUrl
    """
    def __init__(self, channelId=None, consentUrl=None):
        self.channelId = channelId
        self.consentUrl = consentUrl

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.channelId = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.consentUrl = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('LiffErrorConsentRequired')
        if self.channelId is not None:
            oprot.writeFieldBegin('channelId', TType.STRING, 1)
            oprot.writeString(self.channelId)
            oprot.writeFieldEnd()
        if self.consentUrl is not None:
            oprot.writeFieldBegin('consentUrl', TType.STRING, 2)
            oprot.writeString(self.consentUrl)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.channelId))
        value = (value * 31) ^ hash(make_hashable(self.consentUrl))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class LiffErrorPayload(object):
    """
    Attributes:
     - consentRequired
    """
    def __init__(self, consentRequired=None):
        self.consentRequired = consentRequired

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 3:
                if ftype == TType.STRUCT:
                    self.consentRequired = LiffErrorConsentRequired()
                    self.consentRequired.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('LiffErrorPayload')
        if self.consentRequired is not None:
            oprot.writeFieldBegin('consentRequired', TType.STRUCT, 3)
            self.consentRequired.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.consentRequired))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class LiffNoneContext(object):
    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('LiffNoneContext')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class LiffSquareChatContext(object):
    """
    Attributes:
     - squareChatMid
    """
    def __init__(self, squareChatMid=None):
        self.squareChatMid = squareChatMid

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.squareChatMid = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('LiffSquareChatContext')
        if self.squareChatMid is not None:
            oprot.writeFieldBegin('squareChatMid', TType.STRING, 1)
            oprot.writeString(self.squareChatMid)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.squareChatMid))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class LiffView(object):
    """
    Attributes:
     - type
     - url
     - trustedDomain
     - titleIconUrl
     - titleTextColor
     - titleSubtextColor
     - titleButtonColor
     - titleBackgroundColor
     - progressBarColor
     - progressBackgroundColor
    """
    def __init__(self, type=None, url=None, trustedDomain=None, titleIconUrl=None, titleTextColor=None, titleSubtextColor=None, titleButtonColor=None, titleBackgroundColor=None, progressBarColor=None, progressBackgroundColor=None):
        self.type = type
        self.url = url
        self.trustedDomain = trustedDomain
        self.titleIconUrl = titleIconUrl
        self.titleTextColor = titleTextColor
        self.titleSubtextColor = titleSubtextColor
        self.titleButtonColor = titleButtonColor
        self.titleBackgroundColor = titleBackgroundColor
        self.progressBarColor = progressBarColor
        self.progressBackgroundColor = progressBackgroundColor

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.type = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.url = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 11:
                if ftype == TType.BOOL:
                    self.trustedDomain = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.STRING:
                    self.titleIconUrl = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I32:
                    self.titleTextColor = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.I32:
                    self.titleSubtextColor = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 8:
                if ftype == TType.I32:
                    self.titleButtonColor = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I32:
                    self.titleBackgroundColor = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 9:
                if ftype == TType.I32:
                    self.progressBarColor = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 10:
                if ftype == TType.I32:
                    self.progressBackgroundColor = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('LiffView')
        if self.type is not None:
            oprot.writeFieldBegin('type', TType.STRING, 1)
            oprot.writeString(self.type)
            oprot.writeFieldEnd()
        if self.url is not None:
            oprot.writeFieldBegin('url', TType.STRING, 2)
            oprot.writeString(self.url)
            oprot.writeFieldEnd()
        if self.trustedDomain is not None:
            oprot.writeFieldBegin('trustedDomain', TType.BOOL, 11)
            oprot.writeBool(self.trustedDomain)
            oprot.writeFieldEnd()
        if self.titleIconUrl is not None:
            oprot.writeFieldBegin('titleIconUrl', TType.STRING, 6)
            oprot.writeString(self.titleIconUrl)
            oprot.writeFieldEnd()
        if self.titleTextColor is not None:
            oprot.writeFieldBegin('titleTextColor', TType.I32, 4)
            oprot.writeI32(self.titleTextColor)
            oprot.writeFieldEnd()
        if self.titleSubtextColor is not None:
            oprot.writeFieldBegin('titleSubtextColor', TType.I32, 7)
            oprot.writeI32(self.titleSubtextColor)
            oprot.writeFieldEnd()
        if self.titleButtonColor is not None:
            oprot.writeFieldBegin('titleButtonColor', TType.I32, 8)
            oprot.writeI32(self.titleButtonColor)
            oprot.writeFieldEnd()
        if self.titleBackgroundColor is not None:
            oprot.writeFieldBegin('titleBackgroundColor', TType.I32, 5)
            oprot.writeI32(self.titleBackgroundColor)
            oprot.writeFieldEnd()
        if self.progressBarColor is not None:
            oprot.writeFieldBegin('progressBarColor', TType.I32, 9)
            oprot.writeI32(self.progressBarColor)
            oprot.writeFieldEnd()
        if self.progressBackgroundColor is not None:
            oprot.writeFieldBegin('progressBackgroundColor', TType.I32, 10)
            oprot.writeI32(self.progressBackgroundColor)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.type))
        value = (value * 31) ^ hash(make_hashable(self.url))
        value = (value * 31) ^ hash(make_hashable(self.trustedDomain))
        value = (value * 31) ^ hash(make_hashable(self.titleIconUrl))
        value = (value * 31) ^ hash(make_hashable(self.titleTextColor))
        value = (value * 31) ^ hash(make_hashable(self.titleSubtextColor))
        value = (value * 31) ^ hash(make_hashable(self.titleButtonColor))
        value = (value * 31) ^ hash(make_hashable(self.titleBackgroundColor))
        value = (value * 31) ^ hash(make_hashable(self.progressBarColor))
        value = (value * 31) ^ hash(make_hashable(self.progressBackgroundColor))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class LiffViewRequest(object):
    """
    Attributes:
     - liffId
     - context
    """
    def __init__(self, liffId=None, context=None):
        self.liffId = liffId
        self.context = context

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.liffId = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.context = LiffContext()
                    self.context.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('LiffViewRequest')
        if self.liffId is not None:
            oprot.writeFieldBegin('liffId', TType.STRING, 1)
            oprot.writeString(self.liffId)
            oprot.writeFieldEnd()
        if self.context is not None:
            oprot.writeFieldBegin('context', TType.STRUCT, 2)
            self.context.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.liffId))
        value = (value * 31) ^ hash(make_hashable(self.context))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class LiffViewResponse(object):
    """
    Attributes:
     - view
     - contextToken
     - accessToken
     - featureToken
     - features
     - channelId
    """
    def __init__(self, view=None, contextToken=None, accessToken=None, featureToken=None, features=None, channelId=None):
        self.view = view
        self.contextToken = contextToken
        self.accessToken = accessToken
        self.featureToken = featureToken
        self.features = features
        self.channelId = channelId

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.view = LiffView()
                    self.view.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.contextToken = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.accessToken = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.featureToken = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.LIST:
                    self.features = []
                    (_, elem0) = iprot.readListBegin()
                    for _ in range(elem0):
                        elem1 = LiffFeatureType(iprot.readI32())
                        self.features.append(elem1)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.STRING:
                    self.channelId = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('LiffViewResponse')
        if self.view is not None:
            oprot.writeFieldBegin('view', TType.STRUCT, 1)
            self.view.write(oprot)
            oprot.writeFieldEnd()
        if self.contextToken is not None:
            oprot.writeFieldBegin('contextToken', TType.STRING, 2)
            oprot.writeString(self.contextToken)
            oprot.writeFieldEnd()
        if self.accessToken is not None:
            oprot.writeFieldBegin('accessToken', TType.STRING, 3)
            oprot.writeString(self.accessToken)
            oprot.writeFieldEnd()
        if self.featureToken is not None:
            oprot.writeFieldBegin('featureToken', TType.STRING, 4)
            oprot.writeString(self.featureToken)
            oprot.writeFieldEnd()
        if self.features is not None:
            oprot.writeFieldBegin('features', TType.LIST, 5)
            oprot.writeListBegin(TType.I32, len(self.features))
            for elem2 in self.features:
                oprot.writeI32(elem2)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.channelId is not None:
            oprot.writeFieldBegin('channelId', TType.STRING, 6)
            oprot.writeString(self.channelId)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.view))
        value = (value * 31) ^ hash(make_hashable(self.contextToken))
        value = (value * 31) ^ hash(make_hashable(self.accessToken))
        value = (value * 31) ^ hash(make_hashable(self.featureToken))
        value = (value * 31) ^ hash(make_hashable(self.features))
        value = (value * 31) ^ hash(make_hashable(self.channelId))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class RevokeTokenRequest(object):
    """
    Attributes:
     - accessToken
    """
    def __init__(self, accessToken=None):
        self.accessToken = accessToken

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.accessToken = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('RevokeTokenRequest')
        if self.accessToken is not None:
            oprot.writeFieldBegin('accessToken', TType.STRING, 1)
            oprot.writeString(self.accessToken)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.accessToken))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class LiffException(TException):
    """
    Attributes:
     - code
     - message
     - payload
    """
    def __init__(self, code=None, message=None, payload=None):
        self.code = code
        self.message = message
        self.payload = payload

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.code = LiffErrorCode(iprot.readI32())
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.message = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRUCT:
                    self.payload = LiffErrorPayload()
                    self.payload.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('LiffException')
        if self.code is not None:
            oprot.writeFieldBegin('code', TType.I32, 1)
            oprot.writeI32(self.code)
            oprot.writeFieldEnd()
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 2)
            oprot.writeString(self.message)
            oprot.writeFieldEnd()
        if self.payload is not None:
            oprot.writeFieldBegin('payload', TType.STRUCT, 3)
            self.payload.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.code))
        value = (value * 31) ^ hash(make_hashable(self.message))
        value = (value * 31) ^ hash(make_hashable(self.payload))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
