# -*- coding: utf-8 -*-
import os, sys, traceback, asyncio
from . import config
from . import models
from .filters import Filter
from .connections import Connection
from concurrent.futures import ThreadPoolExecutor
from inspect import *
from functools import partial
from .lib.Gen.ttypes import *
from thrift.transport.TTransport import TTransportException

class Handler:
    """
    Class for (next step|reply) handlers
    """

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

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
	
	async def conversation(self, uid, callback, *args, **kws):
		if uid in self.convers_handler.keys():
			self.convers_handler[uid].append(Handler(callback, *args, *kws))
		else:
			self.convers_handler[uid] = [Handler(callback, *args, **kws)]
				
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
		while True:
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
					if op.type in [25, 26]:
						i = 0
						cid = op.message.from_
						executed = False
						if cid in self.convers_handler.keys():
							handlers = self.convers_handler.pop(cid, None)
							if handlers:
								for handler in handlers:
									await self.execute(handler["callback"], op.message, *handler["args"], **handler["kwargs"])
								ops.pop(i)
								executed = True
						if not executed:
							i += 1
			except EOFError:
				continue
			except TTransportException:
				break
			except KeyboardInterrupt:
				raise
			except ShouldSyncException:
				pass
			except Exception:
				print(traceback.format_exc())