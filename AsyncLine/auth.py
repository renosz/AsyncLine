# -*- coding: utf-8 -*-
import os, sys
import hmac
import time
import base64
import asyncio
import hashlib
import rsa
import requests
from . import config
from . import models
from . import log
from .models import SyncAsync
from .connections import Connection
from .lib.Gen.ttypes import *

logs = log.LOGGER

class Auth(Connection):
	def __init__(self, client_name, storage):
		super().__init__(config.MAIN_PATH)
		self.LA, self.UA = models.ApplicationHeader(client_name).get()
		self.updateHeaders({
			'User-Agent': self.UA,
			'X-Line-Application': self.LA,
			'X-Line-Carrier': config.CARRIER,
			"x-lal":"in_ID"
		})
		self.token_db = storage
		self.afterLoginRemote = []

	def remote(self, func):
		self.afterLoginRemote.append(func)
	#crypto
	def __write_val(self, data):
		return (chr(len(data)) + data)

	def __gen_message(self, tuple_msg):
		return (''.join(tuple_msg)).encode('utf-8')

	def __rsa_crypt(self, message,RSA):
		pub_key = rsa.PublicKey(int(RSA.nvalue, 16), int(RSA.evalue, 16))
		crypto  = rsa.encrypt(message, pub_key)
		return crypto

	def _encryptedEmailAndPassword(self, mail, passwd, RSA):
		message_ = (
			self.__write_val(RSA.sessionKey),
			self.__write_val(mail),
			self.__write_val(passwd),
		)
		message = self.__gen_message(message_)
		crypto  = self.__rsa_crypt(message, RSA).hex()
		return crypto

	def _encryptedPassword(self, phone, password, RSA):
		message_ = (
			self.__write_val(RSA.sessionKey),
			self.__write_val(phone),
			self.__write_val(passwd),
		)
		message = self.__gen_message(message_)
		crypto  = self.__rsa_crypt(message, RSA).hex()
		return crypto

	def waitForPhoneConfirm(self, verifier):
		r = requests.get(config.BASE_URL + config.WAIT_FOR_MOBILE_PATH, headers={
			'X-Line-Access': verifier
		})
		return r
	
	def checkmail(self, mail):
		if mail.endswith(".session"):
			if os.path.exists(mail):
				return True
	
	def _validate_col(self, *val):
		r = self.token_db.auth_col.find_one(*val)
		if r:
			return True
		else:
			return False
		
	async def createLoginCmd(self, name):
		choses = ["qr", "email", "token"]
		if not self._validate_col({'name': name}):
			logs.warning("Cannot find last session, trying to create")
			c = input("Choose what you want to login (qr | email | token): ")
			while True:
				if c not in choses:
					logs.warning("Wrong input %s please input qr or email" % c)
					return False
					break
				elif c == "token":
					token = input("Input your token: ")
					await self.loginWithAuthToken(token.strip())
				elif c == "qr":
					await self.loginWithQrcode(name)
				elif c == "email":
					mail = input("Input your email: ")
					password = input("Input your password: ")
					self.token_db.auth_col.insert_one({
						'name': name,
						'mail': mail,
						'passwd': password
					})
					await self.loginWithCredential(mail=mail, name=name, password=password)
				break
		else:
			k = self.token_db.auth_col.find({'name': name})
			for i in k:
				if 'cert' in i.keys():
					await self.loginWithCredential(mail=i['mail'],
								name=i['name'],
								password=i['passwd'],
								cert=i['cert'])
				elif 'token' in i.keys():
					await self.loginWithAuthToken(i['token'])
			
	async def createLoginSession(self, name, token, mail, passwd, certt, qr):
		if token is not None:
			await self.loginWithAuthToken(token)
		elif mail and passwd is not None:
			if self.token_db is not None:
				_name = name if name else mail
				if self._validate_col({'name': _name, 'mail': mail}):
					c = self.token_db.auth_col.find_one({'name': _name, 'mail': mail})
					await self.loginWithCredential(mail=mail, password=passwd, cert=c['cert'])
				else:
					await self.loginWithCredential(mail=mail, password=passwd, name=_name)
			else:
				pname = name if name else mail +".session"
				if self.checkmail(pname):
					y = open(pname, "r").read().strip()
					await self.loginWithCredential(mail=mail, password=passwd, cert=y)
				else:
					await self.loginWithCredential(mail=mail, password=passwd,
											path = pname)
		elif mail and passwd and cert is not None:
			await self.loginWithCredential(mail=mail, password=passwd, cert=certt)
		elif qr and name is not None:
			if self.token_db is not None:
				if self._validate_col({'name': name}):
					token = self.token_db.auth_col.find_one({'name': name})
					await self.loginWithAuthToken(token['token'])
				else:
					await self.loginWithQrcode(name)
			elif not self.token_db and name is not None and os.path.exists(name+'.session'):
				token = open(name+'.session', "r").read()
				await self.loginWithAuthToken(token.split(">")[1])
			else:
				await self.loginWithQrcode(path=name+".session" if name else None)
		elif name is not None and token or mail is None:
			if self.token_db is not None:
				await self.createLoginCmd(name)
			else:
				path = name + ".session"
				choses = ["qr", "email", "token"]
				if not os.path.exists(path):
					logs.warning("Cannot find last session, trying to create")
					await asyncio.sleep(1)
					c = input("Choose what you want to login (qr | email | token): ")
					while True:
						if c not in choses:
							logs.warning("Wrong input %s please input qr or email" % c)
							return False
							break
						elif c == "token":
							token = input("Input your token: ")
							await self.loginWithAuthToken(token.strip(), path)
						elif c == "qr":
							await self.loginWithQrcode(path)
						elif c == "email":
							mail = input("Input your email: ")
							password = input("Input your password: ")
							with open(path, "a") as fp:
								fp.write("cert\n{}\n{}".format(mail, password))
							await self.loginWithCredential(mail=mail, password=password, path=path)
						break
				else:
					with open(path, "r") as fp:
						auth = fp.read()
						if "auth" in auth:
							token = auth.split(">")[1]
							await self.loginWithAuthToken(authToken=token)
						if "cert" in auth:
							y = auth.split("\n")
							await self.loginWithCredential(mail=y[1], password=y[2], cert=y[3])
		logs.info("Login success as %s" % (self.profile.displayName))
		return True
				
	async def loginWithQrcode(self, path=None):
		self.url(config.MAIN_PATH)
		qr = await self.call('getAuthQrcode', True, config.LOGIN_DEVICE_NAME, "")
		print("line://au/q/"+qr.verifier)
		r = self.waitForPhoneConfirm(qr.verifier)
		vr = r.json()['result']['verifier']
		self.url(config.AUTH_PATH)
		rq = LoginRequest(
			LoginType.QRCODE,
			IdentityProvider.LINE,
			None,
			None,
			True,
			config.LOGIN_LOCATION,
			config.LOGIN_DEVICE_NAME,
			None,
			vr,
			None,
			2
		)
		lr = await self.call('loginZ', rq)
		self.updateHeaders({
			'X-Line-Access': lr.authToken
		})
		self.authToken = lr.authToken
		self.cert = lr.certificate
		if path and path.endswith(".session"):
			with open(path, "w") as fp:
				text = "auth > {}".format(lr.authToken)
				fp.write(text)
		elif self.token_db is not None:
			if not self._validate_col({'name': path}):
				self.token_db.auth_col.insert_one({
					'name': path,
					'token': self.authToken
				})
		await self.afterLogin()

	async def loginWithCredential(self, mail, password, name=None, cert=None, path=None):
		self.url(config.MAIN_PATH)
		rsakey = await self.call('getRSAKeyInfo', config.LOGIN_PROVIDER)
		crypt  = self._encryptedEmailAndPassword(mail, password, rsakey)
		self.url(config.AUTH_PATH)
		rq = LoginRequest(
			LoginType.ID_CREDENTIAL,
			IdentityProvider.LINE_PHONE,
			rsakey.keynm,
			crypt,
			True,
			config.LOGIN_LOCATION,
			config.LOGIN_DEVICE_NAME,
			cert,
			None,
			crypt.encode() if type(crypt) == str else crypt, #none, #crypt
			0
		)
		result = await self.call('loginZ', rq)
		self.url(config.MAIN_PATH)
		if result.type == 3:
			print("Please confirm this code on your device %s"% (result.pinCode))
			r = self.waitForPhoneConfirm(result.verifier)
			rq = LoginRequest(
				LoginType.QRCODE,
				IdentityProvider.LINE,
				None, None, True,
				config.LOGIN_LOCATION,
				config.LOGIN_DEVICE_NAME,
				cert, r.json()['result']['verifier'],
				None, 
				2
			)
			self.url(config.AUTH_PATH)
			result = await self.call('loginZ', rq)
			self.updateHeaders({
				'X-Line-Access': result.authToken,
			})
			self.authToken = result.authToken
			self.cert = result.certificate
			self.url(config.MAIN_PATH)
		elif result.type == 1:
			self.authToken = result.authToken
			self.cert = result.certificate
			self.updateHeaders({
				'X-Line-Access': result.authToken
			})
		else:
			logs.critical('Login failed. got result type `%s`' % (result.type))
		if path is not None:
			with open(path, "a") as fp:
				text = "\n{}".format(self.cert)
				fp.write(text)
		elif self.token_db is not None and name is not None:
			if not self._validate_col({'name': name, 'mail': mail}):
				if cert is None:
					self.token_db.auth_col.insert_one({
						'mail': mail,
						'name': name,
						'cert': self.cert
					})
			else:
				r = self.token_db.auth_col.find_one({'name': name,'mail': mail})
				if 'cert' not in r.keys():
					self.token_db.auth_col.update_one({
						'name': name,
						'mail': mail
					}, {'$set': {'cert': self.cert}})
		await self.afterLogin()
	
	async def loginWithAuthToken(self, authToken, path=None):
		self.url(config.MAIN_PATH)
		self.updateHeaders({
			'X-Line-Access': authToken
		})
		self.authToken = authToken
		await self.afterLogin()

	async def afterLogin(self):
		self.url(config.NORMAL_PATH)
		self.profile = await self.call('getProfile')
		self.last_rev = await self.call('getLastOpRevision')
		self.settings = await self.call('getSettings')
		self.groups_ids = await self.call('getGroupIdsJoined')
		self.authToken = self.authToken
		
		for remoteFunc in self.afterLoginRemote:
			remoteFunc(**{
				'profile': self.profile,
				'settings': self.settings,
				'rev': self.last_rev,
				'mid': self.profile.mid,
				'authToken': self.authToken,
				'cert': getattr(self, 'cert', None),
				'app_header': (self.LA, self.UA)
			})
	
	async def logout(self):
		await self.call("logoutZ")