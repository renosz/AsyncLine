# -*- coding: utf-8 -*-
import os, sys, traceback, asyncio
from . import config
from . import models
from .filters import Filter
from .connections import Connection
from thrift.transport.TTransport import TTransportException
from .lib.Gen.ttypes import *
from inspect import *

class Handler:
	def __init__(self, callback, done=False):
		self.callback = callback
		self.done = done
		
	def __getitem__(self, item):
		return getattr(self, item)
		
class Poll(Connection):
	def __init__(self, client_name, loop=None):
		super().__init__(config.POLLING_PATH)
		self.transport.setTimeout(-1)
		self.LA, self.UA = models.ApplicationHeader(client_name).get()
		self.updateHeaders({
			'User-Agent': self.UA,
			'X-Line-Application': self.LA,
		})
		self.revision = 0
		self.loop = loop if loop else asyncio.get_event_loop()
		self.op_handler = {}
		self.convers_handler = {}
		self.fetch_event = asyncio.Event(loop=self.loop)
		if client_name in ['android', 'android2']:
			self.fetch = self.fetchOps
		else:
			self.fetch = self.fetchOperations

	def afterLogin(self, *args, **kws):
		for k,v in kws.items():
			try:
				setattr(self, k, v)
			except:
				pass
		self.revision = self.rev
		self.setupConnection()
		
	def setupConnection(self):
		self.updateHeaders({
			'X-Line-Access': self.authToken
		})

	def hooks(self, **parent_kw):
		def parent(func):
			def wrapper(*args, **kws):
				return func(*args,**kws)
			self.op_handler.setdefault(parent_kw.get('type',-1), []).append({
				wrapper:parent_kw.get("filters", None)
			})
			return wrapper
		return parent

	def streams(self):
		self.loop.run_until_complete(self.run_fetch())
	
	def conversation(self, msg, callback, done=False):
		cid = msg.from_
		msg.callback = callback
		if id in self.convers_handler.keys():
			self.convers_handler[cid].append(Handler(msg.callback, done))
		else:
			self.convers_handler[cid] = [Handler(msg.callback, done)]
			
	async def fetchOps(self, localRev, count=10):
		return await self.call('fetchOps', localRev, count, 0, 0)
		
	async def fetchOperations(self, localRev, count=10):
		return await self.call('fetchOperations', localRev, count)
	
	async def execute(self, coro, *args, **kwgs):
		if isroutine(coro):
			await coro(*args, **kwgs)
		else:
			coro(*args, **kwgs)
		
	async def setRevision(self, revision):
		self.revision = max(revision, self.revision)
	
	async def run_fetch(self, limit=1):
		while not self.fetch_event.is_set():
			try:
				ops = await self.fetch(self.revision, limit)
				for op in ops:
					self.revision = max(self.revision, op.revision)
					if self.op_handler:
						for handle, hFuncs in self.op_handler.items():
							if handle == op.type:
								for hFunc in hFuncs:
									for k, v in hFunc.items():
										if hFunc[k] is not None and isinstance(hFunc[k], Filter):
											if hFunc[k](op.message):
												await self.execute(k, op.message)
										elif hFunc[k] is None:
											await self.execute(k, op)
							else:
								continue
								self.fetch_event.set()
					if self.convers_handler != {} and (op.type == 26 and op.message.toType == 0):
						cid = op.message.from_
						if cid in self.convers_handler.keys():
							handlers = self.convers_handler.get(cid, None)
							if handlers:
								for handler in handlers:
									new_fetch = ops
									default_callback = handler.callback
									for fetch in new_fetch:
										if fetch.message.from_ in self.convers_handler.keys() and not fetch.message.command:
											if not handler.done:
												await self.execute(default_callback, fetch.message)
											else:
												await self.execute(default_callback, fetch.message)
												self.convers_handler.pop(fetch.message.from_)
										else:
											continue
			except EOFError:
				continue
			except TTransportException:
				self.fetch_event.clear()
				break
			except KeyboardInterrupt:
				raise
			except ShouldSyncException:
				self.fetch_event.clear()
				pass
			except Exception:
				print(traceback.format_exc())