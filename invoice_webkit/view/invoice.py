#!/usr/bin/env python
#
#  invoice.py
#
#  Modified by Vincent Renaville
#  Copyright (c) 2008 CamptoCamp. All rights reserved.
#
from osv import osv, fields
import pooler



class invoice_condition_text_webkit(osv.osv):
	"""add info condition in the invoice"""
	_name = "account.condition_text_webkit"
	_description = "Invoice condition text"
	
		
	_columns = {
		'name' : fields.char('Methode', required=True, size=128),
		'type' : fields.selection([('header','Header'),
		('footer','Footer')
		], 
		'type',required=True),
		'text': fields.text('text', translate=True,required=True),
	}

		
invoice_condition_text_webkit()



class account_invoice(osv.osv):
	""" Generated invoice does not advance in the workflow 
	and add text condition"""
	
	_inherit = "account.invoice"
	_description = 'Invoice'
	
	
	def get_trans_webkit(self, cr, uid, name, res_id, lang) :
		sql = " SELECT value     from ir_translation where name = '%s' \
		and res_id = %s and lang ='%s';" %(name, str(res_id), lang)
		cr.execute(sql)
		toreturn =  cr.fetchone()
		if toreturn :
		 return toreturn[0]
		else :
			return toreturn
		
	def set_comment_webkit(self, cr,uid,id,commentid):
		if not commentid :
			return {}
		cond = self.pool.get('account.condition_text_webkit').browse(
			cr,uid,commentid,{})
		translation_obj = self.pool.get('ir.translation')
		

		text =''
		if cond :
			text = cond.text
			try :
				lang = self.browse(cr, uid, id)[0].partner_id.lang
			except :
				lang = 'en_EN'
			res_trans = self.get_trans_webkit(cr, uid, 'account.condition_text_webkit,text', commentid, lang )
			if not res_trans :
				res_trans = text
		
		return {'value': {
				'note1_webkit': res_trans,
				}}
				
				
	def set_note_webkit(self, cr,uid,id,commentid):
		if not commentid :
			return {}
		cond = self.pool.get('account.condition_text_webkit').browse(
			cr,uid,commentid,{})
		translation_obj = self.pool.get('ir.translation')
		

		text =''
		if cond :
			text = cond.text
			try :
				lang = self.browse(cr, uid, id)[0].partner_id.lang
			except :
				lang = 'en_EN'
			res_trans = self.get_trans_webkit(cr, uid, 
				'account.condition_text_webkit,text', commentid, lang )
			if not res_trans :
				res_trans = text
		
		return {'value': {
				'note2_webkit': res_trans,
				}}



	
#	def create(self, cr, uid, vals, context={}):
#		tmp_id = super(account_invoice,self).create(cr, uid, vals, context)
#		#self.action_number(cr, uid, [tmp_id])
#		return tmp_id
		
	_columns = {
		'text_condition1_webkit': fields.many2one('account.condition_text_webkit', 'Header'),
		'text_condition2_webkit': fields.many2one('account.condition_text_webkit', 'Footer'),
		'note1_webkit' : fields.text('Header'),
		'note2_webkit' : fields.text('Footer'),
		'project_webkit': fields.many2one(
									'account.analytic.account', 
									'Project',
									 select=1
									),
		}

account_invoice()

	
